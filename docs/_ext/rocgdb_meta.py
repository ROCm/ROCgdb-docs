"""Inject the ROCgdb commit and version into each page's HTML <head>.

Adds, to the Sphinx-built pages (not the generated GDB manual pages):

    <meta name="rocgdb-commit"  content="<resolved commit sha>">
    <meta name="rocgdb-version" content="<version>">

so the exact ROCgdb source the docs were built from is visible in the browser
"view source". Values come from conf.py (sourced from the release asset's
rocgdb-meta/ bundle), registered as the config values below.

Sphinx has no site-wide html_meta, and rocm-docs-core does not manage meta tags,
so the standard html-page-context event is used (the same event rocm-docs-core
itself connects to).
"""
from __future__ import annotations

from typing import Any

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)


def _inject(app: Sphinx, pagename, templatename, context, doctree) -> None:
    commit = app.config.rocgdb_commit or ""
    version = app.config.rocgdb_version or ""
    tags = ""
    if commit:
        tags += f'<meta name="rocgdb-commit" content="{commit}">\n'
    if version:
        tags += f'<meta name="rocgdb-version" content="{version}">\n'
    if tags:
        context["metatags"] = context.get("metatags", "") + tags


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("rocgdb_commit", "", "html")
    app.add_config_value("rocgdb_version", "", "html")
    app.connect("html-page-context", _inject)
    if not (app.config.rocgdb_commit or app.config.rocgdb_version):
        logger.info("rocgdb_meta: no rocgdb_commit/version set; meta tags will be omitted")
    return {"parallel_read_safe": True, "parallel_write_safe": True}
