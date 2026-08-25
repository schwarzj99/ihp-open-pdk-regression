#!/usr/bin/env python3
"""Give the netlist a real substrate net and its ptap1 taps.

Second pass, run after convert_netlist.py. The shipped netlist has no
substrate node: it aliases the p-substrate onto whichever ground rail is
nearby. That cannot match a layout where every psub tie is labelled 'sub!'
and so extracts as a ptap1 DEVICE, because a two-terminal device needs two
distinct nodes at its ends. Aliasing also collapses diodes whenever the rail
it borrows is already the other terminal (see Findings.md, the shorted
DCNDiode in IOPadIOVss).

What this does:

  1. declares .GLOBAL sub, which KLayout auto-adds as a pin to every circuit
     that uses it and propagates upward, so no pin threading by hand
  2. inserts one ptap1 per entry in tap_inventory.md, A/P from the extraction
  3. repoints every NMOS bulk to sub (PMOS bulk stays on its well)
  4. repoints the rppd third terminal to sub
  5. fixes the DCNDiode/DCPDiode call sites

On (5): the mappings come from the extracted parent instances, not from name
matching. Name matching is a false friend here. DCNDiode's tap sits on a net
the LAYOUT labels 'anode', but that is the schematic's 'guard' pin, and the
schematic's 'anode' pin is the substrate. Verified identical across every pad:

  DCNDiode  pins (psub, tie, cathode, cathode$1) <- (\\$1, iovss, ...)
  DCPDiode  pins (psub, guard, cathode, anode, anode$1) <- (\\$1, iovss, iovdd, pad, ...)

so DCNDiode calls become (sub, <cathode>, iovss) and DCPDiode's guard is
iovss. The shipped DCPDiode call was already right.

  python3 add_taps.py [in.spi] [out.spi] [tap_inventory.md]

Defaults: netlist/sg13g2_io_devices.spi -> netlist/sg13g2_io_sub.spi
Safe to re-run; cells that already hold a ptap1 are left alone.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "netlist" / "sg13g2_io_devices.spi"
DST = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "netlist" / "sg13g2_io_sub.spi"
INV = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "tap_inventory.md"

NMOS = {"sg13_hv_nmos", "sg13_lv_nmos"}
GND = {"iovss", "vss"}   # rails the shipped netlist aliases the substrate onto
SUB = "sub"

# Layout net label -> schematic pin, where the two differ. Everything else in
# the inventory matches by name. Established from parent instance mappings.
TIE_OVERRIDE = {
    ("sg13g2_SecondaryProtection", "minus"): "iovss",
    ("sg13g2_DCNDiode", "anode"): "guard",
}

# Cells where an existing pin already IS the substrate, so the tap's WELL side
# must use that pin rather than the global. DCNDiode's diodes hang off it too;
# using the global instead would split the node and reintroduce the very
# parent-only-connection problem we are trying to avoid.
WELL_PIN = {"sg13g2_DCNDiode": "anode"}

# Gate antenna diode sizes, read back from the layout. Upstream has every clamp
# at l=0.64um w=0.48um (A=0.3072p P=2.24u), which matches none of the seven.
# The local copy had three of them corrected by hand (N43N43D4R to 0.48x0.48,
# N15N15D and P15N15D to 0.78x0.78); for that input those three entries are a
# no-op, so the same table serves both netlists.
#   A = l*w, P = 2*(l+w)
GATE_DIODE_FIX = {
    "sg13g2_Clamp_N2N2D":     ("A=0.6084p", "P=3.12u"),   # 0.78 x 0.78
    "sg13g2_Clamp_P2N2D":     ("A=0.2304p", "P=1.92u"),   # 0.48 x 0.48
    "sg13g2_Clamp_N8N8D":     ("A=0.6084p", "P=3.12u"),   # 0.78 x 0.78
    "sg13g2_Clamp_P8N8D":     ("A=0.2304p", "P=1.92u"),   # 0.48 x 0.48
    "sg13g2_Clamp_N15N15D":   ("A=0.6084p", "P=3.12u"),   # 0.78 x 0.78
    "sg13g2_Clamp_P15N15D":   ("A=0.6084p", "P=3.12u"),   # 0.78 x 0.78
    "sg13g2_Clamp_N43N43D4R": ("A=0.2304p", "P=1.92u"),   # 0.48 x 0.48
}

# rppd bodies that sit in an nwell rather than the p-substrate, so their third
# terminal belongs on the well rail. Upstream writes sub! here, which invents a
# connection the layout does not have; the local copy already had it right, so
# this is a no-op there.
RPPD_WELL = {
    "sg13g2_Clamp_P20N0D": "iovdd",
}

# Cells where the tap's net is called something else in the schematic than in
# the layout. Unlike TIE_OVERRIDE this is applied only when the layout's name
# is NOT a pin of the cell and the alias IS, so a netlist that already uses the
# layout name is left alone. Upstream renamed RCClampInverter's iovss pin to
# 'ground'; without this the tap hangs off a floating net and TAP0 goes
# unmatched.
TIE_ALIAS = {
    ("sg13g2_RCClampInverter", "iovss"): "ground",
}


# Pads whose body wires its sub-blocks to vss where the layout has iovss. The
# clamp, the RC inverter, the guard ring and the protection diodes all sit on
# the IO ground in silicon, alongside the large substrate tap; the shipped
# netlist puts them on the core ground. Applied to subcircuit instance lines
# only, so the taps (which are already correct) are left alone.
# Named per instance, deliberately. This cannot be a blanket "IO blocks sit on
# iovss" rule: Xgatelu's vss really is the core ground, and DCNDiode's cathode
# really is vss in IOPadVss. These are individual wiring errors in the shipped
# netlist, not one systematic one.
# Keyed by cell -> instance -> {argument index: correct net}. Positional, not
# by name: Xleveldown's arg 1 is legitimately vss (core ground) while its arg 3
# is the IO ground, so a name-based "vss -> iovss" swap would break the very
# pads it is meant to fix. Each index below is the sub-block's IO-ground pin.
BODY_NET_FIX = {
    "sg13g2_IOPadVdd":       {"Xnclamp": {0: "iovss"}, "Xrcinv": {1: "iovss"},
                              "Xpad_guard": {0: "iovss"}},
    "sg13g2_IOPadIOVdd":     {"Xnclamp": {0: "iovss"}, "Xrcinv": {1: "iovss"},
                              "Xpad_guard": {0: "iovss"}},
    "sg13g2_IOPadIOVss":     {"Xdcndiode": {1: "iovss"}, "Xdcpdiode": {0: "iovss"}},
    "sg13g2_IOPadOut30mA":   {"Xnclamp": {0: "iovss"}, "Xpclamp": {0: "iovss"}},
    "sg13g2_IOPadAnalog":    {"Xnclamp": {0: "iovss"}, "Xpclamp": {0: "iovss"},
                              "Xsecondprot": {1: "iovss"}},
    "sg13g2_IOPadInOut30mA": {"Xnclamp": {0: "iovss"}, "Xpclamp": {0: "iovss"},
                              "Xleveldown": {3: "iovss"}},
    "sg13g2_IOPadIn":        {"Xleveldown": {3: "iovss"}},
}


# Pins to delete from a .subckt declaration. sg13g2_IOPadAnalog gained a
# 'padbare' pin locally that is wired to nothing, is not among the six port
# labels in the layout (iovdd, iovss, pad, padres, vdd, vss), and was never
# added to the sg13g2_Gallery call. The pin count mismatch makes KLayout refuse
# to read the complete netlist.
PIN_DROP = {"sg13g2_IOPadAnalog": ("padbare",)}


def load_cell_fixes(d):
    """Whole-subckt replacements from cell_fixes/<cell>.spi, for cells whose
    shipped netlist does not describe the layout at all."""
    fixes = {}
    if not d.is_dir():
        return fixes
    for f in sorted(d.glob("*.spi")):
        body = [l for l in f.read_text().splitlines()]
        start = next((i for i, l in enumerate(body) if l.lower().startswith(".subckt")), None)
        if start is None:
            continue
        fixes[body[start].split()[1]] = body[start:]
    return fixes


def load_taps(path):
    taps = {}
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*(sg13g2_\S+)\s*\|\s*(\S+)\s*\|\s*(A=\S+)\s*\|\s*(P=\S+)\s*\|", line)
        if not m:
            continue
        cell, net, a, p = m.groups()
        net = net.split("$")[0]                       # iovss$1 -> iovss
        net = TIE_OVERRIDE.get((cell, net), net)
        taps.setdefault(cell, []).append((net, a, p))
    return taps


def split_inst(s):
    toks = s.split()
    idx = max(k for k, t in enumerate(toks) if "=" not in t)
    return toks[0], toks[1:idx], toks[idx], toks[idx + 1:]


CELL_FIXES = load_cell_fixes(ROOT / "cell_fixes")
taps = load_taps(INV)
if not taps:
    sys.exit(f"no taps parsed from {INV}")

lines = SRC.read_text().splitlines()
out, cur, body = [], None, []
stats = {"taps": 0, "nmos": 0, "rppd": 0, "calls": 0, "dant": 0, "gate": 0, "body": 0, "replaced": 0, "pins": 0, "skipped": 0, "alias": 0}


def flush(cell, body):
    """Append a cell's body, adding its tap before .ends."""
    if cell in CELL_FIXES:
        out.extend(CELL_FIXES[cell][:-1])   # drop its .ends, caller emits one
        stats["replaced"] += 1
        return
    if cell in taps and not any("ptap1" in b for b in body):
        well = WELL_PIN.get(cell, SUB)
        pins = body[0].split()[2:] if body else []
        for i, (tie, a, p) in enumerate(taps[cell]):
            alias = TIE_ALIAS.get((cell, tie))
            if alias and tie not in pins and alias in pins:
                tie = alias
                stats["alias"] += 1
            body.append(f"Rtap{i} {tie} {well} ptap1 {a} {p}")
            stats["taps"] += 1
    elif cell in taps:
        stats["skipped"] += 1
    out.extend(body)


