# IO pad LVS sweep

- date: 2026-08-11 13:53:44 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_upstream`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 7.383 |  |
| sg13g2_IOPadIn | PASS | 8.159 |  |
| sg13g2_IOPadInOut16mA | PASS | 13.524 |  |
| sg13g2_IOPadInOut30mA | PASS | 18.974 |  |
| sg13g2_IOPadInOut4mA | PASS | 13.34 |  |
| sg13g2_IOPadIOVdd | PASS | 6.082 |  |
| sg13g2_IOPadIOVss | PASS | 7.836 |  |
| sg13g2_IOPadOut16mA | PASS | 11.094 |  |
| sg13g2_IOPadOut30mA | PASS | 9.732 |  |
| sg13g2_IOPadOut4mA | PASS | 8.747 |  |
| sg13g2_IOPadTriOut16mA | PASS | 12.363 |  |
| sg13g2_IOPadTriOut30mA | PASS | 8.581 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.332 |  |
| sg13g2_IOPadVdd | PASS | 6.567 |  |
| sg13g2_IOPadVss | PASS | 12.872 |  |

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

