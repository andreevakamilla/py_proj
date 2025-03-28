import pygame
import os
import base

pygame.init()

player_images = []


path_directory = os.path.dirname(__file__)
font = pygame.font.Font(
    os.path.join(
        path_directory,
        'Font/PoetsenOne-Regular.ttf'))
blinky_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory, 'images_ghost/red.png')), (base.IMG_SIZE, base.IMG_SIZE))
pinky_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory,
                 'images_ghost/pink.png')),
    (base.IMG_SIZE, base.IMG_SIZE))
inky_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory,
                 'images_ghost/blue.png')),
    (base.IMG_SIZE, base.IMG_SIZE))
clyde_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory,
                 'images_ghost/orange.png')),
    (base.IMG_SIZE, base.IMG_SIZE))
spooked_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory,
                 'images_ghost/powerup.png')),
    (base.IMG_SIZE, base.IMG_SIZE))
dead_img = pygame.transform.scale(pygame.image.load(
    os.path.join(path_directory,
                 'images_ghost/dead.png')),
    (base.IMG_SIZE, base.IMG_SIZE))
for i in range(1, 5):
    player_images.append(pygame.transform.scale(
        pygame.image.load(f'images_pacman/{i}.png'), (base.IMG_SIZE, base.IMG_SIZE)))

def draw_misc():
    score_text = font.render(f'base.score: {base.score}', True, 'white')
    base.screen.blit(score_text, (base.SMALL_SCORE, base.HEIGHT - base.WIDTH_LINE))
    if base.powerup:
        pygame.draw.circle(base.screen, 'blue', (140, 930), 15)
    for i in range(base.lives):
        base.screen.blit(
            pygame.transform.scale(
                player_images[0], (base.WIDTH_LINE, base.WIDTH_LINE)), (650 + i * 40, 915))
    if base.game_over:
        pygame.draw.rect(base.screen, 'white', [base.BIG_SCORE, 200, 800, 300], 0, base.SMALL_SCORE)
        pygame.draw.rect(base.screen, 'dark gray', [70, 220, 760, 260], 0, base.SMALL_SCORE)
        gameover_text = font.render(
            "Game Over! Space bar to restart", True, "red")
        base.screen.blit(gameover_text, (base.START_SCORE_BORDER, 300))
    if base.game_won:
        pygame.draw.rect(base.screen, 'white', [base.BIG_SCORE, 200, 800, 300], 0, base.SMALL_SCORE)
        pygame.draw.rect(base.screen, 'dark gray', [70, 220, 760, 260], 0, base.SMALL_SCORE)
        gameover_text = font.render(
            "You Won! Space bar to restart", True, "green")
        base.screen.blit(gameover_text, (base.START_SCORE_BORDER, 300))


def draw_board(level):
    num1 = (base.HEIGHT - base.BIG_SCORE) // base.HEIGHT_LINE
    num2 = (base.WIDTH // base.WIDTH_LINE)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(base.screen,
                                   'white',
                                   (j * num2 + (0.5 * num2),
                                    i * num1 + (0.5 * num1)),
                                   4
                                   )
            if level[i][j] == 2 and not base.flicker:
                pygame.draw.circle(base.screen,
                                   'white',
                                   (j * num2 + (0.5 * num2),
                                    i * num1 + (0.5 * num1)),
                                   base.SMALL_SCORE
                                   )
            if level[i][j] == 3:
                pygame.draw.line(base.screen,
                                 base.color,
                                 (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1),
                                 3
                                 )
            if level[i][j] == 4:
                pygame.draw.line(base.screen,
                                 base.color,
                                 (j * num2, (0.5 * num1) + i * num1),
                                 (j * num2 + num2, (0.5 * num1) + i * num1),
                                 3
                                 )
            if level[i][j] == 5:
                pygame.draw.arc(base.screen,
                                base.color,
                                [(j * num2 - (0.4 * num2)) - 2,
                                 (i * num1 + (0.5 * num1)),
                                 num2,
                                 num1],
                                0,
                                base.PI / 2,
                                3)
            if level[i][j] == 6:
                pygame.draw.arc(base.screen,
                                base.color,
                                [j * num2 + (0.5 * num2),
                                 (i * num1 + (0.5 * num1)),
                                 num2,
                                 num1],
                                base.PI / 2,
                                base.PI,
                                3)
            if level[i][j] == 7:
                pygame.draw.arc(base.screen,
                                base.color,
                                [j * num2 + (0.5 * num2),
                                 (i * num1 - (0.4 * num1)),
                                 num2,
                                 num1],
                                base.PI,
                                3 * base.PI / 2,
                                3)
            if level[i][j] == 8:
                pygame.draw.arc(base.screen,
                                base.color,
                                [(j * num2 - (0.4 * num2)) - 2,
                                 (i * num1 - (0.4 * num1)),
                                 num2,
                                 num1],
                                3 * base.PI / 2,
                                2 * base.PI,
                                3)

            if level[i][j] == 4:
                pygame.draw.line(base.screen,
                                 'white',
                                 (j * num2, (0.5 * num1) + i * num1),
                                 (j * num2 + num2, (0.5 * num1) + i * num1),
                                 2)


def draw_player():
    if base.direction == 0:
        base.screen.blit(
            player_images[base.counter // 5],
            (base.player_x, base.player_y))
    elif base.direction == 1:
        base.screen.blit(pygame.transform.flip(
            player_images[base.counter // 5], True, False),
            (base.player_x, base.player_y))
    elif base.direction == 2:
        base.screen.blit(pygame.transform.rotate(
            player_images[base.counter // 5], 90),
            (base.player_x, base.player_y))
    elif base.direction == 3:
        base.screen.blit(pygame.transform.rotate(
            player_images[base.counter // 5], 270),
            (base.player_x, base.player_y))
