# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
import subprocess

from rocm_docs import ROCmDocs

subprocess.run("git submodule update --init", shell=True)

with open('../ROCgdb/zlib/CMakeLists.txt', encoding='utf-8') as f:
    match = re.search(r'.*\bset\(VERSION\s+\"?([0-9.]+)[^0-9.]+', f.read())
    if not match:
        raise ValueError("VERSION not found!")
    version_number = match[1]
left_nav_title = f"ROCgdb {version_number} Documentation"

# for PDF output on Read the Docs
project = "ROCgdb Documentation"
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) 2024 Advanced Micro Devices, Inc. All rights reserved."
version = "15.2"
release = "15.2"

external_toc_path = "./sphinx/_toc.yml"

docs_core = ROCmDocs(left_nav_title)
docs_core.setup()

external_projects_current_project = "rocgdb"

for sphinx_var in ROCmDocs.SPHINX_VARS:
    globals()[sphinx_var] = getattr(docs_core, sphinx_var)
