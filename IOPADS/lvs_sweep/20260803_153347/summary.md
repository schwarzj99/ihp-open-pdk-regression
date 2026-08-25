# IO pad LVS sweep

- date: 2026-08-03 15:34:13 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads`
- extra args: `--combine_devices --disable_tap_extraction`
- result: **0 pass, 1 fail, 0 error/skip** of 1

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadVdd | FAIL | 22.696 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 15:34:11 +0200: Memory Usage (481260K) : ERROR : Netlists don't match
 ==============================================================================
```

