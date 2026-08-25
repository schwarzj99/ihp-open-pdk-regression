# IO pad LVS sweep

- date: 2026-08-03 14:22:05 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- extra args: `none`
- result: **0 pass, 15 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 7.077 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 8.138 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 7.748 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 8.047 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 8.024 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | FAIL | 7.322 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | FAIL | 10.085 | ERROR : Netlists don't match |
| sg13g2_IOPadOut16mA | FAIL | 7.094 | ERROR : Netlists don't match |
| sg13g2_IOPadOut30mA | FAIL | 14.898 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | FAIL | 12.707 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut16mA | FAIL | 12.233 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut30mA | FAIL | 10.141 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut4mA | FAIL | 11.065 | ERROR : Netlists don't match |
| sg13g2_IOPadVdd | FAIL | 6.232 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | FAIL | 7.883 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-03 14:19:47 +0200: Memory Usage (493024K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-03 14:19:56 +0200: Memory Usage (498492K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:04 +0200: Memory Usage (487060K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:12 +0200: Memory Usage (484700K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:20 +0200: Memory Usage (488052K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:28 +0200: Memory Usage (490084K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:39 +0200: Memory Usage (500048K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:20:46 +0200: Memory Usage (494836K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:01 +0200: Memory Usage (478332K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:14 +0200: Memory Usage (482028K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:27 +0200: Memory Usage (488996K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:37 +0200: Memory Usage (484196K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:50 +0200: Memory Usage (484568K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 14:21:56 +0200: Memory Usage (493604K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (FAIL)

```
 Key errors:
   - 2026-08-03 14:22:04 +0200: Memory Usage (494144K) : ERROR : Netlists don't match
 ==============================================================================
```

