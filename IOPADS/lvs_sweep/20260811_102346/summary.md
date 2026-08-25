# IO pad LVS sweep

- date: 2026-08-11 10:25:26 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 6.337 |  |
| sg13g2_IOPadIn | PASS | 6.406 |  |
| sg13g2_IOPadInOut16mA | PASS | 6.52 |  |
| sg13g2_IOPadInOut30mA | PASS | 6.293 |  |
| sg13g2_IOPadInOut4mA | PASS | 6.101 |  |
| sg13g2_IOPadIOVdd | PASS | 5.617 |  |
| sg13g2_IOPadIOVss | PASS | 7.563 |  |
| sg13g2_IOPadOut16mA | PASS | 5.872 |  |
| sg13g2_IOPadOut30mA | PASS | 6.651 |  |
| sg13g2_IOPadOut4mA | PASS | 6.161 |  |
| sg13g2_IOPadTriOut16mA | PASS | 6.117 |  |
| sg13g2_IOPadTriOut30mA | PASS | 6.575 |  |
| sg13g2_IOPadTriOut4mA | PASS | 6.279 |  |
| sg13g2_IOPadVdd | PASS | 5.543 |  |
| sg13g2_IOPadVss | PASS | 8.328 |  |

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

