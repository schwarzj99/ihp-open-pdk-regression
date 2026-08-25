# IO pad LVS sweep

- date: 2026-08-10 16:50:02 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **9 pass, 6 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 7.284 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 7.36 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 7.64 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 8.323 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 8.785 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | PASS | 8.582 |  |
| sg13g2_IOPadIOVss | PASS | 9.765 |  |
| sg13g2_IOPadOut16mA | PASS | 8.495 |  |
| sg13g2_IOPadOut30mA | FAIL | 9.626 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | PASS | 8.259 |  |
| sg13g2_IOPadTriOut16mA | PASS | 8.546 |  |
| sg13g2_IOPadTriOut30mA | PASS | 9.124 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.908 |  |
| sg13g2_IOPadVdd | PASS | 7.084 |  |
| sg13g2_IOPadVss | PASS | 9.141 |  |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-10 16:47:58 +0200: Memory Usage (494340K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-10 16:48:06 +0200: Memory Usage (502704K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:48:13 +0200: Memory Usage (488080K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:48:22 +0200: Memory Usage (485560K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:48:31 +0200: Memory Usage (486972K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (PASS)

```
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
   - 2026-08-10 16:49:09 +0200: Memory Usage (484640K) : ERROR : Netlists don't match
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

### sg13g2_IOPadVdd (PASS)

```
```

### sg13g2_IOPadVss (PASS)

```
```

