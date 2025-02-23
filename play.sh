# searches which python version is installed (from 3.13 - 3.11)
if [ -f /usr/bin/python3.13 ]; then
  pythonTyp=python3.13
  file=PySTK_main.cpython-313.pyc

elif [ -f /usr/bin/python3.12 ]; then
  pythonTyp=python3.12
  file=PySTK_main.cpython-312.pyc

elif [ -f /usr/bin/python3.11 ]; then
  pythonTyp=python3.12
  file=PySTK_main.cpython-311.pyc

fi

tag="-m"

cd Source/bin/
$pythonTyp $file
