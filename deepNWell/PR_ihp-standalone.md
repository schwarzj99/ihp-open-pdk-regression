Title:
LVS: connect isolbox n-tub to its contacted guard ring

---

## Problem

The isolbox `I` terminal (the nBuLay tub) can never be named. It always extracts as an
anonymous net, so a design that biases its tub through a guard ring and declares it as a
top-level port cannot pass LVS.

## Root cause

The isolbox PCell paints `Recog/diode` (99/31) over the whole NWell ring, and both tap
derivations subtract that layer:

```ruby
# general_derivations.lvs
ntap         = nactiv.and(nwell_drw).not(ntap1_mk).not(recog_diode).not(gatpoly)
# tap_derivations.lvs
taps_exclude = ....join(recog_diode)
ntap1_exc    = pwell.join(psd_drw).join(taps_exclude)
```

So a *contacted* isolbox guard ring forms no tap at all. Its Activ/Cont/Metal1 lands on a
device-less net, which `simplify` then deletes along with any label placed on it. The `I`
terminal is left holding nBuLay-derived geometry only, and since there is no nbulay text
layer, nothing can ever name it.

## Fix

Derive the n+ ring inside the isolbox NWell ring and tie it to the `I` terminal — 5 added
lines, nothing removed:

```ruby
# diode_derivations.lvs
isolbox_tie = nact_nwell.and(recog_diode).interacting(isolbox_recog)

# diode_connections.lvs
connect(isolbox_i, isolbox_tie)
connect(isolbox_tie, cont_drw)
```

Scoping the derivation with `recog_diode` confines it to the isolbox ring, so an `ntap1`
placed inside the tub stays a separate net.

## Testcase

`sg13_dnwell_inv` in `unit/diode_devices` — a deep-nwell isolated inverter. The NMOS sits in
the isolated pwell with its bulk on the source; the PMOS well sits on the nBuLay and is
therefore at the tub potential. Per DRC rule `NBL.d` (min. PWell width between nBuLay and
NWell, *different net*, 2.2 µm) an NWell on nBuLay is necessarily the same net as the tub,
so the PMOS bulk cannot be at any other potential.

It runs on default switches — no yaml overrides — and **it gates this fix**. Without
`isolbox_tie` the ring Metal1 is deleted as dangling, taking the `VDD` label with it, so
both the isolbox `I` terminal and the `ntap1` tie lose their name and the comparison fails
outright rather than only on the port check:

| | strict | with `--ignore_top_ports_mismatch` |
|---|---|---|
| before this PR | FAIL | **FAIL** |
| with this PR | PASS | **PASS** |

The second column matters because `run_regression.py` appends `--ignore_top_ports_mismatch`
to every run, so a port-only failure would not be observable from the suite. This case fails
on the netlist itself, so it goes red in CI without the fix.

## Testing

- `run_regression.py` unit suite: **all testcases passed, 0 failures**, before and after.
- `testcases/sg13g2_cells` (80 variants, run manually since that directory has no harness):
  76 pass / 4 fail, **identical** before and after. Those 4 failures are pre-existing and may
  simply need switches my ad-hoc runner did not supply.

## Known limitation, deliberately out of scope

The deck has no `connect(nwell_drw, nbulay_drw)`, so it cannot see an NWell-on-nBuLay short.
Magic models this — `ihp-sg13g2.tech` puts `nwell`, `dnwell` and `isolbox` in a single
connectivity group — and `NBL.d` implies the same. I hit it on a real design: Magic reported
the tub merged with the PMOS well, KLayout did not. Adding that connect reproduces Magic's
extraction exactly, but it changes extraction for every isolated structure (`nwell_iso` feeds
bjt, esd and varicap), so it belongs in its own PR with its own regression analysis.

Related: `NBL.b`–`NBL.f` are documented in the DRC rule tables but not implemented in the
KLayout DRC deck — only `NBL.a` exists. `NBL.d` is precisely the rule that would flag an
independently-biased NWell inside a tub.
