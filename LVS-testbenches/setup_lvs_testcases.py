
#!/usr/bin/env python3
"""
setup_lvs_testcases.py

Scans a GDS folder for layout files, finds matching Xschem schematics,
converts each schematic to a CDL netlist via Xschem (headless), and
copies both into the LVS testcase directory structure.

  flat (default):
    <out_dir>/<group>/layout/<cell>.gds
    <out_dir>/<group>/netlist/<cell>.cdl

  per-cell:
    <out_dir>/<group>/<cell>/layout/<cell>.gds
    <out_dir>/<group>/<cell>/netlist/<cell>.cdl

Usage:
    python3 setup_lvs_testcases.py --group iic_devices
    python3 setup_lvs_testcases.py --group iic_devices --structure per-cell
    python3 setup_lvs_testcases.py --top_dir /foss/designs/my-bench --group MOS --dry_run
"""

import argparse
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path


def die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)
    
def run_xschem_lvs(sch_file: Path, out_dir: Path) -> subprocess.CompletedProcess:
    tcl = f"""\
set lvs_netlist 1
set netlist_dir {{{str(out_dir)}}}
xschem load {{{str(sch_file)}}}
xschem netlist
exit
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tcl', delete=False) as f:
        f.write(tcl)
        tcl_path = Path(f.name)

    try:
        return subprocess.run(
            ["xschem", "--no_x", "--script", str(tcl_path)],
            capture_output=True,
            text=True,
        )
    finally:
        tcl_path.unlink(missing_ok=True)

def main():
    parser = argparse.ArgumentParser(
        description="Populate LVS testcases from GDS layouts + Xschem schematics"
    )
    parser.add_argument(
        "--top_dir", "-t",
        default="/foss/designs/ihp-open-pdk-regression/LVS-testbenches",
        help="Top directory containing gds/ and schematic/ subfolders",
    )
    parser.add_argument(
        "--gds_dir", "-g",
        default=None,
        help="Override GDS folder path (default: <top_dir>/gds)",
    )
    parser.add_argument(
        "--sch_dir", "-s",
        default=None,
        help="Override schematic folder path (default: <top_dir>/schematic)",
    )
    parser.add_argument(
        "--out_dir", "-o",
        default="./unit",
        help="Output testcases root directory (default: ./unit)",
    )
    parser.add_argument(
        "--group",
        default="iic_devices",
        help="Device group name used as subfolder and --device= argument (default: PR)",
    )
    parser.add_argument(
        "--structure",
        choices=["flat", "per-cell"],
        default="flat",
        help="Output structure: 'flat' = shared layout/ and netlist/ folders; "
             "'per-cell' = one subfolder per cell (default: flat)",
    )
    parser.add_argument(
        "--dry_run", "-n",
        action="store_true",
        help="Print what would be done without copying or running Xschem",
    )
    args = parser.parse_args()

    top     = Path(args.top_dir)
    gds_dir = Path(args.gds_dir)  if args.gds_dir else top / "gds"
    sch_dir = Path(args.sch_dir)  if args.sch_dir else top / "schematic"
    out_dir = Path(args.out_dir)

    if not gds_dir.exists():
        die(f"GDS directory not found: {gds_dir}")
    if not sch_dir.exists():
        die(f"Schematic directory not found: {sch_dir}")

    gds_files = sorted(gds_dir.glob("*.gds"))
    if not gds_files:
        die(f"No .gds files found in {gds_dir}")

    print(f"Found {len(gds_files)} GDS file(s) in {gds_dir}")
    print(f"Schematic directory : {sch_dir}")
    print(f"Output directory    : {out_dir / args.group}")
    print(f"Structure           : {args.structure}")
    print(f"Dry run             : {args.dry_run}\n")

    skipped = []
    failed  = []

    for gds_file in gds_files:
        cell     = gds_file.stem
        sch_file = sch_dir / f"{cell}.sch"

        if not sch_file.exists():
            print(f"  [SKIP] {cell} — no matching schematic at {sch_file}")
            skipped.append(cell)
            continue

        if args.structure == "flat":
            dest_layout  = out_dir / args.group / "layout"  / f"{cell}.gds"
            dest_netlist = out_dir / args.group / "netlist" / f"{cell}.cdl"
        else:  # per-cell
            dest_layout  = out_dir / args.group / cell / "layout"  / f"{cell}.gds"
            dest_netlist = out_dir / args.group / cell / "netlist" / f"{cell}.cdl"

        print(f"  {cell}")
        print(f"    layout  : {gds_file} -> {dest_layout}")
        print(f"    netlist : {sch_file} -> {dest_netlist}")

        if args.dry_run:
            continue

        dest_layout.parent.mkdir(parents=True, exist_ok=True)
        dest_netlist.parent.mkdir(parents=True, exist_ok=True)

        # --- Copy GDS ---
        shutil.copy2(gds_file, dest_layout)

        # --- Run Xschem to export netlist ---
        result = run_xschem_lvs(sch_file, dest_netlist.parent)

        if result.returncode != 0:
            print(f"    [FAIL] xschem returned {result.returncode}")
            print(f"           {result.stderr.strip()}")
            failed.append(cell)
            continue

        # Xschem outputs <cell>.spice or <cell>.cdl depending on version/config
        candidates = sorted(dest_netlist.parent.glob(f"{cell}.*"))
        if not candidates:
            print(f"    [FAIL] xschem ran cleanly but produced no netlist")
            failed.append(cell)
            continue

        if candidates[0] != dest_netlist:
            candidates[0].rename(dest_netlist)

        print(f"    CDL written : {dest_netlist}")

    # --- Summary ---
    processed = len(gds_files) - len(skipped) - len(failed)
    print(f"\n{'(dry run) ' if args.dry_run else ''}Done.")
    print(f"  Processed : {processed}")
    print(f"  Skipped   : {len(skipped)}  {skipped if skipped else ''}")
    print(f"  Failed    : {len(failed)}  {failed  if failed  else ''}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()