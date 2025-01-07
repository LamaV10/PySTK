import pygame
import time
import math
import os

import music

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clearTerminal()
music.music()

from utils import scale_image, blit_rotate_center
pygame.init()

# choose mode (single- or multiplayer) 
clearTerminal()
player_mode = int(input("Singleplayer (1) or Multiplayer (2): "))

# factors: help to adjust to different resolutions
clearTerminal()
print("For 1440p ~ 2.3, for 1080p ~ 1.8, for 720p ~ 1.25 ")
scale_factor = float(input("Choose scale-factor: "))

# choose if you want to play on 85 or 144
# 85 FPS is easier to play and works great on smaller screens (like laptops)
# FPS_input = input('(144) or (85) FPS:')
clearTerminal()
print("Choose 144 FPS if you put the scale size over 1.8")
FPS = int(input("144 FPS (1) or 85 FPS (2): "))


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

#window setup
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PySTK")
MAIN_FONT = pygame.font.SysFont("comicsans", 32)

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
won = False

# variables necessary for multiplayer
# start position if there is a second player
START_POS_X2 = 345 * scale_factor
START_POS_Y2 = 478 * scale_factor

#Racer Nr.2
racer2 = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi.png"), scale_player)
racer2_mask = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi-mask.png"), scale_player)

# won utilities for player 2
win_text2 = "Player 2 has won!!!"

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
collision_delay = 1 # Sekunden



##############
#### Car ##### 
##############

#car physics
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = 0.25 * rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS_SCALE
        self.acceleration = 0.1
        self.mask = self.mask

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.mask)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    

###################
#### Players ###### 
###################

#player1
class PlayerCar1(AbstractCar):
    IMG = racer1
    mask = racer1_mask
    START_POS_SCALE = (START_POS_X1, START_POS_Y1)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.9
        self.move()

#Player 2
class PlayerCar2(AbstractCar):
    IMG = racer2
    mask = racer2_mask
    START_POS_SCALE = (START_POS_X2, START_POS_Y2)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.9
        self.move()



# keybinds player 
# takes in the player (for example player_car1 or player_car2)
def move_player(player_car, right, left, forward, backward):

    # Convert string key names to pygame key constants
    left_key = getattr(pygame, left)
    right_key = getattr(pygame, right)
    forward_key = getattr(pygame, forward)
    backward_key = getattr(pygame, backward)


    keys = pygame.key.get_pressed()
    moved = False

    if keys[left_key]:
        player_car.rotate(left=True)
    if keys[right_key]:
        player_car.rotate(right=True)
    if keys[forward_key]:
        moved = True
        player_car.move_forward()
    if keys[backward_key]:
        moved = True
        player_car.move_backward()
    
    if not moved:
        player_car.reduce_speed()



###################
#### Display ###### 
###################

#display of text & players
def draw(win, images, player_car1, player_car2):
    for img, pos in images:
        win.blit(img, pos)
    
    global font_scale
    global text_scale_factor
    global MAIN_FONT

    MAIN_FONT = pygame.font.SysFont("comicsans", font_scale)
    
    # FPS text
    level_text = MAIN_FONT.render(
        f"FPS: {clock}", 1, (255, 255, 255))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() +10))

    # display player 1
    player_car1.draw(win)
 
    # display player 2 
    if player_mode == 2:
        player_car2.draw(win)

    # pygame.display.update()
   
# function to display laptime
def displayLaptime(win, player, playerLaptime, yAxis):
    global MAIN_FONT

    MAIN_FONT = pygame.font.SysFont("comicsans", font_scale)

    # if playerLaptime[0] > 0:
    if playerLaptime[0] > 0:
        level_text = MAIN_FONT.render(
            f"laptime (s) {player}: {math.trunc(playerLaptime[0])}", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() + yAxis * scale_factor))
    else:
        level_text = MAIN_FONT.render(
            f"laptime (s) {player}: /", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() + yAxis * scale_factor))


def displayLapcount(win, player, playerLapcount, yAxis):

    level_text = MAIN_FONT.render(
        f"lapcount {player}: {playerLapcount[0]}", 1, (0, 255, 0))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() + yAxis * scale_factor))



win_text = 0

def wonText(win_text1, win_text2, lapcountP1, lapcountP2):

    global won
    global count_text 

    toAbsolveLaps = 6 

    if won == True:
        #won text
        if count_text < 0:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)

        if lapcountP1[0] >= toAbsolveLaps:
            win_text = win_text1
        elif lapcountP2[0] >= toAbsolveLaps:
            win_text = win_text2
            
        MAIN_FONT = pygame.font.SysFont("comicsans", 5 * font_scale)
        level_text = MAIN_FONT.render(
            f"{win_text}", 1, (color))
        WIN.blit(level_text, (275 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))

    #blinking "won text" for player 
    if lapcountP1[0] >= toAbsolveLaps or lapcountP2[0] >= toAbsolveLaps:

        won = True
        if count_text < 70:
            count_text += 1 
        else:
            count_text -= 140 


