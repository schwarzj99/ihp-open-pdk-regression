# IO pad LVS sweep

- date: 2026-08-11 10:09:34 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 7.048 |  |
| sg13g2_IOPadIn | PASS | 7.815 |  |
| sg13g2_IOPadInOut16mA | PASS | 7.081 |  |
| sg13g2_IOPadInOut30mA | PASS | 7.31 |  |
| sg13g2_IOPadInOut4mA | PASS | 9.198 |  |
| sg13g2_IOPadIOVdd | PASS | 7.401 |  |
| sg13g2_IOPadIOVss | PASS | 12.764 |  |
| sg13g2_IOPadOut16mA | PASS | 17.975 |  |
| sg13g2_IOPadOut30mA | PASS | 15.407 |  |
| sg13g2_IOPadOut4mA | PASS | 9.518 |  |
| sg13g2_IOPadTriOut16mA | PASS | 11.751 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.193 |  |
| sg13g2_IOPadTriOut4mA | PASS | 9.321 |  |
| sg13g2_IOPadVdd | PASS | 6.998 |  |
| sg13g2_IOPadVss | PASS | 8.263 |  |

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

