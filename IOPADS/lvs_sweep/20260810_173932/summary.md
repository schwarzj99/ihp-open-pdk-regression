# IO pad LVS sweep

- date: 2026-08-10 17:41:29 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 6.779 |  |
| sg13g2_IOPadIn | PASS | 8.584 |  |
| sg13g2_IOPadInOut16mA | PASS | 7.554 |  |
| sg13g2_IOPadInOut30mA | PASS | 7.784 |  |
| sg13g2_IOPadInOut4mA | PASS | 8.577 |  |
| sg13g2_IOPadIOVdd | PASS | 6.326 |  |
| sg13g2_IOPadIOVss | PASS | 8.981 |  |
| sg13g2_IOPadOut16mA | PASS | 6.736 |  |
| sg13g2_IOPadOut30mA | PASS | 7.121 |  |
| sg13g2_IOPadOut4mA | PASS | 7.038 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.393 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.4 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.03 |  |
| sg13g2_IOPadVdd | PASS | 6.612 |  |
| sg13g2_IOPadVss | PASS | 7.909 |  |

## Per-pad output

### sg13g2_IOPadAnalog (PASS)

```
```

### sg13g2_IOPadIn (PASS)

```
```

### sg13g2_IOPadInOut16mA (PASS)

```
```

### sg13g2_IOPadInOut30mA (PASS)

```
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

