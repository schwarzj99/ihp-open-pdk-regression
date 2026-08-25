#!/usr/bin/env bash
#
# Same as verify.sh, but built from the CURRENT UPSTREAM netlist instead of the
# locally edited copy in netlist/sg13g2_io.spi. Run INSIDE the container:
#
#   bash /foss/designs/ihp-open-pdk-regression/IOPADS/verify_upstream.sh
#
# Why this exists: netlist/sg13g2_io.spi was edited by hand months ago and no
# longer matches the xschem symbols for 7 of the 15 pads, so it cannot be
# simulated. The upstream netlist matches all 15. This checks that the same
# three-script pipeline takes the upstream netlist to LVS clean too, which is
# what makes the fixes worth sending upstream rather than keeping local.
#
# Reads the upstream netlist and layout/sg13g2_io.gds; writes only new files.
#
#   --quick   skip the rebuild, just re-check the newest sweep

set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 1

UPSTREAM=${UPSTREAM:-/foss/designs/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi}
SWITCHES=(--combine_devices --ignore_top_ports_mismatch
          --implicit_nets='iovss,iovdd,vss,vdd,pad,cathode,anode')

if [ "${1:-}" != "--quick" ]; then
  [ -f "$UPSTREAM" ] || { echo "no upstream netlist at $UPSTREAM" >&2; exit 1; }

  echo "=== 0/5  upstream netlist, with sub! renamed to the sub node we declare"
  # add_taps.py declares .GLOBAL sub; upstream spells the same node sub!.
  # Left alone they would be two separate substrate nets.
  sed 's/\bsub!/sub/g' "$UPSTREAM" > netlist/sg13g2_io_upstream.spi || exit 1
  printf '    %s -> netlist/sg13g2_io_upstream.spi (%s sub! occurrences)\n' \
         "$UPSTREAM" "$(grep -c 'sub!' "$UPSTREAM")"

  echo; echo "=== 1/5  netlist: X-style device calls -> D/M/R elements"
  python3 convert_netlist.py netlist/sg13g2_io_upstream.spi \
                             netlist/sg13g2_io_upstream_devices.spi || exit 1

  echo; echo "=== 2/5  netlist: substrate net, ptap1 taps, wiring fixes"
  python3 add_taps.py netlist/sg13g2_io_upstream_devices.spi \
                      netlist/sg13g2_io_upstream_sub.spi || exit 1

  echo; echo "=== 3/5  layout: add the missing PolyRes markers"
  python3 fix_polyres_marker.py || exit 1

  echo; echo "=== 4/5  cut the pads out, hierarchy intact, and split the netlist"
  python3 extract_pads.py layout/sg13g2_io_polyres.gds | tail -3 || exit 1
  python3 split_pads.py netlist/sg13g2_io_upstream_sub.spi netlist/pads_upstream | tail -2 || exit 1

  echo; echo "=== 5/5  LVS sweep"
  NETLISTS=pads_upstream bash run_lvs_sweep.sh "${SWITCHES[@]}" | tail -20
fi

sweep="lvs_sweep/$(ls -1 lvs_sweep 2>/dev/null | sort | tail -1)"
[ -d "$sweep" ] || { echo "no sweep directory found" >&2; exit 1; }

# ---- independent check, straight from the .lvsdb ------------------------
# run_lvs.py reports PASS even when it aborted before comparing, so ask
# KLayout's own cross-reference instead of parsing the log.
echo
echo "================================================================="
echo "verifying $sweep"
echo
ok=0; bad=0
for d in "$sweep"/*/; do
  p="$(basename "$d")"
  if python3 lvs_check.py "$d" --topcell "$p" -q 2>/dev/null; then
    ok=$((ok + 1)); printf '  %-26s PASS\n' "$p"
  else
    bad=$((bad + 1)); printf '  %-26s FAIL\n' "$p"
    python3 lvs_check.py "$d" --topcell "$p" | sed 's/^/        /'
  fi
done

echo
printf 'genuine passes %d   failures %d\n' "$ok" "$bad"
[ "$ok" = 15 ] && [ "$bad" = 0 ] && echo "ALL 15 IO PADS ARE LVS CLEAN FROM THE UPSTREAM NETLIST"
[ "$bad" -eq 0 ]
