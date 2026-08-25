#!/usr/bin/env bash
#
# Apply the local LVS deck patches to the installed PDK.
#
# The PDK lives inside the container image, so these patches DIE WITH THE
# CONTAINER. Re-run this after every container restart:
#   bash /foss/designs/ihp-open-pdk-regression/lvs_patches/apply.sh
#
# Safe to run repeatedly: already-applied patches are detected and skipped.
# Originals are kept as <file>.orig next to the patched file.
#
#   --revert   restore the originals and remove the patches
#
# Patches:
#   flatten_cells.patch  adds --flatten_cells to run_lvs.py / sg13g2.lvs, to
#                        flatten library cells whose parallel devices are tied
#                        together only by parent-level metal. See Findings.md.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DECK="${IOPAD_PDK:-/foss/pdks/ihp-sg13g2}/libs.tech/klayout/tech/lvs"
PATCHES=(flatten_cells.patch)
REVERT=0
[ "${1:-}" = "--revert" ] && REVERT=1

[ -d "$DECK" ] || { echo "LVS deck not found at $DECK" >&2; exit 1; }
command -v patch >/dev/null || { echo "the 'patch' utility is not installed" >&2; exit 1; }

# Writability is checked per patch, only once something actually needs doing,
# so a plain user can still run this to see what is applied.
need_root() {
  echo "    no write permission on $DECK" >&2
  echo "    run as root: docker exec -u 0 <container> bash $HERE/$(basename "${BASH_SOURCE[0]}")" >&2
}

rc=0
for p in "${PATCHES[@]}"; do
  src="$HERE/$p"
  [ -f "$src" ] || { echo "$p: missing"; rc=1; continue; }

  # a clean reverse-apply means the patch is already in place
  applied=0
  patch -p1 -R -d "$DECK" --dry-run -s -i "$src" >/dev/null 2>&1 && applied=1

  if [ "$REVERT" = 1 ]; then
    if [ "$applied" = 0 ]; then
      echo "$p: not applied, nothing to revert"
    elif [ ! -w "$DECK" ]; then
      echo "$p: applied, but cannot revert"; need_root; rc=1
    else
      patch -p1 -R -d "$DECK" -s -i "$src" && echo "$p: reverted"
    fi
    continue
  fi

  if [ "$applied" = 1 ]; then
    echo "$p: already applied"
    continue
  fi

  if ! patch -p1 -d "$DECK" --dry-run -s -i "$src" >/dev/null 2>&1; then
    echo "$p: does NOT apply cleanly to this PDK, skipped" >&2
    echo "    the deck has probably changed; regenerate with regenerate_patch.py" >&2
    rc=1
    continue
  fi

  if [ ! -w "$DECK" ]; then
    echo "$p: needs applying"; need_root; rc=1
    continue
  fi

  patch -p1 -d "$DECK" -b -z .orig -s -i "$src" && echo "$p: applied (originals kept as *.orig)"
done

echo
if [ "$REVERT" = 1 ]; then
  echo "deck restored: $DECK"
else
  echo "deck patched: $DECK"
  echo "new option:   run_lvs.py --flatten_cells=\"cellA,cellB*\""
fi
exit $rc
