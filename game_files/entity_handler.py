import pygame
import random

import settings.constant as constant

from game_files.paddle import Paddle
from game_files.pong_ball import Ball


class EntityHandler:
    def __init__(self, game_values):
        self.game_values = game_values

        self.paddle1 = Paddle(self.game_values, constant.PADDLE_1_POS)
        self.paddle2 = Paddle(self.game_values, pygame.display.get_surface().get_width() - constant.PADDLE_2_POS)

        self.ball = Ball(self, self.game_values)  # Passing self reference for collision handling of paddles

    def get_paddle1(self):
        return self.paddle1

    def get_paddle2(self):
        return self.paddle2

    def get_ball(self):
        return self.ball

    def collision_check(self):
        p1_collide = pygame.Rect.colliderect(self.get_ball().rect, self.get_paddle1().rect)
        p2_collide = pygame.Rect.colliderect(self.get_ball().rect, self.get_paddle2().rect)

        if p1_collide:
            # We do not want to bounce the ball if it is behind the front surface of the paddle.
            self.get_ball().calc_real_vel()
            self.get_ball().speed += constant.BALL_SPEED_INCREMENT
            constant.PADDLE_HIT_SOUND.play()

            # We want a random y offset for hard AI to make predictions harder.
            # Only calculating this when the ball hits the main paddle.
            rand = random.randint(0, constant.PADDLE_HEIGHT / 2)
            self.game_values.set_random_y_offset(rand)

        if p2_collide:
            self.get_ball().calc_real_vel()
            self.get_ball().vel_x *= -1
            self.get_ball().speed += constant.BALL_SPEED_INCREMENT
            constant.PADDLE_HIT_SOUND.play()
