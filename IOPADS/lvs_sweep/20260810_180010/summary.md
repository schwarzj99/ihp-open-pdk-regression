# IO pad LVS sweep

- date: 2026-08-10 18:02:44 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 8.35 |  |
| sg13g2_IOPadIn | PASS | 9.418 |  |
| sg13g2_IOPadInOut16mA | PASS | 8.566 |  |
| sg13g2_IOPadInOut30mA | PASS | 11.885 |  |
| sg13g2_IOPadInOut4mA | PASS | 11.375 |  |
| sg13g2_IOPadIOVdd | PASS | 8.172 |  |
| sg13g2_IOPadIOVss | PASS | 10.928 |  |
| sg13g2_IOPadOut16mA | PASS | 14.194 |  |
| sg13g2_IOPadOut30mA | PASS | 11.058 |  |
| sg13g2_IOPadOut4mA | PASS | 8.684 |  |
| sg13g2_IOPadTriOut16mA | PASS | 8.711 |  |
| sg13g2_IOPadTriOut30mA | PASS | 13.778 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.175 |  |
| sg13g2_IOPadVdd | PASS | 6.964 |  |
| sg13g2_IOPadVss | PASS | 9.045 |  |

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

