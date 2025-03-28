import copy

import pygame
from board import boards
import math

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = copy.deepcopy(boards)
color = 'red'
PI = math.pi
SMALL_SCORE = 10
BIG_SCORE = 50
HEIGHT_LINE = 32
WIDTH_LINE = 30
COUNTER_BORDER = 600
START_SCORE_BORDER = 100
ADD_COORD_GHOST = 22
ADD_COORD = 23
CENTER_X_BORDER = 29
GHOST_X_LEFT = 12
GHOST_X_RIGHT = 18
GHOST_BORDER_L = 340
GHOST_BORDER_RX = 560
GHOST_BORDER_RY = 500
IMG_SIZE = 45

player_x = WIDTH // 2
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 740
inky_y = 680
inky_direction = 2
pinky_x = 200
pinky_y = 580
pinky_direction = 2
clyde_x = 650
clyde_y = 410
clyde_direction = 2
targets = [(player_x, player_y), (player_x, player_y),
           (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
ghost_speeds = [3, 3, 3, 3]
counter = 0
flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 3
score = 0
powerup = False
power_counter = 0
eaten = [False, False, False, False]
moving = False
startup_score = 0
lives = 3
game_over = False
game_won = False