for line in lines:
    s = line.strip()
    low = s.lower()

    if low.startswith(".subckt"):
        toks = s.split()
        cur = toks[1]
        if cur in PIN_DROP:
            keep = [t for t in toks[2:] if t not in PIN_DROP[cur]]
            if len(keep) != len(toks) - 2:
                line = " ".join(toks[:2] + keep)
                stats["pins"] += 1
        body = [line]
        continue
    if low.startswith(".ends"):
        flush(cur, body)
        out.append(line)
        cur, body = None, []
        continue
    if cur is None:
        out.append(line)
        continue

    if s and s[0] in "MmRrXxDd":
        inst, nets, model, params = split_inst(s)
        m = model.lower()
        changed = False

        if s[0] in "Dd" and "antenna" in m and cur in GATE_DIODE_FIX and "GATE" in inst.upper():
            params = list(GATE_DIODE_FIX[cur])
            stats["gate"] += 1
            changed = True

        if s[0] in "Dd" and m == "dantenna" and len(nets) == 2:
            # dantenna is n-diff to p-substrate, so its anode IS the substrate,
            # never a rail. dpantenna is p-diff to nwell and needs no change.
            # In WELL_PIN cells the substrate is an existing pin, not the
            # global; using the global there would split the node in two.
            well = WELL_PIN.get(cur, SUB)
            if nets[0] != well:
                nets[0] = well
                stats["dant"] += 1
                changed = True
        elif s[0] in "Mm" and m in NMOS and len(nets) == 4 and nets[3] != SUB:
            nets[3] = SUB
            stats["nmos"] += 1
            changed = True
        elif s[0] in "Rr" and m == "rppd" and len(nets) == 3 and cur in RPPD_WELL:
            # Poly resistor inside an nwell: its body is the well, never the
            # substrate. Upstream writes sub! here, which shorts the well rail
            # to the substrate; the layout has "R iovdd $6 iovdd rppd".
            if nets[2] != RPPD_WELL[cur]:
                nets[2] = RPPD_WELL[cur]
                stats["rppd"] += 1
                changed = True
        elif s[0] in "Rr" and m == "rppd" and len(nets) == 3 and nets[2] in GND:
            # Only rppd sitting over p-substrate. A poly resistor inside an
            # nwell (the P-type clamps) has its body terminal on the WELL, and
            # the shipped netlist already names that correctly. Rewriting it to
            # sub invents a connection that is not in the layout, which is why
            # Clamp_P20N0D extracts as "R iovdd \\$6 iovdd rppd".
            nets[2] = SUB
            stats["rppd"] += 1
            changed = True
        elif model == "sg13g2_DCNDiode" and len(nets) == 3:
            nets[0], nets[2] = SUB, "iovss"      # anode is psub; tie is iovss
            stats["calls"] += 1
            changed = True
        elif model == "sg13g2_RCClampResistor" and len(nets) == 3 and nets[2] in GND:
            # Third pin is the resistor's substrate, and the callers pass a
            # ground rail. Left alone it drags the whole pad's sub/iovss/vss
            # net matching down with it.
            nets[2] = SUB
            stats["calls"] += 1
            changed = True
        elif model == "sg13g2_DCPDiode" and len(nets) == 3:
            nets[2] = "iovss"                     # guard; shipped value was right
            stats["calls"] += 1
            changed = True

        if s[0] in "Xx" and inst in BODY_NET_FIX.get(cur, {}):
            for idx, net in BODY_NET_FIX[cur][inst].items():
                if idx < len(nets) and nets[idx] != net:
                    nets[idx] = net
                    stats["body"] += 1
                    changed = True

        if changed:
            body.append(f"{inst} {' '.join(nets)} {model} {' '.join(params)}".rstrip())
            continue

    body.append(line)

# .GLOBAL goes ahead of the first subckt
first = next(i for i, l in enumerate(out) if l.lower().startswith(".subckt"))
out.insert(first, ".GLOBAL sub\n")

DST.write_text("\n".join(out) + "\n")
print(f"{SRC.name} -> {DST.name}")
print(f"  .GLOBAL sub declared")
print(f"  ptap1 taps inserted      {stats['taps']:4d}  ({len(taps)} cells in inventory)")
print(f"  NMOS bulks -> sub        {stats['nmos']:4d}")
print(f"  rppd sub terminals       {stats['rppd']:4d}")
print(f"  dantenna anodes -> sub   {stats['dant']:4d}")
print(f"  gate diode sizes fixed   {stats['gate']:4d}")
print(f"  DCNDiode/DCPDiode calls  {stats['calls']:4d}")
print(f"  pad body nets fixed      {stats['body']:4d}")
print(f"  whole cells replaced     {stats['replaced']:4d}  (from cell_fixes/)")
print(f"  stray pins dropped       {stats['pins']:4d}")
print(f"  tap nets re-aliased      {stats['alias']:4d}")
if stats["skipped"]:
    print(f"  cells already tapped     {stats['skipped']:4d}  (left alone)")
