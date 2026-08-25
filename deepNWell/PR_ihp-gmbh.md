Title:
LVS: connect isolbox n-tub to its contacted guard ring

---

> **⚠️ Depends on #1032 — please merge that first.**
> This branch is based on #1032. The `sg13_dnwell_inv` testcase requires
> `--disable_tap_extraction`, which is introduced there. The first 10 commits in this
> diff belong to #1032 and will disappear once it lands; only the last two are mine.

## Problem

The isolbox `I` terminal (the nBuLay tub) can never be named. It always extracts as an
anonymous `$n` net, so any design that declares the tub as a top-level port fails
`flag_missing_ports`:

```
.SUBCKT test_ptap_dnw_ext D G S VSS          <- no VDD port
D1 S $I3 VSS isolbox                          <- anonymous tub
```

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

`--disable_tap_extraction` does not help here: `ntap1_tie` is already empty on the ring
before that switch is consulted, so the connect it enables has nothing to act on.

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

```
.SUBCKT test_ptap_dnw_ext D G S VDD VSS      <- VDD port present
D1 S VDD VSS isolbox                          <- tub resolves
```

## Testing

| Check | Result |
|---|---|
| `run_regression.py` unit suite | all pass, before and after |
| `testcases/sg13g2_cells` (80 variants, run manually) | 76 pass / 4 fail, **identical** before and after |
| `test_ptap_dnw_ext`, strict (no `--ignore_top_ports_mismatch`) | FAIL before, **PASS** after |
| `sg13_dnwell_inv`, strict | FAIL before, **PASS** after |

The 4 `sg13g2_cells` failures are pre-existing and unchanged by this PR. That directory has
no automated harness, so they may simply need switches my ad-hoc runner did not supply.

## Also in this PR

`sg13_dnwell_inv` — a deep-nwell isolated inverter added to `unit/diode_devices`. It
complements `test_ptap_dnw_ext` (isolated NMOS) by covering a **PMOS inside the tub**, whose
well sits on the nBuLay and is therefore biased to VDD through the guard ring. Per DRC rule
`NBL.d` (min. PWell width between nBuLay and NWell, *different net*, 2.2 µm), an NWell
sitting on nBuLay is necessarily the same net as the tub, so the PMOS bulk cannot be at any
other potential.

The comment in `test_ptap_dnw_ext.yaml` is corrected. It attributed the strict-mode failure
to "the isolation nwell ring is not biased to VDD" — but the ring *is* contacted; the deck
simply had no path from that n+ ring to the `I` terminal.

## Known limitations, deliberately out of scope

1. **This is not yet observable from the suite.** `run_regression.py` appends
   `--ignore_top_ports_mismatch` to every run unconditionally, so the strict path has to be
   exercised by calling `run_lvs.py` directly. Making it yaml-driven would require adding
   the switch to every existing testcase — all 45 fail without it, including
   `sg13_lv_nmos`, because the unit fixtures carry no port labels. Worth a separate PR.

2. **The deck still cannot see an NWell-on-nBuLay short.** There is no
   `connect(nwell_drw, nbulay_drw)`. Magic models it — `ihp-sg13g2.tech` puts
   `nwell`, `dnwell` and `isolbox` in a single connectivity group — and `NBL.d` implies the
   same. Adding that connect reproduces Magic's extraction exactly, but it changes
   extraction for every isolated structure (`nwell_iso` feeds bjt, esd and varicap), so it
   belongs in its own PR with its own regression analysis.

3. **`NBL.b`–`NBL.f` are documented but not implemented** in the KLayout DRC deck — only
   `NBL.a` exists. `NBL.d` is precisely the rule that would flag an independently-biased
   NWell inside a tub.
