#!/usr/bin/env python3
"""Add the missing PolyRes (128/0) markers so rppd resistors extract.

Cells in the IO library draw poly resistor fingers with contacts, salblock,
psd and extblock but no PolyRes marker. rppd extraction needs it:

    polyres_mk = polyres_drw.and(extblock_drw).interacting(gatpoly)...
    rppd_res   = polyres_mk.and(psd_drw).and(salblock_drw)...

Without 128/0 the cell extracts to an EMPTY netlist while the schematic
declares rppd devices. Library-wide, PolyRes exists in only two cells
(Clamp_N20N0D and Clamp_P20N0D), which is why theirs is the only rppd that
ever extracted.

Two things this gets right that a first guess does not:

  PER FINGER. A single marker spanning all fingers (the shape of the salblock
  itself) derives one core region with 2N ports, which the 2-terminal
  extractor cannot use, and the cell still extracts to nothing.

  GATE-SAFE. The marker is salblock AND (GatPoly MINUS Activ). salblock is
  also used over transistor gates for silicide blocking, and marking a gate
  as a resistor would invent a device that is not there.

Which cells to touch is read from the netlist: any subckt that declares rppd
but whose layout cell has no 128/0. Nothing else is touched.

  python3 fix_polyres_marker.py [in.gds] [out.gds] [netlist.spi]

Defaults: layout/sg13g2_io.gds -> layout/sg13g2_io_polyres.gds,
          netlist/sg13g2_io.spi
Writes a new file; the input is never modified. Safe to re-run.
"""
import pathlib
import sys

import pya

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "layout" / "sg13g2_io.gds"
DST = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "layout" / "sg13g2_io_polyres.gds"
NET = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "netlist" / "sg13g2_io.spi"

GATPOLY, SALBLOCK, ACTIV, POLYRES = (5, 0), (28, 0), (1, 0), (128, 0)


def rppd_per_subckt(path):
    """{subckt: rppd count}. Accepts X-style or converted R-style device lines."""
    counts, cur = {}, None
    for line in path.read_text().splitlines():
        s = line.strip()
        low = s.lower()
        if low.startswith(".subckt"):
            cur = s.split()[1]
        elif low.startswith(".ends"):
            cur = None
        elif cur and s[:1] in "XxRr" and "rppd" in low.split():
            counts[cur] = counts.get(cur, 0) + 1
    return counts


declared = rppd_per_subckt(NET)
if not declared:
    sys.exit(f"no rppd devices found in {NET}")

ly = pya.Layout()
ly.read(str(SRC))
print(f"{SRC.name}: {ly.cells()} cells, dbu {ly.dbu}")
print(f"{NET.name}: rppd declared in {len(declared)} subckt(s)\n")

dst_layer = ly.layer(*POLYRES)
added_total = 0
warnings = []

for name in sorted(declared):
    want = declared[name]
    cell = ly.cell(name)
    if cell is None:
        print(f"{name:30s} {want:3d} rppd   no layout cell, skipped")
        continue

    have = cell.shapes(dst_layer).size()
    if have:
        print(f"{name:30s} {want:3d} rppd   already has {have} PolyRes, skipped")
        continue

    def region(layer):
        idx = ly.find_layer(*layer)
        return pya.Region(cell.begin_shapes_rec(idx)) if idx is not None else pya.Region()

    sal, gat, act = region(SALBLOCK), region(GATPOLY), region(ACTIV)
    if sal.is_empty() or gat.is_empty():
        print(f"{name:30s} {want:3d} rppd   no salblock or gatpoly, skipped")
        warnings.append(f"{name}: cannot derive a marker")
        continue

    markers = sal & (gat - act)              # per finger, gates excluded
    for poly in markers.each():
        cell.shapes(dst_layer).insert(poly)

    n = markers.count()
    added_total += n
    note = "" if n == want else f"   <<< expected {want}"
    print(f"{name:30s} {want:3d} rppd   added {n:3d} PolyRes{note}")
    if n != want:
        warnings.append(f"{name}: {n} markers derived but {want} rppd declared")

if added_total:
    ly.write(str(DST))
    print(f"\nwrote {DST}")
else:
    print("\nnothing to do, no file written")

for w in warnings:
    print(f"WARNING: {w}")
