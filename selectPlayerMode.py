# import pyautogui as auto
import time 
import pygame
import pygame_gui
from utils import scale_image, blit_rotate_center

# scale_factor = float(input("Choose scale-factor: "))

# Background = scale_image(pygame.image.load("imgs/Background/selMod_BG/selMod_bg.png"), scale_factor * 0.5 )

#window setup
# WIDTH, HEIGHT = Background.get_width(), Background.get_height()
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("select PySTK Mode")

manager = pygame_gui.UIManager((1600, 900))

TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager, object_id="#main_text_entry")

def get_scale_factor():
    run = True
    while run:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000

        #cloeses the windows if run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
            #     event.ui_object_id == '#main_text_entry'):
            #
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        SCREEN.fill("white")

        manager.draw_ui(SCREEN)

        pygame.display.update()
 
























######################################################################################

    # print("What layout is currently set on your machine?")
    # print("(This is not relevant if you are on Windows. Choose US in this case!)")
    # language = int(input("US (1) or DE (2) layout: "))
    # mode = int(input("singleplayer (1) or multiplayer(2): "))
    # print(mode)
    #
    # if mode == 1 and language == 1:
    #     #this is the normal textthe normal text for the us layout
    #     auto.write("python PySTK_main.py")
    #     time.sleep(1)
    #     auto.press('enter')
    # if mode == 1 and language == 2:
    #     #this is for the de layout
    #     auto.write("pzthon PzSTK?main.pz")
    #     time.sleep(1)
    #     auto.press('enter')
    #
    #
    # if mode == 2 and language == 1:
    #     #this is the normal textthe normal text for the us layout
    #     auto.write("python PySTK_main_duo.py")
    #     time.sleep(1)
    #     auto.press('enter')
    # if mode == 2 and language == 2:
    #     #this is for the de layout
    #     auto.write("pzthon PzSTK?main?duo.pz")
    #     time.sleep(1)
    #     auto.press('enter')
    #
    # run = False

# pygame.quit()
