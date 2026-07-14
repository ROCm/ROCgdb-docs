# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
import shutil
import subprocess
import sys
from pathlib import Path

from rocm_docs import ROCmDocs

subprocess.run("git submodule update --init", shell=True)

DOCS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = DOCS_DIR.parent


def copy_rtd_file(src_path: Path, dest_path: Path):
    if not src_path.exists():
        print(f"Skipped copy, source not found: {src_path}")
        return
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    print(f"Copied {src_path} -> {dest_path}")


# Source the license from the ROCgdb submodule; the built docs are derived
# from GPL-licensed ROCgdb source, so they carry ROCgdb's license.
copy_rtd_file(ROOT_DIR / "ROCgdb" / "COPYING", ROOT_DIR / "LICENSE")

with open("../ROCgdb/gdb/version.in", encoding="utf-8") as f:
    match = re.search(r"([0-9.]+)[^0-9.]+", f.read())
    if not match:
        raise ValueError("VERSION not found!")
    version_number = match[1]
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
