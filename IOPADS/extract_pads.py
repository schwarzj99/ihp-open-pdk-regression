#!/usr/bin/env python3
"""Cut each IO pad out of the sg13g2_io gallery GDS, hierarchy intact.

Run INSIDE the IIC-OSIC-TOOLS container:
  python3 /foss/designs/ihp-open-pdk-regression/IOPADS/extract_pads.py

Writes layout/<pad>.gds for every sg13g2_IOPad* cell in the gallery. Any
existing file of that name is moved to layout/flat_extracted/ first, so the
earlier hand-dragged flat versions are kept rather than overwritten.

SaveLayoutOptions.add_cell selects the cell plus its whole child tree, so the
sub-hierarchy and the 1nm dbu come across untouched.
"""
import pathlib
import shutil
import sys

import pya

ROOT = pathlib.Path(__file__).resolve().parent
MASTER = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "layout" / "sg13g2_io.gds"
LAYOUT = ROOT / "layout"
BACKUP = LAYOUT / "flat_extracted"

if not MASTER.is_file():
    sys.exit(f"gallery GDS not found: {MASTER}")

ly = pya.Layout()
ly.read(str(MASTER))
print(f"{MASTER.name}: {ly.cells()} cells, dbu {ly.dbu}")
if abs(ly.dbu - 0.001) > 1e-9:
    print(f"WARNING: dbu is {ly.dbu}, not 0.001; extraction/LVS needs 1nm")

pads = sorted(c.name for c in ly.each_cell() if c.name.startswith("sg13g2_IOPad"))
if not pads:
    sys.exit("no sg13g2_IOPad* cells found in the gallery")

BACKUP.mkdir(exist_ok=True)
print(f"{len(pads)} pad cells, backing up existing files to {BACKUP.name}/\n")

for pad in pads:
    cell = ly.cell(pad)
    out = LAYOUT / f"{pad}.gds"
    if out.exists() and not (BACKUP / out.name).exists():
        shutil.move(str(out), str(BACKUP / out.name))

    opts = pya.SaveLayoutOptions()
    opts.format = "GDS2"
    opts.clear_cells()
    opts.add_cell(cell.cell_index())        # cell + entire child tree
    ly.write(str(out), opts)

    chk = pya.Layout()
    chk.read(str(out))
    tops = [c.name for c in chk.top_cells()]
    ok = tops == [pad] and abs(chk.dbu - 0.001) < 1e-9
    print(f"{pad:26s} {chk.cells():4d} cells  dbu {chk.dbu}  "
          f"{out.stat().st_size / 1e6:6.2f} MB  {'ok' if ok else 'CHECK ' + str(tops)}")
