# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm/ROCgdb)

> [!NOTE]
> The published documentation is available at [ROCgdb documentation](https://rocm.docs.amd.com/projects/ROCgdb/en/latest/) in an organized, easy-to-read format, with search and a table of contents.

## How the GDB documentation is built

The GDB manuals (HTML and PDF) are generated from the [ROCgdb](https://github.com/ROCm/ROCgdb)
submodule, not written by hand. `build_docs.sh` configures and builds the submodule
(`configure` + `make` + `make do-html` + `make do-pdf`) and copies the result into
`_readthedocs/html/ROCgdb` (HTML) and `docs/_static/pdf/ROCgdb` (PDF).

That native build takes around 16 minutes, which exceeds Read the Docs' build-time
limit, so it does not run on Read the Docs. Instead it is automated in two steps:

1. **GitHub Actions builds and publishes the docs.** The
   [`Build GDB docs and publish release asset`](.github/workflows/build-gdb-docs.yml)
   workflow runs `build_docs.sh` on a Linux runner, packages the HTML and PDFs into
   `rocgdb-docs-html-pdf.tar.gz`, and publishes it as a GitHub Release asset. The
   asset is keyed by the ROCgdb submodule commit (release tag `gdb-docs-<submodule
   sha>`), so any branch pinning the same submodule commit reuses the same asset and
   the build is skipped when it already exists. The workflow runs on pushes that
   change the submodule pointer or build files (and on manual dispatch), and triggers
   the matching Read the Docs build once the asset is published.

2. **Read the Docs downloads the published docs.** During its build,
   [`.readthedocs.yaml`](.readthedocs.yaml) derives the same submodule commit with
   `git rev-parse HEAD:ROCgdb`, downloads the matching release asset, and extracts it
   into place. Read the Docs does not compile the manuals itself.

To update the documentation, update the `ROCgdb` submodule pointer and push:

```bash
cd ROCgdb
git fetch origin
git checkout <desired commit or branch>
cd ..
git add ROCgdb
git commit -m "Update ROCgdb submodule"
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

Run the additional following steps to build the gdb documentation and display it locally with the documentation site:

```bash
cd ..
git submodule update --init --recursive
cd ROCgdb
./configure
make
make do-html
cd ..
cp -v --parents `find ROCgdb/ -name "*.html"` docs/_build/html
```

Alternatively, change `build_docs.sh` and run it.

Change:

```diff
- cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html
+ cp -v --parents `find ROCgdb/ -name '*.html'` docs/_build/html
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
