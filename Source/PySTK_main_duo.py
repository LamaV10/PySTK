#mport
import pygame
import time
import math

import music
music.music()

from utils import scale_image, blit_rotate_center
pygame.init()


#choose if you want to play on 85 or 144
#85 FPS is easier to play and works great on smaller screens (like laptops)
#FPS_input = input('(144) or (85) FPS:')
print("Choose 144 FPS if you put the scale size over 1.8")
FPS = int(input("144 FPS or 85: "))

#factors: help to adjust to different resolutions
scale_factor = float(input("Choose scale-factor: "))


scale_player = 0.02 * scale_factor
font_size = 32 * scale_factor

#start position
START_POS_X1 = 410 * scale_factor
START_POS_Y1 = 428 * scale_factor

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
pygame.display.set_caption("SuperTuxKart")
MAIN_FONT = pygame.font.SysFont("comicsans", 32)

#text scale factor
text_scale_factor = TRACK.get_width() * 0.00088
font_scale = math.trunc(15 * scale_factor)

#Racer Nr.1
racer1 = scale_image(pygame.image.load("imgs/Tux/ferrari-rossa-tux.png"), scale_player)
racer1_mask = scale_image(pygame.image.load("imgs/Tux/ferrari-rossa-tux-mask.png"), scale_player)

#Racer Nr.2
racer2 = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi.png"), scale_player)
racer2_mask = scale_image(pygame.image.load("imgs/Yoshi/chevyss-yoshi-mask.png"), scale_player)

#won utilities
win_text1 = "Player 1 has won!!!"
win_text2 = "Player 2 has won!!!"
won1 = False
won2 = False
count_text = 0


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
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
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

#keybinds player 1
def move_player1(player_car1):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car1.rotate(left=True)
    if keys[pygame.K_d]:
        player_car1.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car1.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car1.move_backward()
    
    if not moved:
        player_car1.reduce_speed()


#keybinds player  22 
def move_player2(player_car2):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_j]: 
        player_car2.rotate(left=True)
    if keys[pygame.K_l]:
        player_car2.rotate(right=True)
    if keys[pygame.K_i]:
        moved = True
        player_car2.move_forward()
    if keys[pygame.K_k]:
        moved = True
        player_car2.move_backward()
    
    if not moved:
        player_car2.reduce_speed()



###################
#### Display ###### 
###################

#display of text & players
def draw(win, images, player_car1, player_car2):
    for img, pos in images:
        win.blit(img, pos)
    
    global won1
    global won2 

    global font_scale
    global text_scale_factor
    global MAIN_FONT

    MAIN_FONT = pygame.font.SysFont("comicsans", font_scale)
    
    #FPS text
    level_text = MAIN_FONT.render(
        f"FPS: {clock}", 1, (255, 255, 255))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() +10))

    #lapcount text 
    level_text = MAIN_FONT.render(
       f"lapcount P1: {lapcount1}", 1, (0, 255, 0))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() +490 * scale_factor))


    level_text = MAIN_FONT.render(
        f"lapcount P2: {lapcount2}", 1, (0, 255, 0))
    WIN.blit(level_text, (10, HEIGHT - TRACK.get_height() +510 * scale_factor))



    #laptime text P1
    if (final_laptime1) > 0:
        level_text = MAIN_FONT.render(
            f"laptime (s) P1: {math.trunc(final_laptime1)}", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() +490 * scale_factor))
    else:
        level_text = MAIN_FONT.render(
            f"laptime (s) P1: /", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() +490 * scale_factor))
   
    #laptime text P2
    if (final_laptime2) > 0:
        level_text = MAIN_FONT.render(
            f"laptime (s) P2: {math.trunc(final_laptime2)}", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() +510 * scale_factor))
    else:
        level_text = MAIN_FONT.render(
            f"laptime (s) P2: /", 1, (0, 0, 255))
        win.blit(level_text, (1040 * text_scale_factor, HEIGHT - TRACK.get_height() +510 * scale_factor))
    
    

    #won text
    if won1 == True:
        global count_text
        
        if count_text < 30:
            color = (0, 255, 0)
        if count_text < 0:
            color = (255, 0, 0)
            
        MAIN_FONT = pygame.font.SysFont("comicsans", 5 * font_scale)
        level_text = MAIN_FONT.render(
            f"{win_text1}", 1, (color))
        WIN.blit(level_text, (275 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))

    #blinking "won text"
    if lapcount1 >= 6:

        won1 = True
        if count_text <= 20:
            count_text += 1 

        elif count_text > 5:
            count_text -=40




    if won2 == True:
        
        if count_text < 30:
            color = (0, 255, 0)
        if count_text < 0:
            color = (255, 0, 0)
            
        MAIN_FONT = pygame.font.SysFont("comicsans", 5 * font_scale)
        level_text = MAIN_FONT.render(
            f"{win_text2}", 1, (color))
        WIN.blit(level_text, (275 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))

    #blinking "won text"
    if lapcount2 >= 6:

        won2 = True
        if count_text <= 20:
            count_text += 1 

        elif count_text > 5:
            count_text -=40


    player_car1.draw(win)
    player_car2.draw(win)
    pygame.display.update()


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
            color = (255, 255, 0)
        
        if countdown_no == 1:
            color = (0, 255, 0)
        
        WIN.blit(image, (0, 0))
        
        level_text = MAIN_FONT.render(
            f"{countdown_no}", 1, (color))
        WIN.blit(level_text, (475 * scale_factor, HEIGHT - TRACK.get_height() +260 * scale_factor))
        pygame.display.update()
        
        countdown_no -= 1
        time.sleep(1)

        WIN.fill((0,0,0))       

        if countdown_no == 0:
            countdown_run = False



