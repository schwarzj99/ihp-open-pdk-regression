# IO pad LVS sweep

- date: 2026-08-10 17:37:08 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **13 pass, 2 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 9.144 |  |
| sg13g2_IOPadIn | FAIL | 11.581 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | PASS | 9.714 |  |
| sg13g2_IOPadInOut30mA | FAIL | 9.14 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | PASS | 12.499 |  |
| sg13g2_IOPadIOVdd | PASS | 12.813 |  |
| sg13g2_IOPadIOVss | PASS | 9.57 |  |
| sg13g2_IOPadOut16mA | PASS | 9.948 |  |
| sg13g2_IOPadOut30mA | PASS | 12.172 |  |
| sg13g2_IOPadOut4mA | PASS | 9.392 |  |
| sg13g2_IOPadTriOut16mA | PASS | 10.005 |  |
| sg13g2_IOPadTriOut30mA | PASS | 11.859 |  |
| sg13g2_IOPadTriOut4mA | PASS | 10.108 |  |
| sg13g2_IOPadVdd | PASS | 9.557 |  |
| sg13g2_IOPadVss | PASS | 12.521 |  |

## Per-pad output

### sg13g2_IOPadAnalog (PASS)

```
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-10 17:34:42 +0200: Memory Usage (500288K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (PASS)

```
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 17:35:02 +0200: Memory Usage (492596K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (PASS)

```
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

