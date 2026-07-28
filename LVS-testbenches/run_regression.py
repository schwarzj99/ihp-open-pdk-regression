#!/usr/bin/env python3
# Regression runner for IHP-Open-PDK LVS/DRC testbenches.
#
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# Johannes Kepler University, Department for Integrated Circuits
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
#
# Directly invokes xschem, KLayout (run_lvs.py / run_drc.py), sak-lvs.sh,
# and sak-drc.sh.  No make round-trips.
#
# Requires environment variables: PDK_ROOT, PDK
#
# Usage:
#   python3 run_regression.py --tools klayout-lvs magic-drc [--cell CELL]
#                              [--ev-precision N] [--results-dir DIR]
# ============================================================================

import argparse
import csv
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Tools exposed as valid --tools arguments.
# klayout-lvs-netlist / magic-lvs-netlist are standalone export utilities;
# the full klayout-lvs / magic-lvs targets call them internally as well.
VALID_TOOLS = [
    "klayout-lvs-netlist",
    "magic-lvs-netlist",
    "klayout-lvs",
    "magic-lvs",
    "klayout-drc",
    "magic-drc",
]

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%H:%M:%S"


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def build_config(base_dir: Path, ev_precision: int) -> dict:
    pdk_root = os.environ.get("PDK_ROOT")
    pdk = os.environ.get("PDK")
    if not pdk_root:
        logging.error("Environment variable PDK_ROOT is not set.")
        sys.exit(1)
    if not pdk:
        logging.error("Environment variable PDK is not set.")
        sys.exit(1)
    return {
        "base_dir":     base_dir,
        "pdk_root":     Path(pdk_root),
        "pdk":          pdk,
        "ev_precision": ev_precision,
        "sch_dir":      base_dir / "schematic",
        "gds_dir":      base_dir / "gds",
        "net_sch_dir":  base_dir / "netlist" / "schematic",
        "net_lay_dir":  base_dir / "netlist" / "layout",
        "lvs_rpt_dir":  base_dir / "verification" / "lvs",
        "drc_rpt_dir":  base_dir / "verification" / "drc",
    }


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------

