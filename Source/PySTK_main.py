import pygame
import time
import math
import os

import music
from setup import *
from utils import scale_image, blit_rotate_center
pygame.init()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_terminal()
music.music()

# choose mode (single- or multiplayer)
clear_terminal()
player_mode = int(input("Singleplayer (1) or Multiplayer (2): "))
clear_terminal()

# choose if you want to play on 85 or 144
# 85 FPS is easier to play and works great on smaller screens (like laptops)
clear_terminal()
print("Choose 144 FPS if you put the scale size over 1.8")
FPS = int(input("144 FPS (1) or 85 FPS (2): "))

# window setup
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PySTK")
MAIN_FONT = pygame.font.SysFont("comicsans", 32)

print("scale factor:", scale_factor)


##############
#### Car #####
##############

# car class -> physics
class AbstractCar:
    def __init__(self, max_vel, rotation_vel, img, mask, pos_x, pos_y):
        self.img = img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = 0.25 * rotation_vel
        self.angle = 0
        self.x = pos_x
        self.y = pos_y
        self.acceleration = 0.1
        self.mask = mask

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

    # def reset(self):
    #     self.x
    #     self.y = self.START_POS
    #     self.angle = 0
    #     self.vel = 0


###################
#### Players ######
###################

class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, img, mask, pos_x, pos_y, name, last_touch=None, laptime=None):
        super().__init__(max_vel, rotation_vel, img, mask, pos_x, pos_y)
        self.name = name
        self.last_touch = last_touch if last_touch is not None else [0, 0]
        self.laptime = laptime if laptime is not None else [0, 0, 0, 0]
        self.final_laptime = [0]

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.9
        self.move()



# player keybinds
# takes in the player (for example playerCar1 or playerCar2)
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

# draw the text & players
def draw(win, images, playerCar1, playerCar2):
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
    playerCar1.draw(win)

    # display player 2
    if player_mode == 2:
        playerCar2.draw(win)

    # pygame.display.update()


win_text = 0
def wonText(win_text1, win_text2, lapcount_P1, lapcountP2):
    global won_P1
    global won_P2
    global count_text

    to_absolve_laps = 6

    # check if the players absolved the laps, that are needed for a win
    if lapcount_P1[0] >= to_absolve_laps:
        won_P1 = True
    elif lapcountP2[0] >= to_absolve_laps:
        won_P2 = True

    # if one player has won
    if won_P1 == True or won_P2 == True:
        # red text if count_text is bigger then 0
        if count_text < 0:
            color = (255, 0, 0)
        # green text if this is not the case
        else:
            color = (0, 255, 0)

        # loops through count_text -> used to change colors after a certain time
        if count_text < 70:
            count_text += 1
        else:
            count_text -= 140

        # sets which text is going to be displayed
        if lapcount_P1[0] >= to_absolve_laps and not won_P2 == True:
            win_text = win_text1
        elif lapcountP2[0] >= to_absolve_laps:
            win_text = win_text2

        # display won text
        MAIN_FONT = pygame.font.SysFont("comicsans", 5 * font_scale)
        level_text = MAIN_FONT.render(
            f"{win_text}", 1, (color))
        WIN.blit(level_text, (275 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))


# countdown
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

        WIN.fill((0, 0, 0))

        if countdown_no == 0:
            countdown_run = False


################
#### Stats #####
################

# measurment and display of the laptime
def display_laptime(win, pPlayerCar, name, y_axis):
    global MAIN_FONT
    MAIN_FONT = pygame.font.SysFont("comicsans", font_scale)

    if pPlayerCar.final_laptime[0] > 0:
        level_text = MAIN_FONT.render(
            f"laptime (s) {name}: {math.trunc(pPlayerCar.final_laptime[0])}", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() + y_axis * scale_factor))
    else:
        level_text = MAIN_FONT.render(
            f"laptime (s) {name}: /", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() + y_axis * scale_factor))

# lapcount from players
def display_lapcount(win, player, player_lapcount, y_axis):
    level_text = MAIN_FONT.render(
        f"lapcount {player}: {player_lapcount[0]}", 1, (0, 255, 0))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() + y_axis * scale_factor))



