# IO pad LVS sweep

- date: 2026-08-03 15:45:24 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads`
- extra args: `--combine_devices --implicit_nets=iovss,iovdd,vss,vdd --flatten_cells=sg13g2_DCNDiode,sg13g2_DCPDiode,sg13g2_Clamp_*,sg13g2_RCClamp*,sg13g2_GuardRing_*`
- result: **0 pass, 1 fail, 0 error/skip** of 1

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadVdd | FAIL | 6.179 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 15:45:23 +0200: Memory Usage (491456K) : ERROR : Netlists don't match
 ==============================================================================
```

