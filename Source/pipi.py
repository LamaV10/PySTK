import pygame
import math
import time

from utils import scale_image, blit_rotate_center
pygame.init()

scale_factor = 0 
def getScale_factor():
    global scale_factor

    print("For 1440p ~ 2.3, for 1080p ~ 1.8, for 720p ~ 1.25 ")
    scale_factor = float(input("Choose scale-factor: "))
    print("scale factor:", scale_factor)
    time.sleep(5)

scale_player = 0.02 * scale_factor
font_size = 32 * scale_factor

# start position player 1
START_POS_X1 = 410 * scale_factor
START_POS_Y1 = 428 * scale_factor

# start position player 2
START_POS_X2 = 345 * scale_factor
START_POS_Y2 = 478 * scale_factor

Finish_POS_X = 305 * scale_factor  
Finish_POS_Y = 460 * scale_factor


#Track and Mask
TRACK = scale_image(pygame.image.load("imgs/RaceTrack/rennstrecke.jpg"), scale_factor)
TRACK_BORDER = scale_image(pygame.image.load("imgs/RaceTrack/rennstrecke_mask.xcf"), scale_factor)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

#finish line Mask
FINISH = pygame.image.load("imgs/RaceTrack/finish-line.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (Finish_POS_X, Finish_POS_Y)

#countdown background
countdown_bg = scale_image(pygame.image.load("imgs/Background/Countdown_BG/countdown_bg.png"), scale_factor * 0.5)

#text scale factor
text_scale_factor = TRACK.get_width() * 0.00088
font_scale = math.trunc(15 * scale_factor)


# start position
START_POS_X1 = 410 * scale_factor
START_POS_Y1 = 428 * scale_factor

Finish_POS_X = 305 * scale_factor  
Finish_POS_Y = 460 * scale_factor

#Racer Nr.1
racer1 = scale_image(pygame.image.load("imgs/Tux/ferrari-rossa-tux.png"), scale_player)
racer1_mask = scale_image(pygame.image.load("imgs/Tux/ferrari-rossa-tux-mask.png"), scale_player)

#won utilities for player 1
win_text1 = "Player 1 has won!!!"
wonP1 = False

# variables necessary for multiplayer
# start position if there is a second player
START_POS_X2 = 345 * scale_factor
START_POS_Y2 = 478 * scale_factor

#Racer Nr.2
racer2 = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi.png"), scale_player)
racer2_mask = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi-mask.png"), scale_player)

# won utilities for player 2
win_text2 = "Player 2 has won!!!"
wonP2 = False

count_text = 0



# variables for displayLaptime function player 1 
last_collision_time_laptimeP1 = [0]

lastTouch1P1 = [0]
lastTouch2P1 = [0]

start1P1 = [0]
start2P1 = [0]

end1P1 = [0]
end2P1 = [0]


final_laptimeP1 = [0] 
lapcountP1 = [0]

# variables for displayLaptime function player 2 
last_collision_time_laptimeP2 = [0]

lastTouch1P2 = [0]
lastTouch2P2 = [0]

start1P2 = [0]
start2P2 = [0]

end1P2 = [0]
end2P2 = [0]


final_laptimeP2 = [0] 
lapcountP2 = [0]


# Timer for the Lapcount-collision
last_collision_timeP1 = [0]
last_collision_timeP2 = [0]
collision_delay = 10 # Sekunden
