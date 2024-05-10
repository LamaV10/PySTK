#import
import pygame
import time
import math
from pygame import mixer
from utils import scale_image, blit_rotate_center
pygame.init()


#music import/play
mixer.music.load("Js.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#window setup
WIN = pygame.display.set_mode((2560,1400))
pygame.display.set_caption("SuperTuxKart")

#Background and Mask
BG = pygame.transform.scale(pygame.image.load('rennstrecke.jpg'), (2560, 1400))
TRACK_BORDER = scale_image(pygame.image.load("rennstrecke_mask.xcf"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
#Racer Nr.1
racer1 = scale_image(pygame.image.load("tuxi.xcf"), 0.35)
player1 = pygame.Rect((810, 1250, 100, 100))
movement1 = racer1.get_rect()
#player1_mask = pygame.transform.scale(pygame.image.load("tuxMask.xcf").convert_alpha(), (100, 100))

#Racer Nr.2
racer2 = scale_image(pygame.image.load("yoshi.xcf"), 0.30)
player2 = pygame.Rect((930, 1130, 100, 100))
movement2 = racer2.get_rect()

class Carphy:
    def __init__(self):
        self.img = self.IMG


#collsion def
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

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
    WIN.blit(racer1, player1)
    WIN.blit(racer2, player2)

    if racer1.collide(TRACK_BORDER_MASK):
        print('collide')

    #player Nr.1 control
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and player1.x - PLAYER_VEL >= 0:
        player1.move_ip(-5, 0)
    if key[pygame.K_d] and player1.x - PLAYER_VEL + PLAYER_WIDTH <= 2500:
        player1.move_ip(5, 0)
    if key[pygame.K_w] and player1.y - PLAYER_VEL >= 0:
        player1.move_ip(0, -5)
    if key[pygame.K_s] and player1.y - PLAYER_VEL + PLAYER_WIDTH <= 1380:
        player1.move_ip(0, 5)

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
