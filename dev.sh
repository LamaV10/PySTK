# This script compiles PySTK_main and overwrites the old binary in the Source/bin directory.
# Then it executes the binary (should work on Linux and maybe MacOS) 

if [ -f /usr/bin/python ]; then
  pythonTyp=python

elif [ -f /usr/bin/python3 ]; then
  pythonTyp=python3
fi

cd Source/
$pythonTyp -m py_compile PySTK_main.py
mv -f __pycache__/PySTK_main.cpython-313.pyc bin/
cd bin/
$pythonTyp PySTK_main.cpython-313.pyc
cd ..
cd ..
