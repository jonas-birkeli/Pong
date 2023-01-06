from game_files.paddle import Paddle, PaddleAI
from game_files.pong_ball import Ball
import settings.constant as constant
import pygame


class EntityHandler:
    def __init__(self, game_values):
        self.paddle1 = Paddle(game_values, constant.PADDLE_1_POS)

        if game_values.mode == 1:  # check if 1-player
            self.paddle2 = PaddleAI(game_values, pygame.display.get_surface().get_width() - constant.PADDLE_2_POS)
        else:  #
            self.paddle2 = Paddle(game_values, pygame.display.get_surface().get_width() - constant.PADDLE_2_POS)

        self.ball = Ball(self, game_values)  # Passing self ref for collision handling of paddles

    def get_paddle1(self):
        return self.paddle1

    def get_paddle2(self):
        return self.paddle2

    def get_ball(self):
        return self.ball
