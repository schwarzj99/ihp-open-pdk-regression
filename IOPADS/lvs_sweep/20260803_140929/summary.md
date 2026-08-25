# IO pad LVS sweep

- date: 2026-08-03 14:11:47 +0200
- pdk: `/foss/pdks/ihp-sg13g2`
- run mode: `deep`
- extra args: `none`
- result: **0 pass, 15 fail, 0 error/skip** of 15

| Pad | Status | Time (s) | First error |
|---|---|---|---|
| sg13g2_IOPadAnalog | FAIL | 7.161 | ERROR : Netlists don't match |
| sg13g2_IOPadIn | FAIL | 8.394 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut16mA | FAIL | 7.395 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut30mA | FAIL | 8.089 | ERROR : Netlists don't match |
| sg13g2_IOPadInOut4mA | FAIL | 8.997 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVdd | FAIL | 12.682 | ERROR : Netlists don't match |
| sg13g2_IOPadIOVss | FAIL | 9.116 | ERROR : Netlists don't match |
| sg13g2_IOPadOut16mA | FAIL | 11.49 | ERROR : Netlists don't match |
| sg13g2_IOPadOut30mA | FAIL | 7.924 | ERROR : Netlists don't match |
| sg13g2_IOPadOut4mA | FAIL | 7.734 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut16mA | FAIL | 7.603 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut30mA | FAIL | 8.595 | ERROR : Netlists don't match |
| sg13g2_IOPadTriOut4mA | FAIL | 9.152 | ERROR : Netlists don't match |
| sg13g2_IOPadVdd | FAIL | 9.24 | ERROR : Netlists don't match |
| sg13g2_IOPadVss | FAIL | 9.548 | ERROR : Netlists don't match |

## Per-pad output

### sg13g2_IOPadAnalog (FAIL)

```
 Key errors:
   - 2026-08-03 14:09:36 +0200: Memory Usage (494504K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIn (FAIL)

```
 Key errors:
   - 2026-08-03 14:09:44 +0200: Memory Usage (531868K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:09:52 +0200: Memory Usage (488524K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:01 +0200: Memory Usage (521736K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadInOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:10 +0200: Memory Usage (483416K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVdd (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:23 +0200: Memory Usage (493272K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadIOVss (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:32 +0200: Memory Usage (533052K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:44 +0200: Memory Usage (482400K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:10:52 +0200: Memory Usage (515548K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:00 +0200: Memory Usage (505820K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut16mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:08 +0200: Memory Usage (484556K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut30mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:17 +0200: Memory Usage (507660K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadTriOut4mA (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:27 +0200: Memory Usage (511972K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVdd (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:36 +0200: Memory Usage (496292K) : ERROR : Netlists don't match
 ==============================================================================
```

### sg13g2_IOPadVss (FAIL)

```
 Key errors:
   - 2026-08-03 14:11:47 +0200: Memory Usage (533692K) : ERROR : Netlists don't match
 ==============================================================================
```

