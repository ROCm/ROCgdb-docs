#!/usr/bin/env python3
"""Resolve the ROCgdb commit to build/download from rocgdb.yaml.

If `rocgdb.commit` is set, that commit is printed (reproducible builds).
Otherwise the latest commit of `rocgdb.branch` is resolved with `git ls-remote`.

Both the GitHub Actions build workflow and the Read the Docs build read the same
value through this script, so they always agree on the release asset key
(`gdb-docs-<commit>`).

Usage: python3 scripts/resolve_rocgdb_commit.py [path/to/rocgdb.yaml]
Prints the 40-char commit SHA to stdout.
"""
import subprocess
import sys

import yaml


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "rocgdb.yaml"
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["rocgdb"]

    commit = (cfg.get("commit") or "").strip()
    if commit:
        print(commit)
        return 0

    branch = (cfg.get("branch") or "").strip()
    url = cfg["url"]
    if not branch:
        sys.stderr.write("rocgdb.yaml must set either 'commit' or 'branch'\n")
        return 1

    out = subprocess.check_output(
        ["git", "ls-remote", url, f"refs/heads/{branch}"], text=True
    )
    if not out.strip():
        sys.stderr.write(f"Could not resolve branch '{branch}' at {url}\n")
        return 1
    print(out.split()[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
