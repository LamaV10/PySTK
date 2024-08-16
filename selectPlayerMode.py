import pyautogui as auto
import time 
import pygame
from utils import scale_image, blit_rotate_center

scale_factor = float(input("Choose scale-factor: "))

Background = scale_image(pygame.image.load("imgs/Background/selMod_BG/selMod_bg.png"), scale_factor * 0.5 )

#window setup
WIDTH, HEIGHT = Background.get_width(), Background.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("select PySTK Mode")


run = True
#loop
while run:
    # Using blit to copy content from one surface to other
    WIN.blit(Background, (0, 0))
    pygame.display.update()

    print("What layout is currently set on your machine?")
    print("(This is not relevant if you are on Windows. Choose US in this case!)")
    language = int(input("US (1) or DE (2) layout: "))
    mode = int(input("singleplayer (1) or multiplayer(2): "))
    print(mode)

    if mode == 1 and language == 1:
        #this is the normal textthe normal text for the us layout
        auto.write("python PySTK_main.py")
        time.sleep(1)
        auto.press('enter')
    if mode == 1 and language == 2:
        #this is for the de layout
        auto.write("pzthon PzSTK?main.pz")
        time.sleep(1)
        auto.press('enter')


    if mode == 2 and language == 1:
        #this is the normal textthe normal text for the us layout
        auto.write("python PySTK_main_duo.py")
        time.sleep(1)
        auto.press('enter')
    if mode == 2 and language == 2:
        #this is for the de layout
        auto.write("pzthon PzSTK?main?duo.pz")
        time.sleep(1)
        auto.press('enter')
    
    run = False
    #cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
