"""Build the --flatten_cells patch as a real unified diff against the PDK."""
import pathlib, shutil, subprocess, sys, os

PDK = pathlib.Path("/foss/pdks/ihp-sg13g2/libs.tech/klayout/tech/lvs")
WORK = pathlib.Path("/tmp/lvs_patch_build")
OUT = pathlib.Path("/foss/designs/ihp-open-pdk-regression/lvs_patches")

shutil.rmtree(WORK, ignore_errors=True)
(WORK / "a").mkdir(parents=True)
(WORK / "b").mkdir(parents=True)
for f in ("sg13g2.lvs", "run_lvs.py"):
    shutil.copy2(PDK / f, WORK / "a" / f)
    shutil.copy2(PDK / f, WORK / "b" / f)


def edit(path, anchor, insert, where="after", count=1):
    text = path.read_text()
    if text.count(anchor) != count:
        sys.exit(f"{path.name}: anchor found {text.count(anchor)}x, expected {count}:\n{anchor!r}")
    repl = anchor + insert if where == "after" else insert + anchor
    path.write_text(text.replace(anchor, repl, 1))


lvs = WORK / "b" / "sg13g2.lvs"
run = WORK / "b" / "run_lvs.py"

edit(lvs,
     """logger.info("Selected IMPLICIT_NETS option: #{IMPLICIT_NETS.empty? ? '(none)' : IMPLICIT_NETS}")\n""",
     """
# FLATTEN_CELLS
FLATTEN_CELLS = ($flatten_cells || '').to_s.strip

logger.info("Selected FLATTEN_CELLS option: #{FLATTEN_CELLS.empty? ? '(none)' : FLATTEN_CELLS}")
""")

edit(lvs, "  #=== NETLIST OPTIONS ===\n", """  #=== FLATTEN CELLS ===
  # Some library cells tie their parallel devices together with metal drawn in
  # the PARENT cell rather than inside the cell itself. Extraction then pushes
  # every finger out as its own pin (pad, pad$1 ... pad$21) while the schematic
  # models that net as internal to the cell, so those circuits can never match.
  # Flattening them on BOTH sides removes the disagreement and leaves the rest
  # of the comparison intact.
  if !FLATTEN_CELLS.empty?
    cells_to_flatten = FLATTEN_CELLS.split(',').map(&:strip).reject(&:empty?)
    if cells_to_flatten.empty?
      logger.info('WARNING : FLATTEN_CELLS was set but no valid entries were found after parsing.')
    else
      logger.info("Flattening circuits in both netlists: #{cells_to_flatten.join(', ')}")
      cells_to_flatten.each do |cell_pattern|
        netlist.flatten_circuit(cell_pattern)
        schematic.flatten_circuit(cell_pattern)
      end
    end
  end

""", where="before")

edit(run, "               [--implicit_nets=<nets>]\n",
     "               [--flatten_cells=<cells>]\n")

edit(run,
     """        "implicit_nets": f'"{args.implicit_nets}"' if args.implicit_nets else '""',\n""",
     """        "flatten_cells": f'"{args.flatten_cells}"' if args.flatten_cells else '""',\n""")

edit(run, """    parser.add_argument(
        "--ignore_top_ports_mismatch",""",
     '''    parser.add_argument(
        "--flatten_cells",
        type=str,
        default=None,
        help=(
            "Comma-separated circuit names/patterns (glob) to flatten in BOTH "
            'netlists before comparison, e.g. "sg13g2_DCNDiode,sg13g2_Clamp_*". '
            "Use for library cells whose parallel devices are tied together only "
            "by metal in the parent cell."
        ),
    )
''', where="before")

OUT.mkdir(exist_ok=True)
patch = OUT / "flatten_cells.patch"
os.chdir(WORK)
diff = subprocess.run(["diff", "-u", "-r", "a", "b"], capture_output=True, text=True)
if diff.returncode != 1:
    sys.exit(f"unexpected diff status {diff.returncode}: {diff.stderr}")
patch.write_text(diff.stdout)
print(f"wrote {patch} ({len(diff.stdout.splitlines())} lines)")
print(diff.stdout)
