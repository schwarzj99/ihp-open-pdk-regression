# LVS deck patches

Local fixes to the installed SG13G2 KLayout LVS deck.

The PDK lives inside the IIC-OSIC-TOOLS container image, so **these patches die
with the container**. Re-apply after every restart:

```
docker exec -u 0 <container> bash /foss/designs/ihp-open-pdk-regression/lvs_patches/apply.sh
```

Root is needed because `/foss/pdks` is owned by root. Running as a normal user
still reports what is applied, it just cannot change anything.

| | |
|---|---|
| `apply.sh` | applies every patch; idempotent, `--revert` restores originals |
| `regenerate_patch.py` | rebuilds the patch against the current deck (run in-container) |
| `flatten_cells.patch` | adds `--flatten_cells` |

Originals are kept as `<file>.orig` beside the patched files.

## flatten_cells.patch

Adds a `--flatten_cells` option to `run_lvs.py` and the matching
`$flatten_cells` handling to `sg13g2.lvs`. It takes comma-separated glob
patterns and flattens those circuits in **both** netlists after `align` and
before the comparison.

```
run_lvs.py --flatten_cells='sg13g2_DCNDiode,sg13g2_Clamp_*'
```

### Why

Several IHP library cells tie their parallel devices together with metal drawn
in the **parent** cell rather than inside the cell itself. Extraction then
pushes every finger out as its own pin while the shipped netlist models that
net as internal, so the circuits can never match no matter how the layout is
cut out or extracted.

`sg13g2_Clamp_N43N43D4R` is the clearest case: it extracts with 25 pins, `pad`
plus `pad$1` … `pad$21`, one per NMOS finger, and the parent maps all 22 onto
`vdd`. The schematic declares 4 pins with a single internal `pad`.

Flattening those cells on both sides removes the disagreement and leaves the
rest of the comparison untouched. Nothing changes unless the option is passed.

### Status

The patch does its job, verified on `sg13g2_IOPadVdd`: the clamp's 172
schematic fingers of `w=4.4um` combine to exactly the `W=756.8u` the layout
extracts, and the pad drops from 3 circuits to 1.

The IO pads still do **not** pass LVS. The remaining blocker is unrelated to
this patch: guard rings are empty subckts in the netlist but extract as
`ptap1`/`ntap1` devices. See `Findings.md` in the repo root.
