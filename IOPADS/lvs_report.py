#!/usr/bin/env python3
"""Print per-circuit LVS match status from an .lvsdb.

The runner only ever says "Netlists don't match". This says which circuit
failed, which is what you need to work through the IO pads one cell at a time.

  python3 lvs_report.py <run_dir_or_lvsdb> [-v]

-v also lists the mismatching pins, nets, devices and subcircuits inside each
bad circuit. "first" is the layout side, "second" the schematic.
"""
import pathlib
import sys

import pya

args = [a for a in sys.argv[1:] if not a.startswith("-")]
verbose = "-v" in sys.argv
if not args:
    sys.exit(__doc__)

target = pathlib.Path(args[0])
if target.is_dir():
    found = sorted(target.rglob("*.lvsdb"))
    if not found:
        sys.exit(f"no .lvsdb under {target}")
    target = found[0]

lvs = pya.LayoutVsSchematic()
lvs.read(str(target))
xref = lvs.xref()
if xref is None:
    sys.exit(f"{target.name} holds no comparison result (was it a --net_only run?)")

S = pya.NetlistCrossReference.Status
NAME = {getattr(S, n): n for n in dir(S) if not n.startswith("_") and n[0].isupper()}
OK = ("Match", "MatchWithWarning")


def nm(o):
    if o is None:
        return "(none)"
    for attr in ("expanded_name", "name"):
        v = getattr(o, attr, None)
        if callable(v):
            return v()
        if v:
            return v
    return str(o)


print(f"{target.name}\n")
bad = 0
for cp in xref.each_circuit_pair():
    st = NAME.get(cp.status(), str(cp.status()))
    a, b = nm(cp.first()), nm(cp.second())
    name = a if a == b else f"{a} <-> {b}"
    flag = "" if st in OK else "  <<<"
    if flag:
        bad += 1
    print(f"{st:18s} {name}{flag}")

    if not verbose or not flag:
        continue
    for kind, items in (("pin", xref.each_pin_pair(cp)),
                        ("net", xref.each_net_pair(cp)),
                        ("device", xref.each_device_pair(cp)),
                        ("subcircuit", xref.each_subcircuit_pair(cp))):
        for pair in items:
            pst = NAME.get(pair.status(), str(pair.status()))
            if pst in OK:
                continue
            print(f"    {pst:16s} {kind:11s} {nm(pair.first()):28s} vs  {nm(pair.second())}")

print()
print("all circuits match" if bad == 0 else f"{bad} circuit(s) do not match")
