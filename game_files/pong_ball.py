import pygame
import math
import random

import settings.constant as constant


class Ball:
    def __init__(self, entities, game_values):
        self.entities = entities
        self.game_values = game_values

        self.paddle_hit_sound = pygame.mixer.Sound('etc/paddle_hit.wav')
        self.roof_and_ground_hit_sound = pygame.mixer.Sound('etc/ground_roof_hit.wav')
        self.score_sound = pygame.mixer.Sound('etc/wall_hit.wav')

        self.speed = constant.BALL_START_SPEED  # starting value, higher after each paddle hit
        self.pos_x = pygame.display.get_surface().get_width()/2 - constant.BALL_SIZE/2
        self.pos_y = pygame.display.get_surface().get_height()/2 - constant.BALL_SIZE/2
        self.vel_x, self.vel_y = 0, 0
        self.calc_random_vel()  # Starting velocity

        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.BALL_SIZE, constant.BALL_SIZE)

    def calc_random_vel(self):
        angle = random.randint(-45, 45)
        rad = math.radians(angle)
        self.vel_x = math.cos(rad)
        self.vel_y = math.sin(rad)

    def calc_real_vel(self):
        screen_width = pygame.display.get_surface().get_width()
        if self.pos_x < screen_width / 2:  # Paddle 1, middle of screen
            paddle_y = self.entities.get_paddle1().pos_y
        else:                                        # Paddle 2
            paddle_y = self.entities.get_paddle2().pos_y
        y_middle = paddle_y + constant.PADDLE_HEIGHT/2 - self.pos_y
        # Sets middle of paddle as y = 0, and the ball pos as its offset.
        # If ball hits the middle of the paddle, then y_middle will be 0
        # if ball hits at top or bottom, y_middle will be the value of PADDLE_HEIGHT/2,
        # negative or positive based on top or bottom.
        y_factor = (y_middle / constant.PADDLE_HEIGHT) * -2
        # Converts from x value to a size from negative -1/2 to 1/2
        # -1 to flip sign and *2 to make up for the half height at line 33
        rad = math.radians(45 * y_factor)
        self.vel_x = math.cos(rad)
        self.vel_y = math.sin(rad)

    def reset(self) -> None:
        self.pos_x = pygame.display.get_surface().get_width() / 2 - constant.BALL_SIZE / 2  # starting in middle
        self.pos_y = pygame.display.get_surface().get_height() / 2 - constant.BALL_SIZE / 2  # Ball size can be anything
        self.speed = constant.BALL_START_SPEED  # reset

    def upd_rect_pos(self) -> None:
        self.rect = pygame.Rect(self.pos_x, self.pos_y, constant.BALL_SIZE, constant.BALL_SIZE)

    def move(self) -> int:
        """
        Moves ball and handles collisions
        :return: 0: Nothing
        1: Player 1 won
        2: Player 2 won
        """
        # if hitting wall behind pads
        if self.pos_x < 0:
            self.score_sound.play()
            return 2  # player 2 has won
        if self.pos_x > pygame.display.get_surface().get_width() - constant.BALL_SIZE:
            self.score_sound.play()
            return 1  # player 1 has won

        # Bounce from roof or ground
        if self.pos_y < 0 or self.pos_y + constant.BALL_SIZE > pygame.display.get_surface().get_height():
            self.vel_y *= -1
            self.roof_and_ground_hit_sound.play()

        # Collision detection as bool
        p1_collide = pygame.Rect.colliderect(self.rect, self.entities.get_paddle1())
        p2_collide = pygame.Rect.colliderect(self.rect, self.entities.get_paddle2())

        if p1_collide:
            # We do not want to bounce the ball if it is behind the front surface of the paddle.
            self.calc_real_vel()
            self.speed += constant.BALL_SPEED_INCREMENT
            self.paddle_hit_sound.play()

            rand = random.randint(0, constant.PADDLE_HEIGHT/2)
            self.game_values.set_random_y_offset(rand)

        if p2_collide:
            self.calc_real_vel()
            self.vel_x *= -1  # inverted sign
            self.speed += constant.BALL_SPEED_INCREMENT
            self.paddle_hit_sound.play()

        self.pos_x += self.vel_x * self.speed
        self.pos_y += self.vel_y * self.speed
        self.upd_rect_pos()
        return 0
