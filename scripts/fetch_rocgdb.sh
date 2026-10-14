#!/bin/bash
# Fetch the ROCgdb source that the manuals are built from.
#
# The repository and revision come from rocgdb.yaml, resolved by
# scripts/resolve_rocgdb_commit.py (a pinned `commit` wins, otherwise the latest
# commit of `branch`), so this agrees with every other consumer of that config.
#
# The fetch is shallow and targets the resolved commit directly rather than
# cloning the history. ROCgdb carries the full binutils-gdb history, which is
# large enough to dominate a Read the Docs build; the manuals need the tree at
# one commit, not the history that led to it.
set -euo pipefail

DEST="${1:-ROCgdb}"

URL=$(python3 -c "import yaml;print(yaml.safe_load(open('rocgdb.yaml'))['rocgdb']['url'])")
SHA=$(python3 scripts/resolve_rocgdb_commit.py --commit)
echo "Fetching ROCgdb $SHA from $URL into $DEST"

rm -rf "$DEST"
# Keep LF endings so GDB's configure script runs regardless of core.autocrlf.
git -c core.autocrlf=false -c core.eol=lf init -q "$DEST"
git -C "$DEST" remote add origin "$URL"
git -C "$DEST" fetch -q --depth 1 origin "$SHA"
git -C "$DEST" checkout -q FETCH_HEAD

echo "ROCgdb at $(git -C "$DEST" rev-parse HEAD)"
