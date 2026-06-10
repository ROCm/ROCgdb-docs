# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
import subprocess
import sys
from pathlib import Path

# Make rocm-docs-core recognize <X.Y.Z>-preview slugs (e.g. 7.13.0-preview) as
# valid version identifiers so intersphinx URLs to sister projects resolve to
# the matching preview build instead of falling back to /en/latest/.
# Remove once rocm-docs-core ships native support.
from rocm_docs import projects as _rdc_projects

# Extend DOCS_VERSION_PATTERN to also match X.Y.Z-preview slugs that RTD uses
# for docs/X.Y.Z branches (e.g. "7.13.0-preview" for branch "docs/7.13.0").
# Without this, get_static_version() falls back to "latest" for these slugs.
_rdc_projects.DOCS_VERSION_PATTERN = r"^(docs-\d+\.\d+\.\d+|\d+\.\d+\.\d+-preview)$"

subprocess.run("git submodule update --init", shell=True)

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

html_static_path = ['_static']

external_projects_current_project = "rocgdb"

html_theme = "rocm_docs_theme"
html_theme_options = {
    "announcement": f"This is ROCm 7.13.0 technology preview release documentation. For the latest production stream release, refer to <a id='rocm-banner' href='https://rocm.docs.amd.com/en/latest/'>ROCm documentation</a>.",
    "flavor": "generic",
    "header_title": f"ROCm™ 7.13.0 Preview",
    "header_link": f"https://rocm.docs.amd.com/en/7.13.0-preview/index.html",
    "version_list_link": "",
    "nav_secondary_items": {
        "GitHub": "https://github.com/ROCm/ROCm",
        "Community": "https://github.com/ROCm/ROCm/discussions",
        "Blogs": "https://rocm.blogs.amd.com/",
        "System and Infra Docs": "https://instinct.docs.amd.com/",
        "Support": "https://github.com/ROCm/ROCm/issues/new/choose",
    },
    "link_main_doc": False,
}

extensions = ["rocm_docs"]
