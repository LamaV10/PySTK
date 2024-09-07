echo "Singleplayer (1) or Multiplayer (2)?"
read mode

if [ $mode -eq 1 ]
then
  cd Source/
  python PySTK_main.py
fi

if [ $mode -eq 2 ]
then
  cd Source/
  python PySTK_main_duo.py
fi
