from game_files.paddle import Paddle, PaddleAI
from game_files.pong_ball import Ball


class ObjHandler:
    def __init__(self, against_ai=False):
        self.paddle1 = Paddle()
        if against_ai:
            self.paddle2 = PaddleAI()
        self.ball = Ball()

    def get_paddle1(self):
        return self.paddle1

    def get_paddle2(self):
        return self.paddle2

    def get_ball(self):
        return self.ball
