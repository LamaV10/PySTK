# This script compiles PySTK_main and overwrites the old binary in the Source/bin directory.
# Then it executes the binary (should work on Linux and maybe MacOS) 

cd Source/
python -m py_compile PySTK_main.py
mv -f __pycache__/PySTK_main.cpython-312.pyc bin/
cd bin/
python PySTK_main.cpython-312.pyc
cd ..
cd ..
