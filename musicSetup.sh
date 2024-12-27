echo "Enter the location of your desiered music title (mp3):"
read location

cd Source/bin/

echo "import pygame
from pygame import mixer
pygame.init()

def music():

    run = int(input('Do you have your music setup? Yes (1) No (2): '))
    if run == 1:
        # music import/play
        # change your path to your music here:
        mixer.music.load('$location')
        

        mixer.music.set_volume(0.5)
        mixer.music.play(-1)" > music.py



