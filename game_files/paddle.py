import pygame
import settings.constant as constant


class Paddle:
    first_paddle_init = True

    def __init__(self, game_values, pos_x):
        self.game_values = game_values
        self.pos_x = pos_x

        self.pos_y = pygame.display.get_surface().get_height() / 2 - constant.PADDLE_HEIGHT / 2  # starting in middle
        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.PADDLE_WIDTH, constant.PADDLE_HEIGHT)

    def draw(self, screen_ref):
        self.upd_rect()  # In case paddle has moved
        pygame.draw.rect(screen_ref, constant.PADDLE_COLOR, self.rect)

    def upd_pos(self, sign):
        window_height = pygame.display.get_surface().get_height()

        if self.pos_y < constant.PADDLE_LIMIT:
            self.pos_y = constant.PADDLE_LIMIT
            # Reset if exceeding screensize, top
            # PADDLE_LIMIT being the capped height to prevent glitching the ball

        elif self.pos_y > window_height - constant.PADDLE_HEIGHT - constant.PADDLE_LIMIT:
            self.pos_y = window_height - constant.PADDLE_HEIGHT - constant.PADDLE_LIMIT
            # Reset if exceeding screensize, bottom
            # PADDLE_LIMIT being the capped height to prevent glitching the ball

        else:
            self.pos_y += constant.PADDLE_SPEED * sign  # sign being either -1 or 1 meaning up or down
            self.upd_rect()

    def upd_rect(self):

        if self.pos_x != 20:
            self.pos_x = pygame.display.get_surface().get_width() - constant.PADDLE_WIDTH - 20
        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.PADDLE_WIDTH, constant.PADDLE_HEIGHT)


class PaddleAI(Paddle):
    def __init__(self, game_values, pos_x):
        super().__init__(game_values, pos_x)

    def move(self, ball_pos: int):
        difficulty = self.game_values.get_difficulty()

        if difficulty == 3:  # Impossible
            # sets value to middle of ball - random value_offset to alter balls direction
            self.pos_y = \
                + ball_pos \
                + constant.BALL_SIZE / 2 \
                - self.game_values.get_random_y_offset() \
                - constant.PADDLE_HEIGHT / 2

        elif difficulty == 2:  # Hard
            if self.pos_y + self.game_values.get_random_y_offset() / 2 > ball_pos:
                # y-offset is being calculated at every Paddle 1 hit in pong_ball.py to make predictions harder
                self.pos_y -= constant.PADDLE_SPEED * 2

            elif self.pos_y + constant.PADDLE_HEIGHT < ball_pos:
                self.pos_y += constant.PADDLE_SPEED * 2

        else:  # Easy
            if self.pos_y + constant.PADDLE_HEIGHT / 2 - constant.PADDLE_HEIGHT / 8 > ball_pos:
                self.pos_y -= constant.PADDLE_SPEED

            elif self.pos_y + constant.PADDLE_HEIGHT / 2 + constant.PADDLE_HEIGHT / 8 < ball_pos:
                self.pos_y += constant.PADDLE_SPEED

        # to limit paddle from traveling off of the screen
        screen_height = self.game_values.get_screen_size()[1]

        if self.pos_y < 0:
            self.pos_y = 0

        elif self.pos_y > screen_height - constant.PADDLE_HEIGHT:
            self.pos_y = screen_height - constant.PADDLE_HEIGHT

        self.upd_rect()
