# IO pad LVS sweep

- date: 2026-08-11 13:56:07 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 9.879 |  |
| sg13g2_IOPadIn | PASS | 8.516 |  |
| sg13g2_IOPadInOut16mA | PASS | 8.156 |  |
| sg13g2_IOPadInOut30mA | PASS | 8.104 |  |
| sg13g2_IOPadInOut4mA | PASS | 7.845 |  |
| sg13g2_IOPadIOVdd | PASS | 6.552 |  |
| sg13g2_IOPadIOVss | PASS | 8.319 |  |
| sg13g2_IOPadOut16mA | PASS | 7.281 |  |
| sg13g2_IOPadOut30mA | PASS | 7.276 |  |
| sg13g2_IOPadOut4mA | PASS | 6.588 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.04 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.263 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.324 |  |
| sg13g2_IOPadVdd | PASS | 6.199 |  |
| sg13g2_IOPadVss | PASS | 7.684 |  |

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

