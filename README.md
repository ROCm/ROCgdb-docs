# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm/ROCgdb)

> [!NOTE]
> The published documentation is available at [ROCgdb documentation](https://rocm.docs.amd.com/projects/ROCgdb/en/latest/) in an organized, easy-to-read format, with search and a table of contents.

## How the GDB documentation is built

The GDB manuals (HTML and PDF) are generated from the
[ROCgdb](https://github.com/ROCm/ROCgdb) source, not written by hand. `build_docs.sh`
configures that source and runs `make do-html` and `make do-pdf`, copying the result
into `_readthedocs/html/ROCgdb` (HTML) and `docs/_static/pdf/ROCgdb` (PDF). The
generated trees are not committed to this repository.

Read the Docs does the whole thing during its own build, so there is no workflow,
release asset or API token involved. [`.readthedocs.yaml`](.readthedocs.yaml)
installs the toolchain through `apt_packages` and then runs two `pre_build` jobs:

1. [`scripts/fetch_rocgdb.sh`](scripts/fetch_rocgdb.sh) shallow-fetches the ROCgdb
   commit into `ROCgdb/`.
2. `build_docs.sh` configures that checkout and generates the manuals.

`docs/conf.py` reads the version, license and commit from the same checkout.

ROCgdb is not a git submodule. Which source to build is declared in
[`rocgdb.yaml`](rocgdb.yaml):

```yaml
rocgdb:
  url: https://github.com/ROCm/ROCgdb.git
  branch: release/therock-10.1
  commit: 7e541ef6fe7d5ad8172cf227656103f22f975226
```

`scripts/resolve_rocgdb_commit.py` turns that into the commit to fetch. A non-empty
`commit` is used as-is, which keeps builds reproducible; leave it empty to track the
latest commit of `branch`, resolved with `git ls-remote`.

The build fits comfortably inside the Read the Docs build-time limit. Measured in an
ubuntu-22.04 container on a constrained CPU budget:

| phase | time |
| --- | --- |
| `apt_packages` (including texlive) | 44s |
| shallow fetch of ROCgdb | 34s |
| `configure` | 2s |
| `make do-html` | 95s |
| `make do-pdf` | 9s |
| total | 184s |

Two things keep it there, and both are easy to undo by accident. `build_docs.sh`
runs no `make` before the doc targets, which build their own prerequisites, and it
passes `--disable-binutils`, `--disable-gas`, `--disable-ld` and friends to
`configure` so the sibling binutils manuals are not built. See the comments in that
script, which record the measurements behind both.

To update the documentation, edit `rocgdb.yaml` and push:

```bash
# Point at a different branch, or set `commit` to pin an exact revision.
$EDITOR rocgdb.yaml
git commit -am "Update ROCgdb source for the GDB manuals"
git push
```

Read the Docs rebuilds and picks up the new source on its next build.

## How to build documentation locally

Publishing is automated (see above); these steps are for previewing the site on your
own machine. Run the following steps to build the base documentation site:

```bash
cd docs
pip3 install -r sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```

Run the additional following steps to build the gdb documentation. These are the same
two jobs Read the Docs runs, so a local preview matches what gets published. ROCgdb is
fetched into `ROCgdb/` at the repository root, which is where `build_docs.sh` and
`docs/conf.py` look for it (the directory is gitignored):

```bash
cd ..
pip3 install pyyaml
bash scripts/fetch_rocgdb.sh
bash build_docs.sh
```

That needs the same toolchain Read the Docs installs: `build-essential`, `libgmp-dev`,
`libmpfr-dev`, `texinfo`, `bison`, `flex`, and `texlive` plus `texlive-plain-generic`
for the PDFs. To preview a different revision, edit `rocgdb.yaml` first, or check out
that revision in `ROCgdb/` after fetching.

`build_docs.sh` writes the HTML to `_readthedocs/html/ROCgdb`. To view it alongside a
local Sphinx build instead, copy it across:

```bash
cp -v --parents `find _readthedocs/html/ROCgdb -name "*.html"` docs/_build/html
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and the
[ROCm contribution guide](https://rocm.docs.amd.com/en/latest/contribute/contributing.html)
for the broader process.

## Security

See [SECURITY.md](SECURITY.md) for the security policy and how to report a vulnerability.

## License

See [LICENSE](LICENSE).
