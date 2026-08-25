Title:
LVS: connect isolbox n-tub to its contacted guard ring

---

> **Note on the diff — 4 commits, only 2 are mine.**
> This branch is based on the IHP-GmbH PR #1032 branch rather than on `iic-jku/dev`, because
> the same branch is proposed upstream to IHP-GmbH, where `--disable_tap_extraction` does not
> exist yet. Our `dev` already carries most of #1032's work as different SHAs (via #48), so
> the only foreign commits here are the two that have not reached our `dev` yet:
> `50b6791a` (deep-mode tap extraction testcase) and `07ae6c00` (yaml cleanup), both by
> @simi1505. They are in flight upstream and will fall out of this diff once `dev` catches up.
>
> Unlike the IHP-GmbH PR, this one has **no hard dependency on #1032** — our `dev` already has
> `--disable_tap_extraction`, which is all the new testcase needs.

## Problem

The isolbox `I` terminal (the nBuLay tub) can never be named. It always extracts as an
anonymous `$n` net, so any design that declares the tub as a top-level port fails
`flag_missing_ports`. This is the wall `test_ptap_dnw_ext` hit — its yaml comment records
the symptom.

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
device-less net which `simplify` deletes, along with any label on it. The `I` terminal is
left holding nBuLay geometry only, and there is no nbulay text layer, so nothing can name
it.

Worth flagging for our own flow: **`--disable_tap_extraction` does not help here.**
`ntap1_tie` is already empty on the isolbox ring before that switch is consulted, so the
`connect(ntap1_tie, ntap1_well)` it enables has nothing to act on. The two switches are
orthogonal.

## Fix

5 added lines, nothing removed:

```ruby
# diode_derivations.lvs
isolbox_tie = nact_nwell.and(recog_diode).interacting(isolbox_recog)

# diode_connections.lvs
connect(isolbox_i, isolbox_tie)
connect(isolbox_tie, cont_drw)
```

`recog_diode` scoping confines it to the isolbox ring, so an `ntap1` inside the tub stays a
separate net.

```
before:  .SUBCKT test_ptap_dnw_ext D G S VSS      /  D1 S $I3 VSS isolbox
after:   .SUBCKT test_ptap_dnw_ext D G S VDD VSS  /  D1 S VDD VSS isolbox
```

## Correcting the test_ptap_dnw_ext note

The yaml comment attributed the failure to *"the isolation nwell ring is not biased to
VDD"*. That diagnosis is wrong — the ring **is** contacted. The deck simply had no path
from that n+ ring to the isolbox `I` terminal. With `isolbox_tie` the VDD top port resolves
strictly, and the case no longer depends on `--ignore_top_ports_mismatch` at all.

## New testcase

`sg13_dnwell_inv` in `unit/diode_devices` — a deep-nwell isolated inverter. It complements
`test_ptap_dnw_ext` (isolated NMOS) by covering a **PMOS inside the tub**, whose well sits
on the nBuLay and is therefore biased to VDD through the guard ring. Per DRC rule `NBL.d`
(min. PWell width between nBuLay and NWell, *different net*, 2.2 µm), an NWell on nBuLay is
necessarily the same net as the tub, so the PMOS bulk cannot be at any other potential.

## Testing

| Check | Result |
|---|---|
| `run_regression.py` unit suite | all pass, before and after |
| `testcases/sg13g2_cells` (80 variants, run manually) | 76 pass / 4 fail, **identical** before and after |
| `test_ptap_dnw_ext`, strict | FAIL before, **PASS** after |
| `sg13_dnwell_inv`, strict | FAIL before, **PASS** after |

The 4 `sg13g2_cells` failures are pre-existing and unchanged.

## Two things we should pick up separately

1. **`run_regression.py` forces `--ignore_top_ports_mismatch` on every run** (line ~264),
   so neither testcase can actually gate this in CI — the strict path has to be run by hand.
   Making it yaml-driven means adding the switch to every existing testcase: all 45 fail
   without it, including `sg13_lv_nmos`, because the unit fixtures carry no port labels.

2. **The deck cannot see an NWell-on-nBuLay short.** There is no
   `connect(nwell_drw, nbulay_drw)`. Magic models it (`ihp-sg13g2.tech` puts `nwell`,
   `dnwell` and `isolbox` in one connectivity group) and `NBL.d` implies the same. I hit
   this on a real design: Magic reported the tub merged with the PMOS well, KLayout did not.
   Adding the connect reproduces Magic exactly, but it changes extraction for every isolated
   structure (`nwell_iso` feeds bjt, esd, varicap), so it needs its own PR. Related:
   `NBL.b`–`NBL.f` are documented but not implemented in the DRC deck — only `NBL.a` is.
