# IO pad LVS sweep

- date: 2026-08-03 15:31:49 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `flat`
- netlists: `netlist/pads_flat`
- extra args: `--disable_tap_extraction`
- result: **0 pass, 1 fail, 0 error/skip** of 1

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadVdd | FAIL | 35.706 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 15:31:47 +0200: Memory Usage (480796K) : ERROR : Netlists don't match
 ==============================================================================
```

