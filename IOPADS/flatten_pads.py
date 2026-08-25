#!/usr/bin/env python3
"""Write a fully flattened SPICE netlist per IO pad.

The PDK's helper cells (DCNDiode, DCPDiode, Clamp_*, ...) tie their parallel
devices together with metal drawn in the PARENT pad cell, not inside the cell
itself. The shipped netlist instead models those nets as internal to each
helper cell, so a hierarchical compare of a single pad can never match: the
extractor pushes each finger out as its own pin (pad, pad$1 ... pad$21) while
the schematic has one.

Flattening both sides sidesteps the disagreement. This writes one .subckt per
pad with every sub-block inlined, to be compared against a flat extraction
(RUN_MODE=flat). Empty subckts (the guard rings) vanish, which is correct:
they carry no devices.

Run INSIDE the container:
  python3 /foss/designs/ihp-open-pdk-regression/IOPADS/flatten_pads.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "netlist" / "sg13g2_io.spi"
OUT = ROOT / "netlist" / "pads_flat"
LAYOUT = ROOT / "layout"


def parse(path):
    """-> (header lines, {name: (pins, [body lines])})"""
    raw = path.read_text().splitlines()
    lines = []
    for ln in raw:
        if ln.startswith("+") and lines:
            lines[-1] += " " + ln[1:].strip()
        else:
            lines.append(ln)

    first = next(i for i, l in enumerate(lines) if l.lower().startswith(".subckt"))
    h = first
    while h > 0 and lines[h - 1].startswith("*"):
        h -= 1
    header = lines[:h]

    subs, i = {}, 0
    while i < len(lines):
        if lines[i].lower().startswith(".subckt"):
            toks = lines[i].split()
            name, pins = toks[1], toks[2:]
            j = i
            while not lines[j].lower().startswith(".ends"):
                j += 1
            body = [l.strip() for l in lines[i + 1:j]
                    if l.strip() and not l.strip().startswith("*")]
            subs[name] = (pins, body)
            i = j + 1
        else:
            i += 1
    return header, subs


def split_inst(line):
    """'Xfoo a b model p=1' -> (inst, [nets], model, [params])"""
    toks = line.split()
    idx = max(k for k, t in enumerate(toks) if "=" not in t)
    return toks[0], toks[1:idx], toks[idx], toks[idx + 1:]


def flatten(subs, name, prefix, netmap, out):
    """Inline `name` into `out`, translating nets through `netmap`."""
    _, body = subs[name]
    for line in body:
        if not line[0] in "Xx":
            print(f"  ignoring unhandled line: {line}", file=sys.stderr)
            continue
        inst, nets, model, params = split_inst(line)

        def xlate(n):
            if n.endswith("!"):          # global net, never renamed
                return n
            return netmap.get(n, f"{prefix}{n}")

        actual = [xlate(n) for n in nets]

        if model in subs:
            child_pins, _ = subs[model]
            if len(child_pins) != len(actual):
                sys.exit(f"{name}: {inst} passes {len(actual)} nets to {model} "
                         f"which declares {len(child_pins)} pins")
            flatten(subs, model, f"{prefix}{inst[1:]}.",
                    dict(zip(child_pins, actual)), out)
        else:
            out.append(f"X{prefix}{inst[1:]} {' '.join(actual)} {model} "
                       f"{' '.join(params)}".rstrip())


header, subs = parse(SRC)
pads = sorted(p.stem for p in LAYOUT.glob("sg13g2_IOPad*.gds"))
missing = [p for p in pads if p not in subs]
if missing:
    sys.exit(f"no subckt for: {missing}")

OUT.mkdir(exist_ok=True)
for pad in pads:
    pins, _ = subs[pad]
    devices = []
    flatten(subs, pad, "", {p: p for p in pins}, devices)

    nets = sorted({n for d in devices for n in split_inst(d)[1]})
    floating = [n for n in nets
                if sum(n in split_inst(d)[1] for d in devices) == 1 and n not in pins]

    text = "\n".join(
        [f"* {pad} (flattened)", "",
         f"* Every sub-block inlined, for comparison against a flat extraction.",
         f"* Generated from {SRC.name}; edit the source, not this file.", ""]
        + header[1:]
        + ["", f".subckt {pad} {' '.join(pins)}"]
        + devices
        + [f".ends {pad}", ""])
    (OUT / f"{pad}.spi").write_text(text)

    warn = f"  ONE-TERMINAL NETS: {floating}" if floating else ""
    print(f"{pad:26s} {len(devices):4d} devices  {len(nets):3d} nets{warn}")
