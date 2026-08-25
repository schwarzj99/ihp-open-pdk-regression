# IO pad LVS sweep

- date: 2026-08-03 18:06:45 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_dev`
- extra args: `--combine_devices --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode --flatten_cells=sg13g2_GuardRing_*`
- result: **0 pass, 15 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 6.977 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 8.541 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 8.39 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 7.872 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 8.451 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | FAIL | 6.453 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | FAIL | 10.044 | ERROR : Netlists don't match |
| sg13g2_IOPadOut16mA | FAIL | 11.099 | ERROR : Netlists don't match |
| sg13g2_IOPadOut30mA | FAIL | 9.938 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | FAIL | 12.315 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut16mA | FAIL | 8.484 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut30mA | FAIL | 8.699 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut4mA | FAIL | 10.105 | ERROR : Netlists don't match |
| sg13g2_IOPadVdd | FAIL | 9.373 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | FAIL | 9.259 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-03 18:04:30 +0200: Memory Usage (493008K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-03 18:04:39 +0200: Memory Usage (494436K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:04:47 +0200: Memory Usage (488988K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:04:55 +0200: Memory Usage (484464K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:04 +0200: Memory Usage (489820K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:11 +0200: Memory Usage (491440K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:21 +0200: Memory Usage (508336K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:33 +0200: Memory Usage (484300K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:43 +0200: Memory Usage (481424K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:05:56 +0200: Memory Usage (486172K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:06:05 +0200: Memory Usage (493852K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:06:14 +0200: Memory Usage (496152K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 18:06:25 +0200: Memory Usage (485112K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 18:06:34 +0200: Memory Usage (484524K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (FAIL)

```
 Key errors:
   - 2026-08-03 18:06:45 +0200: Memory Usage (502436K) : ERROR : Netlists don't match
 ==============================================================================
```

