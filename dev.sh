cd Source/
python -m py_compile PySTK_main.py
mv -f __pycache__/PySTK_main.cpython-312.pyc bin/
cd bin/
python PySTK_main.cpython-312.pyc
cd ..
cd ..
