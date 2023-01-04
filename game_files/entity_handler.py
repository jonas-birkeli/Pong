from game_files.paddle import Paddle, PaddleAI
from game_files.pong_ball import Ball


class EntityHandler:
    def __init__(self, game_values):
        mode = game_values.mode
        self.paddle1 = Paddle(game_values)
        if mode == 1:  # 1 meaning 1-player
            self.paddle2 = PaddleAI(game_values)
        else:  #
            self.paddle2 = Paddle(game_values)

        self.ball = Ball(self, game_values)  # Passing self ref for colission handling of paddles

    def get_paddle1(self):
        return self.paddle1

    def get_paddle2(self):
        return self.paddle2

    def get_ball(self):
        return self.ball
