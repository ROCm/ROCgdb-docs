# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm/ROCgdb)

> [!NOTE]
> The published documentation is available at [ROCgdb documentation](https://rocm.docs.amd.com/projects/ROCgdb/en/latest/) in an organized, easy-to-read format, with search and a table of contents.

## How the GDB documentation is built

The GDB manuals (HTML and PDF) are generated from the
[ROCgdb](https://github.com/ROCm/ROCgdb) source, not written by hand. `build_docs.sh`
configures and builds that source (`configure` + `make` + `make do-html` +
`make do-pdf`) and copies the result into `_readthedocs/html/ROCgdb` (HTML) and
`docs/_static/pdf/ROCgdb` (PDF).

ROCgdb is not a git submodule. Which source to build is declared in
[`rocgdb.yaml`](rocgdb.yaml), and the repository is cloned at build time:

```yaml
rocgdb:
  url: https://github.com/ROCm/ROCgdb.git
  branch: release/therock-10.1
  commit: 7e541ef6fe7d5ad8172cf227656103f22f975226
```

`scripts/resolve_rocgdb_commit.py` turns that into the commit to build and the release
tag to publish under. A non-empty `commit` is used as-is, which keeps builds
reproducible; leave it empty to track the latest commit of `branch`, resolved with
`git ls-remote`. The release tag is `gdb-docs-<last segment of branch>-<commit>`, so
the pinned commit above publishes under
`gdb-docs-therock-10.1-7e541ef6fe7d5ad8172cf227656103f22f975226`.

The native build takes around 16 minutes, which exceeds Read the Docs' build-time
limit, so it does not run on Read the Docs. Instead it is automated in two steps:

1. **GitHub Actions builds and publishes the docs.** The
   [`Build GDB docs and publish release asset`](.github/workflows/build-gdb-docs.yml)
   workflow clones ROCgdb at the resolved commit, runs `build_docs.sh` on a Linux
   runner, packages the HTML and PDFs into `rocgdb-docs-html-pdf.tar.gz`, and
   publishes it as a GitHub Release asset. Because the asset is keyed by the resolved
   commit, any branch resolving to the same commit reuses the same asset and the build
   is skipped when it already exists. The tarball also carries a `rocgdb-meta/`
   directory holding `version.in`, `COPYING`, and the resolved commit. The workflow
   runs on pushes that change `rocgdb.yaml`, `build_docs.sh`, or the workflow itself
   (and on manual dispatch), and triggers the matching Read the Docs build once the
   asset is published.

2. **Read the Docs downloads the published docs.** During its build,
   [`.readthedocs.yaml`](.readthedocs.yaml) runs the same
   `scripts/resolve_rocgdb_commit.py` to derive the release tag, downloads the matching
   asset, and extracts it into place. Read the Docs never clones ROCgdb: `docs/conf.py`
   reads the version and license from the bundled `rocgdb-meta/` instead. Read the Docs
   does not compile the manuals itself.

Both systems resolve the tag through the same script, so they cannot disagree about
which asset belongs to a given commit.

> [!NOTE]
> When `rocgdb.yaml` changes, the Read the Docs build can start before the GitHub
> Actions build has published the new asset. In that case the download fails with a
> 404 ("artifact not found") and the Read the Docs build fails. This is expected: wait
> for the `Build GDB docs and publish release asset` workflow to finish, then **rerun
> the Read the Docs build** and it will find the asset. For branch builds the workflow
> triggers Read the Docs automatically once the asset is published; a pull request
> preview must be rebuilt manually (or by pushing a new commit).

To update the documentation, edit `rocgdb.yaml` and push:

```bash
# Point at a different branch, or set `commit` to pin an exact revision.
$EDITOR rocgdb.yaml
git commit -am "Update ROCgdb source for the GDB manuals"
git push
```

The GitHub Actions workflow then builds and publishes the new docs, and Read the Docs
picks them up. The generated HTML and PDF trees are not committed to this repository.

## How to build documentation locally

Publishing is automated (see above); these steps are for previewing the site on your
own machine. Run the following steps to build the base documentation site:

```bash
cd docs
pip3 install -r sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```

Run the additional following steps to build the gdb documentation and display it locally with the documentation site. ROCgdb is cloned rather than checked out as a submodule; clone it into `ROCgdb/` at the repository root, which is where `build_docs.sh` and `docs/conf.py` look for it (the directory is gitignored):

```bash
cd ..
pip3 install pyyaml
git clone https://github.com/ROCm/ROCgdb.git
git -C ROCgdb checkout "$(python3 scripts/resolve_rocgdb_commit.py --commit)"
cd ROCgdb
./configure
make
make do-html
cd ..
cp -v --parents `find ROCgdb/ -name "*.html"` docs/_build/html
```

Using `resolve_rocgdb_commit.py` checks out the same commit the automated build uses. To preview a different revision, check out that revision instead.

Alternatively, change `build_docs.sh` and run it.

Change:

```diff
- cp -v --parents `find . -name '*.html'` ../_readthedocs/html/ROCgdb
+ cp -v --parents `find . -name '*.html'` ../docs/_build/html
```

Command:

```bash
./build_docs.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and the
[ROCm contribution guide](https://rocm.docs.amd.com/en/latest/contribute/contributing.html)
for the broader process.

## Security

See [SECURITY.md](SECURITY.md) for the security policy and how to report a vulnerability.

## License

See [LICENSE](LICENSE).
