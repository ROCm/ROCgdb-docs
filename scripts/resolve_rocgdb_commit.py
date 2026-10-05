#!/usr/bin/env python3
"""Resolve the ROCgdb commit (and release tag) to build/download from rocgdb.yaml.

If `rocgdb.commit` is set, that commit is used (reproducible builds). Otherwise
the latest commit of `rocgdb.branch` is resolved with `git ls-remote`.

The release asset is keyed by both the ROCgdb branch and commit so the tag is
human-readable about which source branch it came from:

    gdb-docs-<branch-last-segment>-<commit>

e.g. branch `release/therock-10.1` + commit `7e541ef...` -> `gdb-docs-therock-10.1-7e541ef...`.

Both the GitHub Actions build workflow and the Read the Docs build read the same
value through this script, so they always agree on the tag.

Usage:
  python3 scripts/resolve_rocgdb_commit.py [--commit|--slug|--tag] [path/to/rocgdb.yaml]
Default output is the commit SHA.
"""
import subprocess
import sys

import yaml


def _branch_slug(branch: str) -> str:
    """Last path segment of the branch, made tag/URL safe."""
    seg = branch.rsplit("/", 1)[-1]
    return "".join(c if (c.isalnum() or c in "-._") else "-" for c in seg)


def resolve(path: str) -> tuple[str, str]:
    """Return (commit, branch) from the config, resolving the branch if needed."""
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["rocgdb"]

    branch = (cfg.get("branch") or "").strip()
    commit = (cfg.get("commit") or "").strip()
    if commit:
        return commit, branch

    url = cfg["url"]
    if not branch:
        raise SystemExit("rocgdb.yaml must set either 'commit' or 'branch'")
    out = subprocess.check_output(
        ["git", "ls-remote", url, f"refs/heads/{branch}"], text=True
    )
    if not out.strip():
        raise SystemExit(f"Could not resolve branch '{branch}' at {url}")
    return out.split()[0], branch


def main(argv: list[str]) -> int:
    mode = "--commit"
    path = "rocgdb.yaml"
    for arg in argv:
        if arg in ("--commit", "--slug", "--tag"):
            mode = arg
        else:
            path = arg

    commit, branch = resolve(path)
    slug = _branch_slug(branch) if branch else ""

    if mode == "--commit":
        print(commit)
    elif mode == "--slug":
        print(slug)
    else:  # --tag
        print(f"gdb-docs-{slug}-{commit}" if slug else f"gdb-docs-{commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