#countdown 
countdown_run = True
def countdown():
   
    global countdown_run

    image = countdown_bg
    color = (255, 0, 0)
    countdown_no = 3

    MAIN_FONT = pygame.font.SysFont("comicsans", 10 * font_scale)

    while countdown_run == True:
        if countdown_no == 2:
            color = (0, 0, 255)
        elif countdown_no == 1:
            color = (0, 255, 0)
        
        WIN.blit(image, (0, 0))
        
        level_text = MAIN_FONT.render(
            f"{countdown_no}", 1, (color))
        WIN.blit(level_text, (475 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))
        pygame.display.update()
        
        time.sleep(1)
        countdown_no -= 1

        WIN.fill((0,0,0))       

        if countdown_no == 0:
            countdown_run = False



################
#### Stats #####
################

#lapcount
def lapcount_collision(player_car, lapcount, last_collision_time):
    current_time = time.time()
    if current_time - last_collision_time[0] >= collision_delay:
        computer_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide is not None:
            lapcount[0] += 1
            last_collision_time[0] = current_time



# laptime
def laptime(player_car, playerName, last_collision_time_laptime, lastTouch1, lastTouch2, lapcount, start1, start2, end1, end2, final_laptime):
    # global last_collision_time_laptime, lastTouch1, lastTouch2, lapcount1, start1, start2, end1, end2, final_laptime
    current_time = time.time()

    if current_time - last_collision_time_laptime[0] >= collision_delay:
        computer_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
        
        if computer_finish_poi_collide is not None and lastTouch1[0] == 0:
            start1[0] = time.time()
            lastTouch1[0] = lastTouch1[0] + 1
            last_collision_time_laptime[0] = time.time() 

        elif computer_finish_poi_collide is not None and lastTouch1[0] == 1:
            end1[0] = time.time()
            final_laptime[0] = (end1[0] - start1[0])
            lastTouch1[0] = lastTouch1[0] - 1
            last_collision_time_laptime[0] = current_time
            print(playerName, "Lap:", lapcount[0] - 1, ":", final_laptime[0])

        if computer_finish_poi_collide is not None and lastTouch1[0] == 0:
            start2[0] = time.time()
            lastTouch2[0] = lastTouch2[0] + 1
            last_collision_time_laptime[0] = current_time

        elif computer_finish_poi_collide is not None and lastTouch1[0] == 1 and lastTouch2[0] == 1:
            end2[0] = time.time()
            final_laptime[0] = (end2[0] - start2[0])
            lastTouch2[0] = lastTouch2[0] - 1
            last_collision_time_laptime[0] = current_time
            print(playerName, "Lap:", lapcount[0] - 1, ":", final_laptime[0])



#changes the speed of the players and adjusts to the right start angle when the FPS count is choosen
if FPS == 1:
    player_car1 = PlayerCar1(3, 5)
    player_car2 = PlayerCar2(3, 5)
    fpsClock = 144
    
    if player_mode == 2:
        # adjusts players start angle
        count = 0
        while count < 72:
            player_car1.rotate(left=True)
            player_car2.rotate(left=True)
            count = count + 1
    else:
        count = 0
        while count < 72:
            player_car1.rotate(left=True)
            count = count + 1

elif FPS == 2:
    player_car1 = PlayerCar1(3, 9)
    player_car2 = PlayerCar2(3, 9)
    fpsClock = 85 
    
    if player_mode == 2:
    #adjusts players start angle
        count = 0
        while count < 40:
            player_car1.rotate(left=True)
            player_car2.rotate(left=True)
            count = count + 1
    else:
    #adjusts players start angle
        count = 0
        while count < 40:
            player_car1.rotate(left=True)
            count = count + 1
else:
    print("ERROR: Please enter a valid FPS number!")



clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
run = True


# countdown()
# game loop
while  run:
    clock.tick(fpsClock)

    draw(WIN, images, player_car1, player_car2)
    displayLaptime(WIN, "P1", final_laptimeP1, 490)
    displayLapcount(WIN, "P1", lapcountP1, 490)
    wonText(win_text1, win_text2, lapcountP1, lapcountP2);


    # player Nr.1 control
    # move_player1(player_car1)
    move_player(player_car1, "K_d", "K_a", "K_w", "K_s")
    if player_car1.collide(TRACK_BORDER_MASK) != None:
        player_car1.bounce()
   
    # lapcount: collision with finishline for player 1 
    lapcount_collision(player_car1, lapcountP1, last_collision_timeP1)
   
    # laptime
    laptime(player_car1, "Player 1", last_collision_time_laptimeP1, lastTouch1P1, lastTouch2P1, lapcountP1, start1P1, start2P1, end1P1, end2P1, final_laptimeP1)

    # if player 2
    if player_mode == 2:
        # laptime & lapcount
        displayLaptime(WIN, "P2", final_laptimeP2, 510)
        displayLapcount(WIN, "P2", lapcountP2, 510)
        
        # movement player 2
        move_player(player_car2, "K_l", "K_j", "K_i", "K_k")
        if player_car2.collide(TRACK_BORDER_MASK) != None:
            player_car2.bounce()

        # lapcount: collision with finishline for player 2
        lapcount_collision(player_car2, lapcountP2, last_collision_timeP2)
        # laptime player 2
        laptime(player_car2, "Player 2", last_collision_time_laptimeP2, lastTouch1P2, lastTouch2P2, lapcountP2, start1P2, start2P2, end1P2, end2P2, final_laptimeP2)

    # cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
