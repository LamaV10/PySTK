echo "Put the directory where your music is located in the following file which is going to be opend!"
echo "Press 1 and then Enter to continue: "

read continue

if [ $continue -eq 1 ]; then
  cd Source/

  if [ -f /usr/bin/nvim ]; then
    nvim music.py	

  elif [ -f /usr/bin/vim ]; then
    vim	music.py

  elif [ -f /usr/bin/nano ]; then
  nano music.py
  
  elif [ -f /usr/bin/vscodium ]; then
  vscodium music.py
  
  elif [ -f /usr/bin/code ]; then
  code music.py
  fi

fi
