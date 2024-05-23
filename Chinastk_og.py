#import
import pygame
import time
import math
from pygame import mixer
pygame.init()


#music import/play
#mixer.music.load("music/yourtitel.mp3")
#mixer.music.set_volume(0.5)
#mixer.music.play(-1)

#window setup
WIN = pygame.display.set_mode((2560,1400))
pygame.display.set_caption("SuperTuxKart")

#Background and Mask
BG = pygame.transform.scale(pygame.image.load('imgs/rennstrecke.jpg'), (2560, 1400))
#Racer Nr.1
racer = pygame.transform.scale(pygame.image.load("imgs/tuxi.xcf").convert_alpha(), (100, 100))
player = pygame.Rect((810, 1250, 100, 100))
movement = racer.get_rect()

#Racer Nr.2
racer2 = pygame.transform.scale(pygame.image.load("imgs/yoshi.xcf").convert_alpha(), (100, 100))
player2 = pygame.Rect((930, 1130, 100, 100))
movement2 = racer2.get_rect()

#Game settings
PLAYER_VEL = 5
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
clock = pygame.time.Clock()

run = True
while  run:
    #game loop setup
    clock.tick(144)
    WIN.blit(BG, (0,0))
    WIN.blit(racer, player)
    WIN.blit(racer2, player2)

    #player Nr.1 control
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and player.x - PLAYER_VEL >= 0:
        player.move_ip(-5, 0)
    if key[pygame.K_d] and player.x - PLAYER_VEL + PLAYER_WIDTH <= 2500:
        player.move_ip(5, 0)
    if key[pygame.K_w] and player.y - PLAYER_VEL >= 0:
        player.move_ip(0, -5)
    if key[pygame.K_s] and player.y - PLAYER_VEL + PLAYER_WIDTH <= 1380:
        player.move_ip(0, 5)

    #player Nr.2 control
    key2 = pygame.key.get_pressed()
    if key2[pygame.K_j] and player2.x - PLAYER_VEL >= 0:
        player2.move_ip(-5, 0)
    if key2[pygame.K_l] and player2.x - PLAYER_VEL + PLAYER_WIDTH <= 2500:
        player2.move_ip(5, 0)
    if key2[pygame.K_i] and player2.y - PLAYER_VEL >= 0:
        player2.move_ip(0, -5)
    if key2[pygame.K_k] and player2.y - PLAYER_VEL + PLAYER_WIDTH <= 1380:
        player2.move_ip(0, 5)

    #cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
