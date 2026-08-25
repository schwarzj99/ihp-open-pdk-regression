#!/usr/bin/env bash
#
# Run SG13G2 LVS on every extracted IO pad and collect the results in one table.
#
# Run this INSIDE the IIC-OSIC-TOOLS container:
#   /foss/designs/ihp-open-pdk-regression/IOPADS/run_lvs_sweep.sh
#
# Each pad is matched against its own split netlist in netlist/pads/.
# Failures are expected; the sweep never stops on one, it records it and
# moves on so you get the full picture in a single pass.
#
# Env overrides:
#   RUN_MODE=flat          KLayout run mode (default: deep, matching earlier runs)
#   PADS="a b"             Only run these pads
#   NETLISTS=pads_flat     Netlist dir under netlist/ (default: pads). Use
#                          pads_flat together with RUN_MODE=flat to compare
#                          flat against flat.
#   IOPAD_PDK=/path/to/pdk PDK to check against (default: /foss/pdks/ihp-sg13g2)
# Anything passed as an argument is forwarded verbatim to run_lvs.py, e.g.
#   ./run_lvs_sweep.sh --disable_tap_extraction --ignore_top_ports_mismatch
#
# Note: the default is hard-coded, NOT derived from the container's $PDK /
# $PDK_ROOT. Those are mutable and have been observed pointing at
# ihp-sg13cmos5l mid-session, which silently runs these sg13g2 pads against the
# wrong rule deck. A bare relative $PDK also resolves against the cwd, which is
# how an earlier version of this script ran against /foss/designs/ihp-sg13g2.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IOPAD_PDK="${IOPAD_PDK:-/foss/pdks/ihp-sg13g2}"
LVS="$IOPAD_PDK/libs.tech/klayout/tech/lvs/run_lvs.py"
RUN_MODE="${RUN_MODE:-deep}"
NETLISTS="${NETLISTS:-pads}"

case "$IOPAD_PDK" in
  /*) ;;
  *) echo "IOPAD_PDK must be an absolute path, got '$IOPAD_PDK'" >&2; exit 1 ;;
esac
case "$IOPAD_PDK" in
  /foss/designs/*)
    echo "refusing to use the PDK checkout under /foss/designs ('$IOPAD_PDK')." >&2
    echo "it is stale; use the installed PDK at /foss/pdks/ihp-sg13g2." >&2
    exit 1 ;;
esac
[ -f "$LVS" ] || { echo "run_lvs.py not found at $LVS (set IOPAD_PDK=)" >&2; exit 1; }

TS="$(date +%Y%m%d_%H%M%S)"
SWEEP="$ROOT/lvs_sweep/$TS"
mkdir -p "$SWEEP"

if [ -n "${PADS:-}" ]; then
  read -r -a pads <<< "$PADS"
else
  pads=()
  for g in "$ROOT"/layout/sg13g2_IOPad*.gds; do
    pads+=("$(basename "$g" .gds)")
  done
fi

echo "sweep     : $SWEEP"
echo "pdk       : $IOPAD_PDK"
echo "run mode  : $RUN_MODE"
echo "netlists  : netlist/$NETLISTS"
echo "extra args: ${*:-none}"
echo "pads      : ${#pads[@]}"
echo

declare -a rows=()
n_pass=0; n_fail=0; n_err=0

for pad in "${pads[@]}"; do
  gds="$ROOT/layout/$pad.gds"
  net="$ROOT/netlist/$NETLISTS/$pad.spi"
  dir="$SWEEP/$pad"
  mkdir -p "$dir"

  if [ ! -f "$gds" ] || [ ! -f "$net" ]; then
    printf '%-24s SKIP (missing %s)\n' "$pad" "$([ -f "$gds" ] || echo gds; [ -f "$net" ] || echo netlist)"
    rows+=("$pad|SKIP|-|missing input file")
    n_err=$((n_err + 1))
    continue
  fi

  printf '%-24s ... ' "$pad"
  python3 "$LVS" \
    --layout="$gds" \
    --netlist="$net" \
    --topcell="$pad" \
    --run_mode="$RUN_MODE" \
    --run_dir="$dir" \
    "$@" > "$dir/run.log" 2>&1
  rc=$?

  status="$(sed -n 's/.*| Status *| *\([A-Za-z]*\).*/\1/p' "$dir/run.log" | head -1)"
  rtime="$(sed -n 's/.*| Run Time (s) *| *\([0-9.]*\).*/\1/p' "$dir/run.log" | head -1)"
  errs="$(sed -n 's/.*| Errors *| *\([0-9]*\).*/\1/p' "$dir/run.log" | head -1)"
  [ -n "$status" ] || status="ERROR"
  [ -n "$rtime" ] || rtime="-"
  [ -n "$errs" ] || errs=0

  # run_lvs.py reports PASS even when it never got as far as comparing, so
  # do not take its word for it: a nonzero exit, any logged error, or a
  # missing PASS/FAIL signature all mean the run did not actually clear.
  if [ "$status" = "PASS" ]; then
    if [ "$rc" -ne 0 ] || [ "$errs" -ne 0 ] \
       || grep -q 'no explicit PASS/FAIL signature found' "$dir/run.log"; then
      status="ERROR"
    fi
  fi

  # first key error line, stripped of the logger prefix and memory noise
  note="$(grep -m1 '| ERROR   |   - ' "$dir/run.log" \
          | sed -e 's/.*| ERROR   |   - //' -e 's/^.*Memory Usage ([0-9]*K) : //' \
          | cut -c1-80)"
  if [ -z "$note" ] && [ "$status" != "PASS" ]; then
    note="run_lvs.py exit $rc, see run.log"
  fi

  case "$status" in
    PASS) n_pass=$((n_pass + 1)) ;;
    FAIL) n_fail=$((n_fail + 1)) ;;
    *)    n_err=$((n_err + 1)) ;;
  esac

  echo "$status (${rtime}s) ${note}"
  rows+=("$pad|$status|$rtime|$note")
done

# ---- summary -----------------------------------------------------------
sum="$SWEEP/summary.md"
{
  echo "# IO pad LVS sweep"
  echo
  echo "- date: $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "- pdk: \`$IOPAD_PDK\`"
  echo "- run mode: \`$RUN_MODE\`"
  echo "- netlists: \`netlist/$NETLISTS\`"
  echo "- extra args: \`${*:-none}\`"
  echo "- result: **$n_pass pass, $n_fail fail, $n_err error/skip** of ${#pads[@]}"
  echo
  echo "| Pad | Status | Time (s) | First error |"
  echo "|---|---|---|---|"
  for r in "${rows[@]}"; do
    IFS='|' read -r p s t note <<< "$r"
    echo "| $p | $s | $t | ${note:-} |"
  done
  echo
  echo "## Per-pad output"
  echo
  for r in "${rows[@]}"; do
    IFS='|' read -r p s t note <<< "$r"
    [ "$s" = "SKIP" ] && continue
    echo "### $p ($s)"
    echo
    echo '```'
    sed -n '/Key errors:/,$p' "$SWEEP/$p/run.log" | sed -e 's/.*| ERROR   |//' -e 's/.*| INFO    |//' | head -20
    echo '```'
    echo
  done
} > "$sum"

echo
echo "-----------------------------------------------------------------"
printf 'pass %d   fail %d   error/skip %d   of %d\n' "$n_pass" "$n_fail" "$n_err" "${#pads[@]}"
echo "summary : $sum"
echo "results : $SWEEP/<pad>/"

[ "$n_fail" -eq 0 ] && [ "$n_err" -eq 0 ]
