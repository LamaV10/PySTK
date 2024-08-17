import time
import pyautogui as auto


print("What layout is currently set on your machine?")
print("(This is not relevant if you are on Windows. Choose US in this case!)")

language = int(input("US (1) or DE (2) layout: "))
mode = int(input("singleplayer (1) or multiplayer(2): "))


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


