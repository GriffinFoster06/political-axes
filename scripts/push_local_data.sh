#!/usr/bin/env bash
# Push data files you downloaded by hand (ANES, Pew) to the `data` branch.
#
#   scripts/push_local_data.sh anes ~/Downloads/anes_timeseries_2024_csv_20260519.zip
#   scripts/push_local_data.sh pew  ~/Downloads/ATP_W183.zip
#
# First argument is the folder name the files go under (anes, pew, ...).
# Zips are unpacked first so the data branch holds the actual data files.
#
# IMPORTANT: ANES and Pew terms restrict redistributing their microdata.
# Only push them to a PRIVATE repository. This script refuses if the target
# repo is public (checked with the GitHub CLI when available).
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <folder> <file-or-zip> [more files...]" >&2
  exit 1
fi
FOLDER="$1"; shift
REPO_ROOT="$(git rev-parse --show-toplevel)"

if command -v gh >/dev/null 2>&1; then
  REMOTE_URL="$(git -C "$REPO_ROOT" remote get-url "${DATA_REMOTE:-origin}")"
  VIS="$(gh repo view "$REMOTE_URL" --json visibility -q .visibility 2>/dev/null || echo UNKNOWN)"
  if [ "$VIS" = "PUBLIC" ] && [ "${ALLOW_PUBLIC:-0}" != "1" ]; then
    echo "Refusing: $REMOTE_URL is PUBLIC. Make it private (or set DATA_REMOTE to a private repo)." >&2
    echo "Override only if the data's license allows redistribution: ALLOW_PUBLIC=1 $0 ..." >&2
    exit 2
  fi
else
  echo "Note: GitHub CLI not found, so repo visibility was not checked. Make sure the repo is private." >&2
fi

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/$FOLDER"
for f in "$@"; do
  case "$f" in
    *.zip) unzip -q -o "$f" -d "$STAGE/$FOLDER" ;;
    *) cp "$f" "$STAGE/$FOLDER/" ;;
  esac
done
find "$STAGE" -name '__MACOSX' -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" -name '.DS_Store' -delete 2>/dev/null || true

"$REPO_ROOT/scripts/commit_to_data_branch.sh" "$STAGE" "Add $FOLDER data ($(date -u +%Y-%m-%d))"
