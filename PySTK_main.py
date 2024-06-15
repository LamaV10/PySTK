#import
import pygame
import time
import math
from pygame import mixer
from utils import scale_image, blit_rotate_center
pygame.init()

#Bruno Banani

#music import/play
#mixer.music.load("music/yourtitel.mp3")
#mixer.music.set_volume(0.5)
#mixer.music.play(-1)


#85 FPS is easier to play and works great on smaller screens (like laptops)
#FPS_input = input('(144) or (85) FPS:')
FPS = int(input("144 FPS or 85:"))

#factors: help to adjust to different resolutions
scale_factor = float(input("Choose scale-factor:"))

scale_player = 0.1 * scale_factor
START_POS_X = 390 * scale_factor
START_POS_Y = 433 * scale_factor

Finish_POS_X = 305 * scale_factor  
Finish_POS_Y = 460 * scale_factor


#Track and Mask
TRACK = scale_image(pygame.image.load("imgs/rennstrecke.jpg"), scale_factor)
TRACK_BORDER = scale_image(pygame.image.load("imgs/rennstrecke_mask_s.xcf"), scale_factor)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)


#finish line Mask
FINISH = pygame.image.load("imgs/finish-line.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (Finish_POS_X, Finish_POS_Y)


#window setup
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SuperTuxKart")
MAIN_FONT = pygame.font.SysFont("comicsans", 32)


#Racer Nr.1
racer1 = scale_image(pygame.image.load("imgs/tuxi.xcf"), scale_player)

#stat count
stat1 = 0

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = 0.25 * rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS_SCALE
        self.acceleration = 0.1

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
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    
    def finish_line(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi



class PlayerCar(AbstractCar):
    IMG = racer1
    START_POS_SCALE = (START_POS_X, START_POS_Y)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.5
        self.move()


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"FPS: {clock}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - TRACK.get_height() +5))

    level_text = MAIN_FONT.render(
       f"lapcount P1: {lapcount1}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - TRACK.get_height() +490 * scale_factor))

    player_car.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    
    if not moved:
        player_car.reduce_speed()


       
#lapcount
# Timer for the Lapcount-collision
last_collision_time1 = 0
last_collision_time2 = 0
collision_delay = 5  # Sekunden


lapcount1 = 0
def lapcount_collision(player_car1):
    global lapcount1, last_collision_time1
    current_time = time.time()
    if current_time - last_collision_time1 >= collision_delay:
        computer_finish_poi_collide = player_car1.collide(FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide is not None:
            lapcount1 += 1
            last_collision_time1 = current_time

#changes the speed of the players and adjusts to the right start angle when the FPS count is choosen
if FPS == 144:
    player_car = PlayerCar(3, 4)
    #adjusts players start angle
    count = 0
    while count < 90:
        player_car.rotate(left=True)
        count = count + 1

if FPS == 85:
    player_car = PlayerCar(3, 8)
    #adjusts players start angle
    count = 0
    while count < 45:
        player_car.rotate(left=True)
        count = count + 1

clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
run = True


    
while  run:
    #game loop setup
    draw(WIN, images, player_car, )
    clock.tick(FPS)
     

    #player Nr.1 control
    move_player(player_car)
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    lapcount_collision(player_car)

    #cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