################
#### Stats #####
################

#lapcount
# Timer for the Lapcount-collision
last_collision_time1 = 0
last_collision_time2 = 0
collision_delay = 10 # Sekunden


lapcount1 = 0
def lapcount_collision1(player_car1):
    global lapcount1, last_collision_time1
    current_time = time.time()
    if current_time - last_collision_time1 >= collision_delay:
        computer_finish_poi_collide = player_car1.collide(FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide is not None:
            lapcount1 += 1
            last_collision_time1 = current_time



lapcount2 = 0
def lapcount_collision2(player_car2):
    global lapcount2, last_collision_time2
    current_time = time.time()
    if current_time - last_collision_time2 >= collision_delay:
        computer_finish_poi_collide = player_car2.collide(FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide is not None:
            lapcount2 += 1
            last_collision_time2 = current_time




#laptime1
last_collision_time_laptime1 = 0

lastTouch1 = 0
lastTouch2 = 0

start1 = 0 
start2 = 0 

end1 = 0
end2 = 0

final_laptime1 = 0 

def laptime1(player_car1):
    global last_collision_time_laptime1, lastTouch1, lastTouch2, lapcount1, start1, start2, end1, end2, final_laptime1
    current_time = time.time()
    
    if current_time - last_collision_time_laptime1 >= collision_delay:
        computer_finish_poi_collide = player_car1.collide(FINISH_MASK, *FINISH_POSITION)
        
        if computer_finish_poi_collide is not None and lastTouch1 == 0:
            start1 = time.time()
            lastTouch1 = lastTouch1 + 1
            last_collision_time_laptime1 = current_time
            #print(lastTouch1)

        elif computer_finish_poi_collide is not None and lastTouch1 == 1:
            end1 = time.time()
            final_laptime1 = (end1 - start1)
            lastTouch1 = lastTouch1 - 1
            last_collision_time_laptime1 = current_time
            print("P1:", final_laptime1)
            #print(lastTouch1)

        if computer_finish_poi_collide is not None and lastTouch1 == 0 and lapcount1 ==2:
            start2 = time.time()
            lastTouch2 = lastTouch2 + 1
            last_collision_time_laptime1 = current_time
            #print("2:", lastTouch2)

        elif computer_finish_poi_collide is not None and lastTouch1 == 1 and lastTouch2 == 1 and lapcount1 == 3:
            end2 = time.time()
            final_laptime1 = (end2 - start2)
            lastTouch2 = lastTouch2 - 1
            last_collision_time_laptime1 = current_time
            print("P1:", final_laptime1)
           #print("2:", lastTouch2)


#laptime2
last_collision_time_laptime2 = 0

lastTouch3 = 0
lastTouch4 = 0

start3 = 0 
start4 = 0 

end3 = 0
end4 = 0

final_laptime2 = 0

def laptime2(player_car2):
    global last_collision_time_laptime2, lastTouch3, lastTouch4, lapcount2, start3, start4, end3, end4, final_laptime2
    current_time = time.time()
    
    if current_time - last_collision_time_laptime2 >= collision_delay:
        computer_finish_poi_collide = player_car2.collide(FINISH_MASK, *FINISH_POSITION)
        
        if computer_finish_poi_collide is not None and lastTouch3 == 0:
            start3 = time.time()
            lastTouch3 = lastTouch3 + 1
            last_collision_time_laptime2 = current_time
            #print("lastTouch3:", lastTouch3)

        elif computer_finish_poi_collide is not None and lastTouch3 == 1:
            end3 = time.time()
            final_laptime2 = (end3 - start3)
            lastTouch3 = lastTouch3 - 1
            last_collision_time_laptime2 = current_time
            print("P2:", final_laptime2)
            #print("lastTouch3:", lastTouch3)

        if computer_finish_poi_collide is not None and lastTouch4 == 0 and lapcount2 ==2:
            start4 = time.time()
            lastTouch4 = lastTouch4 + 1
            last_collision_time_laptime2 = current_time
            #print("lastTouch4:", lastTouch4)

        elif computer_finish_poi_collide is not None and lastTouch4 == 1 and lastTouch3 == 1 and lapcount2 == 3:
            end4 = time.time()
            final_laptime2 = (end4 - start4)
            lastTouch4 = lastTouch4 - 1
            last_collision_time_laptime2 = current_time
            print("P2:", final_laptime2)
            #print("lastTouch4:", lastTouch4)




#changes the speed of the players and adjusts to the right start angle when the FPS count is choosen
if FPS == 144:
    player_car1 = PlayerCar1(3, 5)
    player_car2 = PlayerCar2(3, 5)

    #adjusts players start angle
    count = 0
    while count < 72:
        player_car1.rotate(left=True)
        player_car2.rotate(left=True)
        count = count + 1

if FPS == 85:
    player_car1 = PlayerCar1(3, 9)
    player_car2 = PlayerCar2(3, 9)

    #adjusts players start angle
    count = 0
    while count < 40:
        player_car1.rotate(left=True)
        player_car2.rotate(left=True)
        count = count + 1

clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
run = True

#game loop
while  run:
    countdown()
    draw(WIN, images, player_car1, player_car2)
    clock.tick(FPS)

    #player Nr.1 control
    move_player1(player_car1)
    if player_car1.collide(TRACK_BORDER_MASK) != None:
        player_car1.bounce()
    
    #player Nr.2 control
    move_player2(player_car2)
    if player_car2.collide(TRACK_BORDER_MASK) != None:
        player_car2.bounce()
    

    #lapcount (who would have thought)
    lapcount_collision1(player_car1)
    lapcount_collision2(player_car2)
   
    #laptime
    laptime1(player_car1)
    laptime2(player_car2)

    #cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
