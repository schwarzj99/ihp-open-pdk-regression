#!/usr/bin/env python3
"""Decide whether an LVS run actually passed, by asking the .lvsdb.

Do not trust run_lvs.py's Status field. It prints

    | Status  | PASS |
    | Outcome | Comparison mode: completed (no explicit PASS/FAIL signature found). |
    | Errors  | 1 |

when the run died before comparing anything: a missing file, an unreadable
netlist, a bad topcell. Grepping the log for "PASS" therefore reports success
for runs that did nothing at all.

The .lvsdb is KLayout's own record of what it compared, so this checks that
instead:

  1. an .lvsdb exists                     - the run got far enough to write one
  2. it carries a cross-reference         - a comparison was actually attempted
  3. the schematic netlist is non-empty   - the netlist was read and had circuits
  4. there is at least one circuit pair   - something was compared
  5. every pair is Match, both sides present
  6. the expected top cell is among them  - the right thing was compared

Anything else is a failure, and the reason is printed.

  python3 lvs_check.py <run_dir> [--topcell NAME] [-q]

Exit code 0 only if the run genuinely passed.
"""
import pathlib
import sys

import pya

args = [a for a in sys.argv[1:] if not a.startswith("-")]
quiet = "-q" in sys.argv
topcell = None
if "--topcell" in sys.argv:
    topcell = sys.argv[sys.argv.index("--topcell") + 1]
    args = [a for a in args if a != topcell]
if not args:
    sys.exit(__doc__)

target = pathlib.Path(args[0])


def fail(msg):
    print(f"FAIL  {target.name}: {msg}")
    sys.exit(1)


dbs = sorted(target.rglob("*.lvsdb")) if target.is_dir() else [target]
if not dbs:
    fail("no .lvsdb was written, so the run did not reach the comparison")

lvs = pya.LayoutVsSchematic()
lvs.read(str(dbs[0]))

xref = lvs.xref()
if xref is None:
    fail("the .lvsdb holds no cross-reference, so nothing was compared")

schematic = xref.netlist_b()
if schematic is None or not list(schematic.each_circuit()):
    fail("the schematic netlist is empty, so it was never successfully read "
         "(check the netlist parses: device lines need D/M/R prefixes)")

S = pya.NetlistCrossReference.Status
NAME = {getattr(S, n): n for n in dir(S) if not n.startswith("_") and n[0].isupper()}
OK = ("Match", "MatchWithWarning")

pairs = list(xref.each_circuit_pair())
if not pairs:
    fail("the cross-reference contains no circuit pairs")

bad, matched = [], []
for cp in pairs:
    st = NAME.get(cp.status(), str(cp.status()))
    a, b = cp.first(), cp.second()
    an = a.name if a else "(none)"
    bn = b.name if b else "(none)"
    if st in OK and a and b:
        matched.append(an)
    else:
        bad.append(f"{st}: {an} <-> {bn}")

if bad:
    print(f"FAIL  {target.name}: {len(bad)} of {len(pairs)} circuits did not match")
    for b in bad:
        print(f"        {b}")
    print(f"        python3 lvs_report.py {target} -v")
    sys.exit(1)

if topcell and topcell not in matched:
    fail(f"'{topcell}' is not among the matched circuits {matched}; "
         "the wrong cell was compared")

if not quiet:
    print(f"PASS  {target.name}: {len(matched)} circuits matched "
          f"({', '.join(matched)})")
sys.exit(0)
