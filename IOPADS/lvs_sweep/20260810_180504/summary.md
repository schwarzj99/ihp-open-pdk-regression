# IO pad LVS sweep

- date: 2026-08-10 18:07:23 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **15 pass, 0 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | PASS | 8.604 |  |
| sg13g2_IOPadIn | PASS | 10.156 |  |
| sg13g2_IOPadInOut16mA | PASS | 8.689 |  |
| sg13g2_IOPadInOut30mA | PASS | 8.564 |  |
| sg13g2_IOPadInOut4mA | PASS | 8.328 |  |
| sg13g2_IOPadIOVdd | PASS | 7.383 |  |
| sg13g2_IOPadIOVss | PASS | 9.423 |  |
| sg13g2_IOPadOut16mA | PASS | 9.214 |  |
| sg13g2_IOPadOut30mA | PASS | 9.356 |  |
| sg13g2_IOPadOut4mA | PASS | 10.523 |  |
| sg13g2_IOPadTriOut16mA | PASS | 9.952 |  |
| sg13g2_IOPadTriOut30mA | PASS | 8.466 |  |
| sg13g2_IOPadTriOut4mA | PASS | 8.693 |  |
| sg13g2_IOPadVdd | PASS | 6.863 |  |
| sg13g2_IOPadVss | PASS | 8.788 |  |

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

