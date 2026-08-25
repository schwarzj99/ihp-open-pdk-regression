# IO pad LVS sweep

- date: 2026-08-10 16:45:08 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- netlists: `netlist/pads_sub`
- extra args: `--combine_devices --ignore_top_ports_mismatch --implicit_nets=iovss,iovdd,vss,vdd,pad,cathode,anode`
- result: **6 pass, 9 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 6.857 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 7.306 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 6.911 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 6.879 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 6.801 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | FAIL | 5.926 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | FAIL | 7.346 | ERROR : Netlists don't match |
| sg13g2_IOPadOut16mA | PASS | 6.761 |  |
| sg13g2_IOPadOut30mA | FAIL | 7.185 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | PASS | 6.624 |  |
| sg13g2_IOPadTriOut16mA | PASS | 7.029 |  |
| sg13g2_IOPadTriOut30mA | PASS | 7.777 |  |
| sg13g2_IOPadTriOut4mA | PASS | 7.515 |  |
| sg13g2_IOPadVdd | FAIL | 7.472 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | PASS | 9.956 |  |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:21 +0200: Memory Usage (486932K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:29 +0200: Memory Usage (499204K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:36 +0200: Memory Usage (485328K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:43 +0200: Memory Usage (485180K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:51 +0200: Memory Usage (492196K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-10 16:43:57 +0200: Memory Usage (489768K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (FAIL)

```
 Key errors:
   - 2026-08-10 16:44:04 +0200: Memory Usage (508848K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut16mA (PASS)

```
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-10 16:44:19 +0200: Memory Usage (491684K) : ERROR : Netlists don't match
 ==============================================================================
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

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-10 16:44:57 +0200: Memory Usage (489792K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (PASS)

```
```

