import pygame
import time
from pygame import mixer
pygame.init()

mixer.music.load("yourtitel.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

WIN = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("SuperTuxKart")

racer = pygame.transform.scale(pygame.image.load("imgs/tuxi.xcf").convert_alpha(), (100, 100))
player = pygame.Rect((300 ,250 , 100 ,100))
player2 = racer.get_rect()

PLAYER_VEL = 5
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
clock = pygame.time.Clock()
BG = pygame.transform.scale(pygame.image.load('imgs/rennstrecke.jpg'), (1920, 1080))

run = True
while  run:
    clock.tick(144)
    WIN.blit(BG, (0,0))
    WIN.blit(racer, player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] and player.x - PLAYER_VEL >= 0:
        player.move_ip(-5, 0)
    if key[pygame.K_d] and player.x - PLAYER_VEL + PLAYER_WIDTH <= 1840:
        player.move_ip(5, 0)
    if key[pygame.K_w] and player.y - PLAYER_VEL >= 0:
        player.move_ip(0, -5)
    if key[pygame.K_s] and player.y - PLAYER_VEL + PLAYER_WIDTH <= 1020:
        player.move_ip(0, 5)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