def _run(cmd: list) -> tuple:
    """Run a command list and return (returncode, combined_stdout_stderr)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def run_klayout_lvs_netlist(cell: str, cfg: dict) -> tuple:
    """Export a KLayout-compatible CDL netlist from Xschem."""
    cfg["net_sch_dir"].mkdir(parents=True, exist_ok=True)
    tcl_cmd = (
        f"set spiceprefix 1; "
        f"set lvs_netlist 1; "
        f"set top_is_subckt 1; "
        f"set lvs_ignore 0; "
        f"set ev_precision {cfg['ev_precision']}; "
        f"set netlist_dir {cfg['net_sch_dir']}; "
        f"xschem set netlist_name "
        f"[file tail [file rootname [xschem get current_name]]]_klayout.cdl; "
        f"xschem netlist"
    )
    cmd = [
        "xschem", "-s", "-r", "-x", "-q",
        "--rcfile", str(cfg["sch_dir"] / "xschemrc"),
        "--command", tcl_cmd,
        str(cfg["sch_dir"] / f"{cell}.sch"),
    ]
    rc, output = _run(cmd)
    return rc == 0, output


def run_magic_lvs_netlist(cell: str, cfg: dict) -> tuple:
    """Export a Magic-compatible SPICE netlist from Xschem."""
    cfg["net_sch_dir"].mkdir(parents=True, exist_ok=True)
    tcl_cmd = (
        f"set spiceprefix 1; "
        f"set lvs_netlist 0; "
        f"set top_is_subckt 1; "
        f"set lvs_ignore 1; "
        f"set ev_precision {cfg['ev_precision']}; "
        f"set netlist_dir {cfg['net_sch_dir']}; "
        f"xschem set netlist_name "
        f"[file tail [file rootname [xschem get current_name]]]_magic.spice; "
        f"xschem netlist"
    )
    cmd = [
        "xschem", "-s", "-r", "-x", "-q",
        "--rcfile", str(cfg["sch_dir"] / "xschemrc"),
        "--command", tcl_cmd,
        str(cfg["sch_dir"] / f"{cell}.sch"),
    ]
    rc, output = _run(cmd)
    return rc == 0, output


def run_klayout_lvs(cell: str, cfg: dict) -> tuple:
    """Export CDL netlist via Xschem, then run KLayout LVS and check the log."""
    # Step 1: netlist export
    passed, output = run_klayout_lvs_netlist(cell, cfg)
    if not passed:
        return False, f"[klayout-lvs-netlist step failed]\n{output}"

    cfg["lvs_rpt_dir"].mkdir(parents=True, exist_ok=True)
    cfg["net_lay_dir"].mkdir(parents=True, exist_ok=True)

    # Step 2: run KLayout LVS
    run_lvs = cfg["pdk_root"] / cfg["pdk"] / "libs.tech/klayout/tech/lvs/run_lvs.py"
    cmd = [
        "python3", str(run_lvs),
        f"--layout={cfg['gds_dir'] / cell}.gds",
        f"--netlist={cfg['net_sch_dir'] / cell}_klayout.cdl",
        f"--topcell={cell}",
        f"--run_dir={cfg['lvs_rpt_dir']}",
        "--run_mode=deep",
    ]
    rc, output = _run(cmd)

    # Step 3: move extracted netlist (ignore if absent)
    extracted = cfg["lvs_rpt_dir"] / f"{cell}_extracted.cir"
    if extracted.exists():
        shutil.move(str(extracted), str(cfg["net_lay_dir"] / f"{cell}_klayout.cir"))

    # Step 4: check exit code, then confirm match string in log
    if rc != 0:
        return False, output

    log_file = cfg["lvs_rpt_dir"] / f"{cell}.log"
    if not log_file.exists():
        return False, output + "\n[No LVS log file produced]"

    log_text = log_file.read_text(errors="replace")
    output += log_text
    if "Congratulations! Netlists match" not in log_text:
        return False, output + "\n[LVS log does not contain 'Congratulations! Netlists match']"

    return True, output


def run_magic_lvs(cell: str, cfg: dict) -> tuple:
    """Run Magic + Netgen LVS via sak-lvs.sh (handles netlist export internally)."""
    cfg["lvs_rpt_dir"].mkdir(parents=True, exist_ok=True)
    cfg["net_lay_dir"].mkdir(parents=True, exist_ok=True)

    cmd = [
        "sak-lvs.sh", "-d",
        "-w", str(cfg["lvs_rpt_dir"]),
        "-s", str(cfg["sch_dir"] / f"{cell}.sch"),
        "-l", str(cfg["gds_dir"] / f"{cell}.gds"),
        "-c", cell,
    ]
    rc, output = _run(cmd)

    # Move extracted netlist
    ext_spc = cfg["lvs_rpt_dir"] / f"{cell}.ext.spc"
    if ext_spc.exists():
        shutil.move(str(ext_spc), str(cfg["net_lay_dir"] / f"{cell}_magic.ext.spc"))

    # Cleanup intermediate files
    for name in (f"{cell}.sch.spc", f"ext_{cell}.tcl"):
        (cfg["lvs_rpt_dir"] / name).unlink(missing_ok=True)
    for ext_file in cfg["lvs_rpt_dir"].glob("*.ext"):
        ext_file.unlink(missing_ok=True)

    return rc == 0, output


def run_klayout_drc(cell: str, cfg: dict) -> tuple:
    """Run KLayout DRC via run_drc.py."""
    cfg["drc_rpt_dir"].mkdir(parents=True, exist_ok=True)

    run_drc = cfg["pdk_root"] / cfg["pdk"] / "libs.tech/klayout/tech/drc/run_drc.py"
    cmd = [
        "python3", str(run_drc),
        f"--path={cfg['gds_dir'] / cell}.gds",
        f"--topcell={cell}",
        f"--run_dir={cfg['drc_rpt_dir']}",
        "--no_feol",
        "--no_density",
    ]
    rc, output = _run(cmd)
    return rc == 0, output


def run_magic_drc(cell: str, cfg: dict) -> tuple:
    """Run Magic DRC via sak-drc.sh."""
    cfg["drc_rpt_dir"].mkdir(parents=True, exist_ok=True)

    cmd = [
        "sak-drc.sh", "-d", "-m", "-f", "*",
        "-w", str(cfg["drc_rpt_dir"]),
        str(cfg["gds_dir"] / f"{cell}.gds"),
        cell,
    ]
    rc, output = _run(cmd)

    # Cleanup intermediate TCL file
    (cfg["drc_rpt_dir"] / f"drc_{cell}.tcl").unlink(missing_ok=True)

    return rc == 0, output


TOOL_RUNNERS = {
    "klayout-lvs-netlist": run_klayout_lvs_netlist,
    "magic-lvs-netlist":   run_magic_lvs_netlist,
    "klayout-lvs":         run_klayout_lvs,
    "magic-lvs":           run_magic_lvs,
    "klayout-drc":         run_klayout_drc,
    "magic-drc":           run_magic_drc,
}


# ---------------------------------------------------------------------------
# Cell discovery
# ---------------------------------------------------------------------------

def discover_cells(gds_dir: Path) -> list:
    gds_files = sorted(gds_dir.glob("*.gds"))
    if not gds_files:
        logging.error(f"No .gds files found in {gds_dir}")
        sys.exit(1)
    cells = [f.stem for f in gds_files]
    logging.info(f"Discovered {len(cells)} cells: {', '.join(cells)}")
    return cells


# ---------------------------------------------------------------------------
# Regression loop + results
# ---------------------------------------------------------------------------

def run_regression(cfg: dict, tools: list, cells: list, results_dir: Path) -> bool:
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = results_dir / f"regression_results_{timestamp}.csv"
    latest_csv = results_dir / "regression_results_latest.csv"

    rows = []
    any_failure = False
    total = len(cells) * len(tools)
    done = 0

    for cell in cells:
        for tool in tools:
            done += 1
            logging.info(f"[{done}/{total}] {tool} :: {cell}")
            t0 = time.monotonic()
            passed, output = TOOL_RUNNERS[tool](cell, cfg)
            duration = time.monotonic() - t0
            status = "PASSED" if passed else "FAILED"

            if not passed:
                any_failure = True
                logging.error(f"  FAILED: {cell} [{tool}] ({duration:.1f}s)")
                for line in output.splitlines():
                    logging.error(f"    {line}")
            else:
                logging.info(f"  PASSED: {cell} [{tool}] ({duration:.1f}s)")

            rows.append({
                "cell":       cell,
                "tool":       tool,
                "status":     status,
                "duration_s": f"{duration:.2f}",
            })

    # Write timestamped CSV and a stable "latest" symlink-equivalent copy
    fieldnames = ["cell", "tool", "status", "duration_s"]
    for path in (csv_path, latest_csv):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    logging.info(f"Results written to {csv_path}")

    # Summary
    passed_count = sum(1 for r in rows if r["status"] == "PASSED")
    failed_count = len(rows) - passed_count

    logging.info("")
    logging.info("=" * 60)
    logging.info(f"  REGRESSION SUMMARY  {timestamp}")
    logging.info("=" * 60)
    logging.info(f"  Tools  : {', '.join(tools)}")
    logging.info(f"  Total  : {len(rows)}")
    logging.info(f"  Passed : {passed_count}")
    logging.info(f"  Failed : {failed_count}")
    if any_failure:
        logging.info("")
        logging.info("  Failed checks:")
        for r in rows:
            if r["status"] == "FAILED":
                logging.info(f"    - {r['cell']} [{r['tool']}]")
    logging.info("=" * 60)

    return not any_failure


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    parser = argparse.ArgumentParser(
        description="LVS/DRC regression runner for IHP-Open-PDK testbenches.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available tools: {', '.join(VALID_TOOLS)}",
    )
    parser.add_argument(
        "--tools",
        nargs="+",
        choices=VALID_TOOLS,
        required=True,
        metavar="TOOL",
        help="One or more tools to run per cell.",
    )
    parser.add_argument(
        "--cell",
        default=None,
        help="Run on a single named cell only (default: all cells in gds/).",
    )
    parser.add_argument(
        "--ev-precision",
        type=int,
        default=5,
        help="Significant digits for Xschem ev function (default: 5).",
    )
    parser.add_argument(
        "--results-dir",
        default="verification/regression",
        help="Directory for CSV output (default: verification/regression).",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent.resolve()
    cfg = build_config(base_dir, args.ev_precision)
    results_dir = base_dir / args.results_dir

    if args.cell:
        gds_file = cfg["gds_dir"] / f"{args.cell}.gds"
        if not gds_file.is_file():
            logging.error(f"GDS file not found: {gds_file}")
            sys.exit(1)
        cells = [args.cell]
    else:
        cells = discover_cells(cfg["gds_dir"])

    logging.info(f"Tools    : {', '.join(args.tools)}")
    logging.info(f"Cells    : {len(cells)}")
    logging.info(f"Base dir : {base_dir}")

    all_passed = run_regression(cfg, args.tools, cells, results_dir)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
