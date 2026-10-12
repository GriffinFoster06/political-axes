#!/usr/bin/env bash
# Package a folder of data files onto the orphan `data` branch and push it.
#
#   scripts/commit_to_data_branch.sh <staging_dir> [message]
#
# Each file is gzipped. Anything still over 90 MB is split into 90 MB parts
# (GitHub rejects files over 100 MB). scripts/restore_data.py reverses this.
# The `data` branch never touches `main`, so code history stays small.
set -euo pipefail

STAGING="$(cd "$1" && pwd)"
MSG="${2:-Update data $(date -u +%Y-%m-%d)}"
REMOTE="${DATA_REMOTE:-origin}"
BRANCH="${DATA_BRANCH:-data}"
LIMIT="${DATA_SPLIT_BYTES:-$((90 * 1024 * 1024))}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORK="$(mktemp -d)"
trap 'git -C "$REPO_ROOT" worktree remove --force "$WORK" >/dev/null 2>&1 || rm -rf "$WORK"' EXIT

cd "$REPO_ROOT"
if git ls-remote --exit-code --heads "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
  git fetch --depth 1 "$REMOTE" "$BRANCH"
  git worktree add --force "$WORK" "FETCH_HEAD" >/dev/null
  git -C "$WORK" checkout -B "$BRANCH" >/dev/null
else
  git worktree add --force --detach "$WORK" >/dev/null
  git -C "$WORK" checkout --orphan "$BRANCH" >/dev/null
  git -C "$WORK" rm -rf --quiet . >/dev/null 2>&1 || true
  cat > "$WORK/README.md" <<'EOF'
# Data branch

Raw datasets for political-axes, gzipped and split into <90 MB parts.
Do not merge into main. Restore with `python3 scripts/restore_data.py`
from the main branch. Licenses and citations: see DATA.md on main.
EOF
fi

cd "$STAGING"
find . -type f | while read -r f; do
  rel="${f#./}"
  dest="$WORK/raw/$rel.gz"
  mkdir -p "$(dirname "$dest")"
  rm -f "$dest" "$dest".part*
  gzip -9 -n -c "$f" > "$dest"
  size=$(wc -c < "$dest")
  if [ "$size" -gt "$LIMIT" ]; then
    split -b "$LIMIT" -d -a 3 "$dest" "$dest.part"
    rm "$dest"
  fi
done

cd "$WORK"
find raw -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
git add -A
if git diff --cached --quiet; then
  echo "no data changes"
  exit 0
fi
git commit -q -m "$MSG"
git push "$REMOTE" "HEAD:$BRANCH"
echo "pushed to $REMOTE/$BRANCH"
