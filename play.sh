echo "Singleplayer (1) or Multiplayer (2)?"
read mode

cd Source/

if [ $mode -eq 1 ]; then
  python PySTK_main.py
fi


if [ $mode -eq 2 ]; then
  python PySTK_main_duo.py
fi
