import pygame
import settings.constant as constant


class Paddle:
    first_paddle_init = True

    def __init__(self, game_values):
        self.game_values = game_values

        self.pos_y = pygame.display.get_surface().get_height() / 2 - constant.PADDLE_HEIGHT / 2  # starting in middle
        self.dif = 1

        if Paddle.first_paddle_init:
            self.pos_x = 20
            Paddle.first_paddle_init = False
        else:
            self.pos_x = pygame.display.get_surface().get_width() - 40
            Paddle.first_paddle_init = True

        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.PADDLE_WIDTH, constant.PADDLE_HEIGHT)

    def draw(self, screen_ref):
        self.upd_pos(0)
        pygame.draw.rect(screen_ref, constant.PADDLE_COLOR, self.rect)

    def upd_pos(self, vel: float):
        window_height = pygame.display.get_surface().get_height()
        if self.pos_y < constant.PADDLE_LIMIT:
            self.pos_y = constant.PADDLE_LIMIT  # Reset if exceeding screensize
        elif self.pos_y > window_height - constant.PADDLE_HEIGHT:
            self.pos_y = window_height - constant.PADDLE_HEIGHT  # Reset
        else:
            self.pos_y += vel
            self.upd_rect()

    def upd_rect(self):
        if self.pos_x != 20:
            self.pos_x = pygame.display.get_surface().get_width() - 40
        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.PADDLE_WIDTH, constant.PADDLE_HEIGHT)


class PaddleAI(Paddle):
    def __init__(self, game_values):
        super().__init__(game_values)

    def move(self, ball_pos: int, vel: float):
        """

        :param ball_pos: Y position to all
        :param vel: Max velocity the paddle can move at lower difficulties
        """
        difficulty = self.game_values.get_difficulty()
        if difficulty == 3:  # Impossible difficulty
            # sets value to middle of ball - random value_offset to alter balls direction
            self.pos_y = \
                ball_pos \
                + constant.BALL_SIZE / 2 \
                - self.game_values.get_random_y_offset() \
                - constant.PADDLE_HEIGHT / 2
        elif difficulty == 2:  # Hard
            if self.pos_y + self.game_values.get_random_y_offset() / 2 > ball_pos:
                # y-offset is being calculated at every Paddle 1 hit in pong_ball.py to make predictions harder
                self.pos_y -= vel * self.game_values.get_difficulty()
            elif self.pos_y + constant.PADDLE_HEIGHT < ball_pos:
                self.pos_y += vel * self.game_values.get_difficulty()
        else:  # Easy
            if self.pos_y + constant.PADDLE_HEIGHT / 2 - constant.PADDLE_HEIGHT / 8 > ball_pos:
                self.pos_y -= vel
            elif self.pos_y + constant.PADDLE_HEIGHT / 2 + constant.PADDLE_HEIGHT / 8 < ball_pos:
                self.pos_y += vel

        # to limit paddle from traveling off of the screen
        window_height = pygame.display.get_surface().get_height()
        if self.pos_y < constant.PADDLE_LIMIT:
            self.pos_y = constant.PADDLE_LIMIT
        elif self.pos_y > window_height - constant.PADDLE_HEIGHT:
            self.pos_y = window_height - constant.PADDLE_HEIGHT
        # End

        self.upd_rect()
