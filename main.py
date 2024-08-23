import pygame
import time
import pyautogui as auto
import pygame_gui
import sys

pygame.init()

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input in PyGame | BaralTech")

manager = pygame_gui.UIManager((1600, 900))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')

language = 0
mode = 0


clock = pygame.time.Clock()
def get_language():
    run = True
    global language
    while run:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                language = event.text 
                print("language:", language)
                run = False
            
            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)

        SCREEN.fill("black")

        manager.draw_ui(SCREEN)

        pygame.display.update()


def get_mode():
    run = True
    global mode 
    while run:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                mode = event.text 
                print("mode:", mode)
                run = False
            
            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)

        SCREEN.fill("black")

        manager.draw_ui(SCREEN)

        pygame.display.update()


get_language()
get_mode()

# print("What layout is currently set on your machine?")
# print("(This is not relevant if you are on Windows. Choose US in this case!)")

if language == 1:
    auto.write("cd Source/")
    time.sleep(1)
    auto.press('enter')

if language == 2:
    auto.write("cd Source-")
    time.sleep(1)
    auto.press('enter')



if mode == 1 and language == 1:
    #this is the normal textthe normal text for the us layout
    auto.write("python PySTK_main.py")
    time.sleep(1)
    auto.press('enter')

elif mode == 1 and language == 2:
    #this is for the de layout
    auto.write("pzthon PzSTK?main.pz")
    time.sleep(1)
    auto.press('enter')


if mode == 2 and language == 1:
    #this is the normal textthe normal text for the us layout
    auto.write("python PySTK_main_duo.py")
    time.sleep(1)
    auto.press('enter')

elif mode == 2 and language == 2:
    #this is for the de layout
    auto.write("pzthon PzSTK?main?duo.pz")
    time.sleep(1)
    auto.press('enter')