# lapcount
def lapcount_collision(pPlayerCar, lapcount, last_collision_time):
    current_time = time.time()
    if current_time - last_collision_time[0] >= collision_delay:
        computer_finish_poi_collide = pPlayerCar.collide(FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide is not None:
            lapcount[0] += 1
            last_collision_time[0] = current_time



# laptime
def laptime(pPlayerCar, last_collision_time_laptime, lapcount):
    current_time = time.time()

    if current_time - last_collision_time_laptime[0] >= collision_delay:
        computer_finish_poi_collide = pPlayerCar.collide(FINISH_MASK, *FINISH_POSITION)

        # if player crosses finish line and last_touch1 = 0 (for laptime lap 1,3,5 ...)
        if computer_finish_poi_collide is not None and pPlayerCar.last_touch[0] == 0:
            pPlayerCar.laptime[0] = time.time()
            pPlayerCar.last_touch[0] =  1
            last_collision_time_laptime[0] = time.time()

        elif computer_finish_poi_collide is not None and pPlayerCar.last_touch[0] == 1:
            pPlayerCar.laptime[1] = time.time()
            pPlayerCar.last_touch[0] =  0
            last_collision_time_laptime[0] = current_time
            pPlayerCar.final_laptime[0] = pPlayerCar.laptime[1] - pPlayerCar.laptime[0]
            print(pPlayerCar.name, "Lap:", lapcount[0] - 1, ":", pPlayerCar.final_laptime[0])

        # if player crosses finish line and last_touch1 = 0 (for laptime lap 2,4,6 ...)
        if computer_finish_poi_collide is not None and pPlayerCar.last_touch[0] == 0:
            pPlayerCar.laptime[2] = time.time()
            pPlayerCar.last_touch[1] = 1
            last_collision_time_laptime[0] = current_time

        elif computer_finish_poi_collide is not None and pPlayerCar.last_touch[0] == 1 and pPlayerCar.last_touch[1] == 1:
            pPlayerCar.laptime[3] = time.time()
            pPlayerCar.last_touch[1] = 0
            last_collision_time_laptime[0] = current_time
            pPlayerCar.final_laptime[0] = pPlayerCar.laptime[3] - pPlayerCar.laptime[2]
            print(pPlayerCar.name, "Lap:", lapcount[0] - 1, ":", pPlayerCar.final_laptime[0])



# changes the speed of the players and adjusts to the right start angle when the FPS count is choosen
if FPS == 1:
    playerCar1 = PlayerCar(3, 5, racer1, racer1_mask, 410 * scale_factor, 428 * scale_factor, "Player 1")
    playerCar2 = PlayerCar(3, 5, racer2, racer2_mask, 345 * scale_factor, 478 * scale_factor, "Player 2")
    fpsClock = 144

    if player_mode == 2:
        # adjusts players start angle
        count = 0
        while count < 72:
            playerCar1.rotate(left=True)
            playerCar2.rotate(left=True)
            count = count + 1
    else:
        count = 0
        while count < 72:
            playerCar1.rotate(left=True)
            count = count + 1

elif FPS == 2:
    playerCar1 = PlayerCar(3, 9, racer1, racer1_mask, 410 * scale_factor, 428 * scale_factor, "Player 1")
    playerCar2 = PlayerCar(3, 9, racer2, racer2_mask, 345 * scale_factor, 478 * scale_factor, "Player 2")
    fpsClock = 85

    if player_mode == 2:
        # adjusts players start angle
        count = 0
        while count < 40:
            playerCar1.rotate(left=True)
            playerCar2.rotate(left=True)
            count = count + 1
    else:
        # adjusts players start angle
        count = 0
        while count < 40:
            playerCar1.rotate(left=True)
            count = count + 1
else:
    print("ERROR: Please enter a valid FPS number!")




clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
run = True

print(fpsClock)
# countdown()
# game loop
while run:
    clock.tick(fpsClock)

    draw(WIN, images, playerCar1, playerCar2)
    display_laptime(WIN, playerCar1, "P1", 490)
    display_lapcount(WIN, "P1", lapcount_P1, 490)
    wonText(win_text1, win_text2, lapcount_P1, lapcount_P2);


    # player Nr.1 control
    # move_player1(playerCar1)
    move_player(playerCar1, "K_d", "K_a", "K_w", "K_s")
    if playerCar1.collide(TRACK_BORDER_MASK) != None:
        playerCar1.bounce()

    # lapcount: colliion with finishline for player 1
    lapcount_collision(playerCar1, lapcount_P1, last_collision_timeP1)
    laptime(playerCar1, last_collision_time_laptimeP1, lapcount_P1)

    # if player 2
    if player_mode == 2:
        # laptime & lapcount
        display_laptime(WIN, playerCar2, "P2", 510)
        display_lapcount(WIN, "P2", lapcount_P2, 510)

        # movement player 2
        move_player(playerCar2, "K_l", "K_j", "K_i", "K_k")
        if playerCar2.collide(TRACK_BORDER_MASK) != None:
            playerCar2.bounce()

        # lapcount: collision with finishline for player 2
        lapcount_collision(playerCar2, lapcount_P2, last_collision_timeP2)
        laptime(playerCar2, last_collision_time_laptimeP2, lapcount_P2)

    # cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
