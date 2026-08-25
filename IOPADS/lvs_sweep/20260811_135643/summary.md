# IO pad LVS sweep

- date: 2026-08-11 13:58:44 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_upstream`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 7.321 |  |
| sg13g2_IOPadIn | PASS | 8.204 |  |
| sg13g2_IOPadInOut16mA | PASS | 7.216 |  |
| sg13g2_IOPadInOut30mA | PASS | 7.679 |  |
| sg13g2_IOPadInOut4mA | PASS | 7.969 |  |
| sg13g2_IOPadIOVdd | PASS | 6.516 |  |
| sg13g2_IOPadIOVss | PASS | 8.07 |  |
| sg13g2_IOPadOut16mA | PASS | 7.687 |  |
| sg13g2_IOPadOut30mA | PASS | 7.257 |  |
| sg13g2_IOPadOut4mA | PASS | 10.637 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.403 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.739 |  |
| sg13g2_IOPadTriOut4mA | PASS | 6.99 |  |
| sg13g2_IOPadVdd | PASS | 6.657 |  |
| sg13g2_IOPadVss | PASS | 8.683 |  |

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

