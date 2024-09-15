echo "Put the directory where your music is located in the following file which is going to be opend!"
echo ""

echo "Which editor do you want to use?"
echo "1: NeoVim"
echo "2: Vim"
echo "3: Nano"
echo "4: Vscodium"
echo "5: Vscode"
echo "Your editors number: "

read ide
cd Source/

if [ $ide -eq 1 ]; then
  nvim music.py	

elif [ $ide -eq 2 ]; then
  vim	music.py

elif [ $ide -eq 3 ]; then
  nano music.py
  
elif [ $ide -eq 4 ]; then
  vscodium music.py
  
elif [ $ide -eq 5 ]; then
  code music.py
fi

