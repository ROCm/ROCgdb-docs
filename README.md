# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm-Developer-Tools/ROCgdb)

## How to build documentation locally

Run the following steps:

```
git submodule update --init --recursive
git submodule update --remote --merge
cd ROCgdb
./configure
make do-html
cd ..
mkdir --parents _readthedocs/html
cp -v --parents `find ROCgdb/ -name "*.html"` _readthedocs/html
cd docs
pip3 install -r .sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```
