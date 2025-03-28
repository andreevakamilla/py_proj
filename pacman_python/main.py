import copy

import pygame
from board import boards
import Ghost
import draw
import base
import os

pygame.init()


path_directory = os.path.dirname(__file__)
pygame.mixer.music.load(os.path.join(path_directory, 'sound/nyan-cat_1.mp3'))
pygame.mixer.music.play(-1)

def default():
    base.lives -= 1
    base.startup_counter = 0
    base.powerup = False
    base.power_counter = 0
    base.player_x = 450
    base.player_y = 663
    base.direction = 0
    base.direction_command = 0
    base.blinky_x = 56
    base.blinky_y = 58
    base.blinky_direction = 0
    base.inky_x = 740
    base.inky_y = 680
    base.inky_direction = 2
    base.pinky_x = 200
    base.pinky_y = 580
    base.pinky_direction = 2
    base.clyde_x = 650
    base.clyde_y = 410
    base.clyde_direction = 2
    base.eaten = [False, False, False, False]
    base.blinky_dead = False
    base.inky_dead = False
    base.clyde_dead = False
    base.pinky_dead = False

def check_collisions(skore, power, power_count, eat):
    num1 = (base.HEIGHT - base.BIG_SCORE) // base.HEIGHT_LINE
    num2 = (base.WIDTH // base.WIDTH_LINE)
    if 0 < base.player_x < base.WIDTH - base.WIDTH_LINE:
        if base.level[center_y // num1][center_x // num2] == 1:
            base.level[center_y // num1][center_x // num2] = 0
            skore += base.SMALL_SCORE
        if base.level[center_y // num1][center_x // num2] == 2:
            base.level[center_y // num1][center_x // num2] = 0
            skore += base.BIG_SCORE
            power = True
            power_count = 0
            eat = [False, False, False, False]
    return skore, power, power_count, eat


def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = (base.HEIGHT - base.BIG_SCORE) // base.HEIGHT_LINE
    num2 = (base.WIDTH // base.WIDTH_LINE)
    num3 = 15
    if center_x // base.WIDTH_LINE < base.CENTER_X_BORDER:
        if base.direction == 0:
            if base.level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[1] = True
        if base.direction == 1:
            if base.level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[0] = True
        if base.direction == 2:
            if base.level[(center_y + num3) // num1][center_x // num2] < 3:
                turns[3] = True
        if base.direction == 3:
            if base.level[(center_y - num3) // num1][center_x // num2] < 3:
                turns[2] = True
        if base.direction == 2 or base.direction == 3:
            if base.GHOST_X_LEFT <= center_x % num2 <= base.GHOST_X_RIGHT:
                if base.level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[3] = True
                if base.level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[2] = True
            if base.GHOST_X_LEFT <= center_y % num1 <= base.GHOST_X_RIGHT:
                if base.level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if base.level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[0] = True
        if base.direction == 0 or base.direction == 1:
            if base.GHOST_X_LEFT <= center_x % num2 <= base.GHOST_X_RIGHT:
                if base.level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if base.level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            if base.GHOST_X_LEFT <= center_y % num1 <= base.GHOST_X_RIGHT:
                if base.level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if base.level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True
    return turns


def move_pacman(play_x, play_y):
    if base.direction == 0 and turns_allowed[0]:
        play_x += base.player_speed
    elif base.direction == 1 and turns_allowed[1]:
        play_x -= base.player_speed
    elif base.direction == 2 and turns_allowed[2]:
        play_y -= base.player_speed
    elif base.direction == 3 and turns_allowed[3]:
        play_y += base.player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y,
                pink_x, pink_y, clyd_x, clyd_y):
    def target_logic(ghost_x, ghost_y, dead_status, eaten_status):
        if not dead_status:
            if base.GHOST_BORDER_L < ghost_x < base.GHOST_BORDER_RX and base.GHOST_BORDER_L < ghost_y < base.GHOST_BORDER_RY:
                return (400, base.START_SCORE_BORDER)
            else:
                return (base.player_x, base.player_y)
        elif not eaten_status:
            return (runaway_x, runaway_y)
        else:
            return return_target

    if base.player_x < 450:
        runaway_x, runaway_y = 900, 0
    else:
        runaway_x, runaway_y = 0, 900

    return_target = (380, 400)
    blink_target = target_logic(blink_x, blink_y, blinky.dead, base.eaten[0])
    ink_target = target_logic(ink_x, base.player_y, inky.dead, base.eaten[1])
    pink_target = target_logic(
        base.player_x,
        pink_y,
        pinky.dead,
        base.eaten[2])
    clyd_target = target_logic(clyd_x, clyd_y, clyde.dead, base.eaten[3])

    if base.powerup:
        return [blink_target, ink_target, pink_target, clyd_target]
    else:
        return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    base.timer.tick(base.fps)

    if base.counter < 19:
        base.counter += 1
        if base.counter > 3:
            base.flicker = False
    else:
        base.counter = 0
        base.flicker = True
    if base.powerup and base.power_counter < base.COUNTER_BORDER:
        base.power_counter += 1
    elif base.powerup and base.power_counter >= base.COUNTER_BORDER:
        base.power_counter = 0
        base.powerup = False
        base.eaten = [False, False, False, False]
    if base.startup_score < 180 and not base.game_over and not base.game_won:
        moving = False
        base.startup_score += 1
    else:
        moving = True
    base.screen.fill('black')
    draw.draw_board(base.level)
    draw.draw_player()
    blinky = Ghost.Ghost(base.blinky_x, base.blinky_y, base.targets[0],
                         base.ghost_speeds[0], draw.blinky_img,
                         base.blinky_direction, base.blinky_dead,
                         base.blinky_box, 0)
    inky = Ghost.Ghost(base.inky_x, base.inky_y, base.targets[1],
                       base.ghost_speeds[1], draw.inky_img,
                       base.inky_direction, base.inky_dead,
                       base.inky_box, 1)
    pinky = Ghost.Ghost(base.pinky_x, base.pinky_y, base.targets[2],
                        base.ghost_speeds[2], draw.pinky_img,
                        base.pinky_direction, base.pinky_dead,
                        base.pinky_box, 2)
    clyde = Ghost.Ghost(base.clyde_x, base.clyde_y, base.targets[3],
                        base.ghost_speeds[3], draw.clyde_img,
                        base.clyde_direction, base.clyde_dead,
                        base.clyde_box, 3)

    draw.draw_misc()
    base.targets = get_targets(
        base.blinky_x,
        base.blinky_y,
        base.inky_x,
        base.inky_y,
        base.pinky_x,
        base.pinky_y,
        base.clyde_x,
        base.clyde_y)
    center_x = base.player_x + base.ADD_COORD
    center_y = base.player_y + base.ADD_COORD
    if base.powerup:
        base.player_speed = 2
        base.ghost_speeds = [5, 5, 5, 5]
    else:
        base.player_speed = 3
        base.ghost_speeds = [3, 3, 3, 3]
    if base.eaten[0]:
        base.ghost_speeds[0] = 2
    if base.eaten[1]:
        base.ghost_speeds[1] = 2
    if base.eaten[2]:
        base.ghost_speeds[2] = 2
    if base.eaten[3]:
        base.ghost_speeds[3] = 2
    if base.blinky_dead:
        base.ghost_speeds[0] = 7
    if base.inky_dead:
        base.ghost_speeds[1] = 7
    if base.pinky_dead:
        base.ghost_speeds[2] = 7
    if base.clyde_dead:
        base.ghost_speeds[3] = 7

    base.game_won = True
    for i in range(len(base.level)):
        if 1 in base.level[i] or 2 in base.level[i]:
            base.game_won = False

    player_circle = pygame.draw.circle(
        base.screen, 'yellow', (center_x + 3, center_y), 9, 1)
    turns_allowed = check_position(center_x, center_y)
    pygame.draw.circle(base.screen, 'red', (center_x, center_y), 2)
    if moving:
        base.player_x, base.player_y = move_pacman(
            base.player_x, base.player_y)
        base.blinky_x, base.blinky_y, base.blinky_direction = blinky.move_ghost()
        base.inky_x, base.inky_y, base.inky_direction = inky.move_ghost()
        base.clyde_x, base.clyde_y, base.clyde_direction = clyde.move_ghost()
        base.pinky_x, base.pinky_y, base.pinky_direction = pinky.move_ghost()

    base.score, base.powerup,base.power_counter, base.eaten = check_collisions(
        base.score, base.powerup, base.power_counter, base.eaten)

    if not base.powerup:
        base.color = "red"
        if ((player_circle.colliderect(blinky.rect) and not blinky.dead) or
                (player_circle.colliderect(inky.rect) and not inky.dead) or
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or
                (player_circle.colliderect(clyde.rect) and not clyde.dead)):
            if base.lives > 0:
                default()
            elif blinky.dead or inky.dead or pinky.dead or clyde.dead:
                base.blinky_dead = False
                base.inky_dead = False
                base.clyde_dead = False
                base.pinky_dead = False
            else:
                base.game_over = True
                moving = False
                startup_counter = 0
    if base.powerup:
        base.color = "blue"
        if player_circle.colliderect(
                blinky.rect) and base.eaten[0] and not blinky.dead:
            if base.lives > 0:
                default()
            else:
                base.game_over = True
                moving = False
                startup_counter = 0
        if player_circle.colliderect(
                inky.rect) and base.eaten[1] and not inky.dead:
            if base.lives > 0:
                default()
            else:
                base.game_over = True
                moving = False
                startup_counter = 0
        if player_circle.colliderect(
                pinky.rect) and base.eaten[2] and not pinky.dead:
            if base.lives > 0:
                default()
            else:
                base.game_over = True
                moving = False
                startup_counter = 0
        if player_circle.colliderect(
                clyde.rect) and base.eaten[3] and not clyde.dead:
            if base.lives > 0:
                default()
            else:
                base.game_over = True
                moving = False
                startup_counter = 0
        if player_circle.colliderect(
                blinky.rect) and not blinky.dead and not base.eaten[0]:
            base.blinky_dead = True
            base.eaten[0] = True
            base.score += (2 ** base.eaten.count(True)) * base.START_SCORE_BORDER
        if player_circle.colliderect(
                inky.rect) and not inky.dead and not base.eaten[1]:
            base.inky_dead = True
            base.eaten[1] = True
            base.score += (2 ** base.eaten.count(True)) * base.START_SCORE_BORDER
        if player_circle.colliderect(
                pinky.rect) and not pinky.dead and not base.eaten[2]:
            base.pinky_dead = True
            base.eaten[2] = True
            base.score += (2 ** base.eaten.count(True)) * base.START_SCORE_BORDER
        if player_circle.colliderect(
                clyde.rect) and not clyde.dead and not base.eaten[3]:
            base.clyde_dead = True
            base.eaten[3] = True
            base.score += (2 ** base.eaten.count(True)) * base.START_SCORE_BORDER

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                base.direction_command = 0
            if event.key == pygame.K_LEFT:
                base.direction_command = 1
            if event.key == pygame.K_UP:
                base.direction_command = 2
            if event.key == pygame.K_DOWN:
                base.direction_command = 3
            if event.key == pygame.K_SPACE and (
                    base.game_over or base.game_won):
                default()
                base.lives = 3
                base.level = copy.deepcopy(boards)
                base.game_won = False
                base.game_over = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and base.direction_command == 0:
                base.direction_command = base.direction
            if event.key == pygame.K_LEFT and base.direction_command == 1:
                base.direction_command = base.direction
            if event.key == pygame.K_UP and base.direction_command == 2:
                base.direction_command = base.direction
            if event.key == pygame.K_DOWN and base.direction_command == 3:
                base.direction_command = base.direction

    for i in range(4):
        if base.direction_command == i and turns_allowed[i]:
            base.direction = i

    if base.player_x > base.WIDTH:
        base.player_x = -base.SMALL_SCORE
    elif base.player_x < -base.SMALL_SCORE:
        base.player_x = base.WIDTH - base.SMALL_SCORE

    if blinky.in_box and base.blinky_dead:
        base.blinky_dead = False
    if inky.in_box and base.inky_dead:
        base.inky_dead = False
    if pinky.in_box and base.pinky_dead:
        base.pinky_dead = False
    if clyde.in_box and base.clyde_dead:
        base.clyde_dead = False

    pygame.display.flip()
pygame.quit()
