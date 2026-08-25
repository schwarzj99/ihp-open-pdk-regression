#!/usr/bin/env bash
#
# Rebuild everything from the shipped netlist and GDS, then check all 15 IO
# pads are LVS clean. Run INSIDE the IIC-OSIC-TOOLS container:
#
#   bash /foss/designs/ihp-open-pdk-regression/IOPADS/verify.sh
#
# Reads only sg13g2_io.spi and sg13g2_io.gds; every output is a new file.
# Neither shipped file is modified. Takes roughly 3 minutes.
#
#   --quick   skip the rebuild, just re-check the newest sweep

set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 1

SWITCHES=(--combine_devices --ignore_top_ports_mismatch
          --implicit_nets='iovss,iovdd,vss,vdd,pad,cathode,anode')

if [ "${1:-}" != "--quick" ]; then
  echo "=== 1/5  netlist: X-style device calls -> D/M/R elements"
  python3 convert_netlist.py || exit 1

  echo; echo "=== 2/5  netlist: substrate net, ptap1 taps, wiring fixes"
  python3 add_taps.py || exit 1

  echo; echo "=== 3/5  layout: add the missing PolyRes markers"
  python3 fix_polyres_marker.py || exit 1

  echo; echo "=== 4/5  cut the pads out, hierarchy intact, and split the netlist"
  python3 extract_pads.py layout/sg13g2_io_polyres.gds | tail -3 || exit 1
  python3 split_pads.py netlist/sg13g2_io_sub.spi netlist/pads_sub | tail -2 || exit 1

  echo; echo "=== 5/5  LVS sweep"
  NETLISTS=pads_sub bash run_lvs_sweep.sh "${SWITCHES[@]}" | tail -20
fi

sweep="lvs_sweep/$(ls -1 lvs_sweep 2>/dev/null | sort | tail -1)"
[ -d "$sweep" ] || { echo "no sweep directory found" >&2; exit 1; }

# ---- independent check, not trusting the sweep's own tally ---------------
# run_lvs.py reports PASS even when it aborted before comparing, so require
# the explicit signature AND zero errors AND zero warnings for every pad.
echo
echo "================================================================="
echo "verifying $sweep"
echo
ok=0; bad=0
for d in "$sweep"/*/; do
  p="$(basename "$d")"
  [ -f "$d/run.log" ] || continue
  sig=$(grep -c 'Comparison mode: PASS (netlists match)' "$d/run.log")
  err=$(sed -n 's/.*| Errors *| *\([0-9]*\).*/\1/p' "$d/run.log" | head -1)
  wrn=$(sed -n 's/.*| Warnings *| *\([0-9]*\).*/\1/p' "$d/run.log" | head -1)
  if [ "$sig" = 1 ] && [ "${err:-x}" = 0 ] && [ "${wrn:-x}" = 0 ]; then
    ok=$((ok + 1))
    printf '  %-26s PASS\n' "$p"
  else
    bad=$((bad + 1))
    printf '  %-26s FAIL  (signature=%s errors=%s warnings=%s)\n' \
           "$p" "$sig" "${err:-?}" "${wrn:-?}"
    echo "        python3 lvs_report.py $d -v     # names the failing circuit"
  fi
done

echo
printf 'genuine passes %d   failures %d\n' "$ok" "$bad"
[ "$ok" = 15 ] && [ "$bad" = 0 ] && echo "ALL 15 IO PADS ARE LVS CLEAN"
[ "$bad" -eq 0 ]
