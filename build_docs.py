import os

os.system("git submodule update --init --recursive")
os.system("git submodule update --remote --merge")
os.system("cd ROCgdb")
os.system("./configure")
os.system("make do-html")
os.system("cd ..")
os.system("mkdir --parents _readthedocs/html")
os.system("cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html")
os.system("cd docs")
os.system("pip3 install -r .sphinx/requirements.txt")
os.system("python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html")
