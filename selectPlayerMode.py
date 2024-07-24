import pyautogui as auto
import time 

mode = int(input("singleplayer (1) or multiplayer(2): "))
print(mode)

if mode == 1:
    auto.write("python PySTK_main.py")
    time.sleep(1)
    auto.press('enter')

if mode == 2:
    auto.write("python PySTK_main_duo.py")
    auto.press('enter')
