# IO pad LVS sweep

- date: 2026-08-11 13:43:38 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_upstream`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **9 pass, 6 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 9.047 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | PASS | 12.805 |  |
| sg13g2_IOPadInOut16mA | PASS | 10.259 |  |
| sg13g2_IOPadInOut30mA | FAIL | 7.569 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | PASS | 10.962 |  |
| sg13g2_IOPadIOVdd | FAIL | 10.342 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | PASS | 8.032 |  |
| sg13g2_IOPadOut16mA | PASS | 6.659 |  |
| sg13g2_IOPadOut30mA | FAIL | 6.958 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | PASS | 10.545 |  |
| sg13g2_IOPadTriOut16mA | PASS | 11.259 |  |
| sg13g2_IOPadTriOut30mA | FAIL | 7.658 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut4mA | PASS | 7.314 |  |
| sg13g2_IOPadVdd | FAIL | 6.201 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | PASS | 7.107 |  |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-11 13:41:29 +0200: Memory Usage (488556K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (PASS)

```
```

### sg13g2_IOPadInOut16mA (PASS)

```
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-11 13:42:01 +0200: Memory Usage (492320K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (PASS)

```
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-11 13:42:22 +0200: Memory Usage (487868K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (PASS)

```
```

### sg13g2_IOPadOut16mA (PASS)

```
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-11 13:42:45 +0200: Memory Usage (487316K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut4mA (PASS)

```
```

### sg13g2_IOPadTriOut16mA (PASS)

```
```

### sg13g2_IOPadTriOut30mA (FAIL)

```
 Key errors:
   - 2026-08-11 13:43:16 +0200: Memory Usage (494076K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut4mA (PASS)

```
```

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-11 13:43:30 +0200: Memory Usage (489812K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (PASS)

```
```

