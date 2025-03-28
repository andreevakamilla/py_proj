import pygame

import random
import base
import draw

class Ghost:
    def __init__(self, x_coord, y_coord, target,
                 speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.x_centre = x_coord + base.ADD_COORD_GHOST
        self.y_centre = y_coord + base.ADD_COORD_GHOST
        self.target = target
        self.speed = speed
        self.img = img
        self.direct = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not base.powerup and not self.dead) or (
                base.eaten[self.id] and base.powerup and not self.dead):
            base.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif base.powerup and not self.dead and not base.eaten[self.id]:
            base.screen.blit(draw.spooked_img, (self.x_pos, self.y_pos))
        else:
            base.screen.blit(draw.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect(
            (self.x_centre - base.GHOST_X_RIGHT, self.y_centre - base.GHOST_X_RIGHT), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = (base.HEIGHT - base.BIG_SCORE) // base.HEIGHT_LINE
        num2 = (base.WIDTH // base.WIDTH_LINE)
        num3 = 15
        self.turns = [False, False, False, False]

        dx = [0, 0, 1, -1]
        dy = [-1, 1, 0, 0]

        for i in range(4):
            x_check = self.x_centre + num3 * dx[i]
            y_check = self.y_centre + num3 * dy[i]

            if 0 <= x_check // num2 < base.CENTER_X_BORDER and 0 <= y_check // num1 < len(
                    base.level):
                if base.level[y_check // num1][x_check // num2] < 3 or (
                        base.level[y_check // num1][x_check // num2] == 9
                        and (self.in_box or self.dead)):
                    self.turns[i] = True

        if self.direct in (2, 3):
            for i in [0, 1]:
                x_check = self.x_centre + num3 * dx[i]
                y_check = self.y_centre + num3 * dy[i]

                if base.GHOST_X_LEFT <= self.x_centre % num2 <= base.GHOST_X_RIGHT:
                    if (0 <= x_check // num2 < base.CENTER_X_BORDER
                            and 0 <= y_check // num1 < len(base.level)):
                        if (base.level[y_check // num1][x_check // num2] < 3 or
                            (base.level[y_check // num1][x_check // num2] == 9
                                and (self.in_box or self.dead))):
                            self.turns[i] = True

            for i in [2, 3]:
                x_check = self.x_centre + num3 * dx[i]
                y_check = self.y_centre + num3 * dy[i]

                if base.GHOST_X_LEFT <= self.y_centre % num1 <= base.GHOST_X_RIGHT:
                    if ((0 <= x_check // num2 < base.CENTER_X_BORDER)
                            and (0 <= y_check // num1 < len(base.level))):
                        if ((base.level[y_check // num1][x_check // num2] < 3)
                            or ((base.level[y_check //
                                            num1][x_check // num2] == 9
                                and (self.in_box or self.dead)))):
                            self.turns[i] = True

        if self.direct in (0, 1):
            for i in [2, 3]:
                x_check = self.x_centre + num1 * dx[i]
                y_check = self.y_centre + num1 * dy[i]

                if base.GHOST_X_LEFT <= self.x_centre % num2 <= base.GHOST_X_RIGHT:
                    if ((0 <= x_check // num2 < base.CENTER_X_BORDER)
                            and (0 <= y_check // num1 < len(base.level))):
                        if (base.level[y_check // num1][x_check // num2] < 3
                            or ((base.level[y_check // num1]
                                 [x_check // num2] == 9)
                                and ((self.in_box or self.dead)))):
                            self.turns[i] = True

            for i in [0, 1]:
                x_check = self.x_centre + num3 * dx[i]
                y_check = self.y_centre + num3 * dy[i]

                if base.GHOST_X_LEFT <= self.y_centre % num1 <= base.GHOST_X_RIGHT:
                    if ((0 <= x_check // num2 < base.CENTER_X_BORDER)
                            and (0 <= y_check // num1 < len(base.level))):
                        if (base.level[y_check // num1][x_check // num2] < 3
                            or (base.level[y_check // num1]
                                [x_check // num2] == 9
                                and (self.in_box or self.dead))):
                            self.turns[i] = True

        if self.x_centre // base.WIDTH_LINE == base.CENTER_X_BORDER:
            self.turns[0] = True
            self.turns[1] = True

        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_ghost(self):
        target_x, target_y = self.target
        dx, dy = [0, 0, 1, -1], [-1, 1, 0, 0]
        if self.x_pos > base.WIDTH:
            self.x_pos = -base.SMALL_SCORE
        elif self.x_pos < -base.SMALL_SCORE:
            self.x_pos = base.WIDTH - base.SMALL_SCORE

        if self.direct is None or not self.turns[self.direct]:
            available_directions = [i for i in range(4) if self.turns[i]]

            if available_directions:
                self.direct = random.choice(available_directions)

        if 0 <= self.direct < 4:
            new_x = self.x_pos + self.speed * dx[self.direct]
            new_y = self.y_pos + self.speed * dy[self.direct]

            if self.is_valid_move(new_x, new_y):
                self.x_pos, self.y_pos = new_x, new_y

        return self.x_pos, self.y_pos, self.direct

    def is_valid_move(self, x, y):
        num1 = (base.HEIGHT - base.BIG_SCORE) // base.HEIGHT_LINE
        num2 = (base.WIDTH // base.WIDTH_LINE)

        x_check = x + base.ADD_COORD_GHOST
        y_check = y + base.ADD_COORD_GHOST

        if (
                0 <= x_check // num2 < base.CENTER_X_BORDER and
                0 <= y_check // num1 < len(base.level) and
                (base.level[y_check // num1][x_check // num2] < 3 or (
                    base.level[y_check // num1][x_check // num2] == 9
                    and (self.in_box or self.dead)))
        ):
            return True

        return False
