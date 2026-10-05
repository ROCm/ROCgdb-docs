# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
import shutil
import sys
from pathlib import Path

from rocm_docs import ROCmDocs

DOCS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = DOCS_DIR.parent

# ROCgdb is no longer a git submodule. The "Build GDB docs" workflow builds the
# manuals and bundles the resolved commit, version, and license into the release
# asset under rocgdb-meta/, which Read the Docs extracts at the repo root before
# this build runs. Read those instead of a local ROCgdb checkout. A local ROCgdb/
# clone (for developer previews) is used as a fallback.
META_DIR = ROOT_DIR / "rocgdb-meta"


def copy_rtd_file(src_path: Path, dest_path: Path):
    if not src_path.exists():
        print(f"Skipped copy, source not found: {src_path}")
        return
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    print(f"Copied {src_path} -> {dest_path}")


def _read_build_info() -> dict:
    """Parse rocgdb-meta/rocgdb-build-info.txt (key=value) if present."""
    info: dict = {}
    info_file = META_DIR / "rocgdb-build-info.txt"
    if info_file.exists():
        for line in info_file.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                info[k.strip()] = v.strip()
    return info


def _version_from_file(version_in: Path) -> str:
    match = re.search(r"([0-9.]+)[^0-9.]+", version_in.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("VERSION not found!")
    return match[1]


build_info = _read_build_info()

# License: prefer the bundled copy, fall back to a local ROCgdb checkout.
for copying in (META_DIR / "COPYING", ROOT_DIR / "ROCgdb" / "COPYING"):
    if copying.exists():
        copy_rtd_file(copying, ROOT_DIR / "LICENSE")
        break

# Version + resolved commit: prefer the bundled build info, then the bundled
# version.in, then a local ROCgdb checkout.
rocgdb_commit = build_info.get("commit", "")
if build_info.get("version"):
    version_number = build_info["version"]
elif (META_DIR / "version.in").exists():
    version_number = _version_from_file(META_DIR / "version.in")
elif (ROOT_DIR / "ROCgdb" / "gdb" / "version.in").exists():
    version_number = _version_from_file(ROOT_DIR / "ROCgdb" / "gdb" / "version.in")
else:
    raise ValueError(
        "No ROCgdb version source found (expected rocgdb-meta/ from the release "
        "asset, or a local ROCgdb/ checkout)."
    )
left_nav_title = f"ROCgdb {version_number} Documentation"

# for PDF output on Read the Docs
project = "ROCgdb Documentation"
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) 2024 Advanced Micro Devices, Inc. All rights reserved."
version = version_number
release = version_number

external_toc_path = "./sphinx/_toc.yml"

docs_core = ROCmDocs(left_nav_title)
docs_core.setup()

html_static_path = ['_static']

external_projects_current_project = "rocgdb"

for sphinx_var in ROCmDocs.SPHINX_VARS:
    globals()[sphinx_var] = getattr(docs_core, sphinx_var)
