# IO pad LVS sweep

- date: 2026-08-10 17:01:53 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **11 pass, 4 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 7.72 |  |
| sg13g2_IOPadIn | FAIL | 8.339 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 7.749 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 7.773 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 7.662 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | PASS | 6.248 |  |
| sg13g2_IOPadIOVss | PASS | 8.485 |  |
| sg13g2_IOPadOut16mA | PASS | 7.03 |  |
| sg13g2_IOPadOut30mA | PASS | 7.306 |  |
| sg13g2_IOPadOut4mA | PASS | 7.49 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.03 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.426 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.037 |  |
| sg13g2_IOPadVdd | PASS | 6.765 |  |
| sg13g2_IOPadVss | PASS | 8.158 |  |

## Per-pad output

### sg13g2_IOPadAnalog (PASS)

```
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-10 17:00:12 +0200: Memory Usage (493840K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-10 17:00:20 +0200: Memory Usage (488748K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 17:00:28 +0200: Memory Usage (489808K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-10 17:00:36 +0200: Memory Usage (491724K) : ERROR : Netlists don't match
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

### sg13g2_IOPadOut30mA (PASS)

```
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

