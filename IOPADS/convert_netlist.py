#!/usr/bin/env python3
"""Rewrite sg13g2_io.spi device calls as real SPICE elements.

The shipped netlist writes every device as a subcircuit call:

    Xdcdiode[0] anode cathode dantenna l=1.26um w=27.78um

KLayout reads that as a call to a circuit named DANTENNA(L=1.26U,W=27.78U), so
the schematic ends up with ZERO devices and can never match anything. This
converts those lines to the element prefixes the LVS deck's reader handles
(CUSTOM_READER = M C R Q L D in globals.lvs):

    Dd0 anode cathode dantenna A=35.0028p P=58.08u

Genuine subcircuit calls are left alone.

  python3 convert_netlist.py [in.spi] [out.spi]

Defaults: netlist/sg13g2_io.spi -> netlist/sg13g2_io_devices.spi

This does the mechanical part only. It does NOT add the substrate taps, which
need per-cell judgement about which pin is the substrate; see cell_tests/ for
the cells confirmed so far.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "netlist" / "sg13g2_io.spi"
DST = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "netlist" / "sg13g2_io_devices.spi"

DIODES = {"dantenna", "dpantenna"}
MOS = {"sg13_hv_nmos", "sg13_hv_pmos", "sg13_lv_nmos", "sg13_lv_pmos"}
RES = {"rppd"}


def num(v):
    """'1.26um' -> 1.26 (microns)."""
    m = re.match(r"^([-+0-9.eE]+)\s*([a-zA-Z]*)$", v)
    if not m:
        raise ValueError(v)
    x, unit = float(m.group(1)), m.group(2).lower()
    return x * {"": 1.0, "u": 1.0, "um": 1.0, "n": 1e-3, "nm": 1e-3, "m": 1e3, "mm": 1e3}[unit]


def fmt(x):
    return f"{x:.6g}"


def split_inst(line):
    toks = line.split()
    idx = max(k for k, t in enumerate(toks) if "=" not in t)
    params = {}
    for t in toks[idx + 1:]:
        k, _, v = t.partition("=")
        params[k.lower()] = v
    return toks[0], toks[1:idx], toks[idx], params


raw = SRC.read_text().splitlines()
subckts = {l.split()[1] for l in raw if l.lower().startswith(".subckt")}

out, counts, unknown = [], {"D": 0, "M": 0, "R": 0, "X": 0}, {}
for line in raw:
    s = line.strip()
    if not s or s[0] not in "Xx":
        out.append(line)
        continue

    inst, nets, model, params = split_inst(s)
    base = re.sub(r"[\[\]]", "_", inst[1:]).strip("_")
    m = model.lower()

    if model in subckts:                       # a real subcircuit call
        out.append(line)
        counts["X"] += 1
    elif m in DIODES:
        l, w = num(params["l"]), num(params["w"])
        out.append(f"D{base} {' '.join(nets)} {model} "
                   f"A={fmt(l * w)}p P={fmt(2 * (l + w))}u")
        counts["D"] += 1
    elif m in MOS:
        out.append(f"M{base} {' '.join(nets)} {model} "
                   f"L={fmt(num(params['l']))}u W={fmt(num(params['w']))}u")
        counts["M"] += 1
    elif m in RES:
        rest = " ".join(f"{k}={fmt(num(v))}u" if k in ("l", "w") else f"{k}={v}"
                        for k, v in params.items())
        out.append(f"R{base} {' '.join(nets)} {model} {rest}".rstrip())
        counts["R"] += 1
    else:
        unknown.setdefault(model, 0)
        unknown[model] += 1
        out.append(line)

DST.write_text("\n".join(out) + "\n")
print(f"{SRC.name} -> {DST.name}")
print(f"  D (diodes)      {counts['D']:5d}")
print(f"  M (mos)         {counts['M']:5d}")
print(f"  R (resistors)   {counts['R']:5d}")
print(f"  X (subcircuits) {counts['X']:5d}  left as-is")
for k, v in sorted(unknown.items()):
    print(f"  UNRECOGNISED    {k} x{v}  left as-is")
