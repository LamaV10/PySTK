echo "Singleplayer (1) or Multiplayer (2)?"
read mode

cd Source/bin

if [ $mode -eq 1 ]; then
  python PySTK_main.cpython-312.pyc
fi


if [ $mode -eq 2 ]; then
  python PySTK_main_duo.cpython-312.pyc
fi
