# This script compiles PySTK_main and overwrites the old binary in the Source/bin directory.
# Then it executes the binary (should work on Linux and maybe MacOS) 

if [ -f /usr/bin/python3.13 ]; then
  pythonTyp=python3.13
  file=PySTK_main.cpython-313.pyc

elif [ -f /usr/bin/python3.12 ]; then
  pythonTyp=python3.12
  file=PySTK_main.cpython-312.pyc
fi

tag="-m"

cd Source/
$pythonTyp $tag py_compile PySTK_main.py
mv -f __pycache__/$file bin/
cd bin/
$pythonTyp $file 
