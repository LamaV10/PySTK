import pygame
from pygame import mixer
pygame.init()

def music():

    run = int(input('Do you have your music setup? Yes (1) No (2): '))
    if run == 1:
        # music import/play
        # change your path to your music here:
        mixer.music.load('/home/marcel/Music/It-was-a-good-day.mp3')
        

        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
