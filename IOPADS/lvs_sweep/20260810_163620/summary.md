# IO pad LVS sweep

- date: 2026-08-10 16:38:23 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **6 pass, 9 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 7.128 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 8.125 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 7.663 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 11.458 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 8.672 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | FAIL | 6.681 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | FAIL | 8.458 | ERROR : Netlists don't match |
| sg13g2_IOPadOut16mA | PASS | 6.764 |  |
| sg13g2_IOPadOut30mA | FAIL | 7.435 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | PASS | 7.644 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.468 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.393 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.524 |  |
| sg13g2_IOPadVdd | FAIL | 7.646 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | PASS | 8.303 |  |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-10 16:36:27 +0200: Memory Usage (500600K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-10 16:36:35 +0200: Memory Usage (499544K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:36:43 +0200: Memory Usage (488644K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:36:55 +0200: Memory Usage (488884K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:37:04 +0200: Memory Usage (488224K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-10 16:37:11 +0200: Memory Usage (491700K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (FAIL)

```
 Key errors:
   - 2026-08-10 16:37:20 +0200: Memory Usage (496196K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut16mA (PASS)

```
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:37:34 +0200: Memory Usage (490516K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut4mA (PASS)

```
```

### sg13g2_IOPadTriOut16mA (PASS)

```
```

### sg13g2_IOPadTriOut30mA (PASS)

```
```

### sg13g2_IOPadTriOut4mA (PASS)

```
```

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-10 16:38:14 +0200: Memory Usage (489976K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (PASS)

```
```

