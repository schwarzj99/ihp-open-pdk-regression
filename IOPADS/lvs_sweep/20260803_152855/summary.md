# IO pad LVS sweep

- date: 2026-08-03 15:29:20 +0200
- pdk: `/foss/pdks/ihp-sg13cmos5l`
- run mode: `flat`
- netlists: `netlist/pads_flat`
- extra args: `--disable_tap_extraction`
- result: **0 pass, 1 fail, 0 error/skip** of 1

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadVdd | FAIL | 23.763 | KLayout run failed with exit code 1. |

## Per-pad output

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - KLayout run failed with exit code 1.
   - KLayout stderr: ERROR: In /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/sg13cmos5l.lvs: CMOS5L forbidden layers detected: Via4 (66/0): 2371 polygons; Metal5 (67/0): 8 polygons; TopVia2 (133/0): 443 polygons; TopMetal2 (134/0): 11 polygons
   - KLayout stderr: ERROR: RuntimeError: CMOS5L forbidden layers detected: Via4 (66/0): 2371 polygons; Metal5 (67/0): 8 polygons; TopVia2 (133/0): 443 polygons; TopMetal2 (134/0): 11 polygons in Executable::execute
 ==============================================================================
```

