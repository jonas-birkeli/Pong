import pygame
import math
import random

import settings.constant as constant


class Ball:
    def __init__(self, entities, game_values) -> None:
        self.entities = entities
        self.game_values = game_values

        screen_size = self.game_values.get_screen_size()
        self.pos_x = screen_size[0]/2 - constant.BALL_SIZE/2
        self.pos_y = screen_size[1]/2 - constant.BALL_SIZE/2

        self.speed = constant.BALL_START_SPEED
        self.vel_x, self.vel_y = 0, 0
        self.calc_random_vel()  # Starting velocity

        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.BALL_SIZE, constant.BALL_SIZE)

        self.winner = 0

    def calc_random_vel(self) -> None:
        angle = random.randint(-45, 45)
        rad = math.radians(angle)

        self.vel_x = math.cos(rad)
        self.vel_y = math.sin(rad)

    def calc_real_vel(self) -> None:
        screen_width, screen_height = self.game_values.get_screen_size()

        if self.pos_x < screen_width / 2:  # Paddle 1, middle of screen
            paddle_y = self.entities.get_paddle1().pos_y
        else:                                        # Paddle 2
            paddle_y = self.entities.get_paddle2().pos_y

        y_middle = paddle_y + constant.PADDLE_HEIGHT/2 - self.pos_y
        # Sets middle of paddle as y = 0, and the ball pos as its offset.
        # If ball hits the middle of the paddle, then y_middle will be 0.
        # if ball hits at top or bottom, y_middle will be the value of PADDLE_HEIGHT/2,
        # negative or positive based on top or bottom.
        y_factor = (y_middle / constant.PADDLE_HEIGHT) * -2
        # Converts from x value to a size from negative -1/2 to 1/2
        # -1 to flip sign and *2 to make up for the half height at line 35

        rad = math.radians(45 * y_factor)
        self.vel_x = math.cos(rad)
        self.vel_y = math.sin(rad)

    def reset(self) -> None:
        screen_size = self.game_values.get_screen_size()

        self.pos_x = screen_size[0]/2 - constant.BALL_SIZE / 2  # starting in middle
        self.pos_y = screen_size[1]/2 - constant.BALL_SIZE / 2  # Ball size can be anything
        self.speed = constant.BALL_START_SPEED  # reset
        # Velocity stays the same

    def upd_rect_pos(self) -> None:
        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.BALL_SIZE, constant.BALL_SIZE)

    def move(self) -> None:
        screen_width, screen_height = self.game_values.get_screen_size()

        if self.pos_x < 0:
            self.set_winner(2)

            return

        if self.pos_x > screen_width - constant.BALL_SIZE:
            self.set_winner(1)

            return

        # Bounce from roof or ground
        if self.pos_y < constant.SCREEN_OFFSET:
            self.invert_velocity()

            # Ball can glitch through wall if at a specific angle
            # To limit this, the pos is set to outside the limit
            self.pos_y = constant.SCREEN_OFFSET

        elif self.pos_y + constant.BALL_SIZE > screen_height - constant.SCREEN_OFFSET:
            self.invert_velocity()

            # Ball can glitch through wall if at a specific angle
            # To limit this, the pos is set to outside the limit
            self.pos_y = screen_height - constant.SCREEN_OFFSET - constant.BALL_SIZE

        self.entities.collision_check()

        self.pos_x += self.vel_x * self.speed
        self.pos_y += self.vel_y * self.speed
        self.upd_rect_pos()

        return

    def set_winner(self, winner: int) -> None:
        self.winner = winner

    def get_winner(self) -> int:
        return self.winner

    def invert_velocity(self):
        self.vel_y *= -1  # Invert ball velocity
        constant.WALL_HIT_SOUND.play()
