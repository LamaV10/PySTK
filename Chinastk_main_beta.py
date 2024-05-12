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


#Track and Mask
scale_factor = 2.3
TRACK = scale_image(pygame.image.load("imgs/rennstrecke.jpg"), scale_factor)
TRACK_BORDER = scale_image(pygame.image.load("imgs/rennstrecke_mask_s.xcf"), scale_factor)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

#finish line Mask
FINISH_BORDER = scale_image(pygame.image.load("imgs/finish-line.png"), scale_factor)
FINISH_BORDER_MASK = pygame.mask.from_surface(FINISH_BORDER)



#window setup
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SuperTuxKart")
FPS = 144

#Racer Nr.1
racer1 = scale_image(pygame.image.load("imgs/tuxi.xcf"), 0.2)

#Racer Nr.2
racer2 = scale_image(pygame.image.load("imgs/yoshi.xcf"), 0.30)
player2 = pygame.Rect((930, 1130, 100, 100))
movement2 = racer2.get_rect()

#stat count
stat1 = 0

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = 0.25 * rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
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
    START_POS = (400, 600)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.25
        self.move()


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

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


clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
player_car = PlayerCar(3, 5)
run = True

while  run:
    #game loop setup
    draw(WIN, images, player_car, )
    #WIN.blit(racer2, player2)
    clock.tick(FPS)

    #player Nr.1 control
    move_player(player_car)
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
        #print("collide")

    #if player_car.finish_line(finish_line) != None:
     #   stat1 = stat1 + 1
      #  sleep(3)
        

    #player Nr.2 control
    key2 = pygame.key.get_pressed()
    if key2[pygame.K_j] and player2.x - PLAYER_VEL >= 0:
        player2.move_ip(-5, 0)
    if key2[pygame.K_l] and player2.x - PLAYER_VEL + PLAYER_WIDTH <= 2500:
        player2.move_ip(5, 0)
    if key2[pygame.K_i] and player2.y - PLAYER_VEL >= 0:
        player2.move_ip(0, -5)
    if key2[pygame.K_k] and player2.y - PLAYER_VEL + PLAYER_WIDTH <= 1380:
        player2.move_ip(0, 5)

    #cloeses the windows if run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
