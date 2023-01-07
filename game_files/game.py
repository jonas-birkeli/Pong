import pygame

import settings.constant as constant
import settings.keybind as keybind
from game_files.entity_handler import EntityHandler


class Game:
    def __init__(self, game_values):
        self.game_values = game_values

        pygame.init()
        self.entities = EntityHandler(self.game_values)
        self.screen = pygame.display.set_mode(self.game_values.get_screen_size(), pygame.RESIZABLE, vsync=1)
        self.fps = pygame.time.Clock()
        pygame.display.set_caption(constant.GAME_NAME)
        pygame.display.set_icon(pygame.image.load('etc/pong_icon.png'))

        self.font = pygame.font.Font('etc/block_font.ttf', 40)

        self.pause = False

        self.player1_score = 0
        self.player2_score = 0

    def run(self):
        while True:
            surface = pygame.display.get_surface()
            middle_width = surface.get_width() / 2
            middle_height = surface.get_height() / 2

            self.screen.fill(constant.BACKGROUND_COLOR)  # Reset scene

            self.display_text(self.player1_score, middle_width*0.7, middle_height*0.2)
            self.display_text(self.player2_score, middle_width*1.3, middle_height*0.2)

            if self.key_handler() == 1:  # 1 means exit game
                self.reset_class(wipe=True)

                return

            if self.pause:
                self.display_text(constant.PAUSE_TEXT, middle_width, middle_height - 100)
                self.display_text(constant.UNPAUSE_TEXT, middle_width, middle_height + 50)
                self.display_text(constant.PAUSE_EXIT, middle_width, middle_height + 150)
                # Pause text
            else:
                self.entities.get_ball().move()

            winner = self.entities.get_ball().get_winner()
            if winner != 0:

                if winner == 1:
                    self.player1_score += 1

                elif winner == 2:
                    self.player2_score += 1

                constant.SCORE_SOUND.play()
                self.entities.get_ball().set_winner(0)
                self.entities.get_ball().reset()
                # Reset winner and ball position

                if self.player2_score == constant.POINT_LIMIT:

                    if self.game_values.get_mode != 1:
                        self.game_values.set_game_title(f'Spiller 2 vant med {self.player2_score} - {self.player1_score}')
                    else:
                        self.game_values.set_game_title(f'AI vant med {self.player2_score} - {self.player1_score}')

                elif self.player1_score == constant.POINT_LIMIT:
                    self.game_values.set_game_title(f'Spiller 1 vant med {self.player1_score} - {self.player2_score}')

                if self.player1_score == constant.POINT_LIMIT or self.player2_score == constant.POINT_LIMIT:
                    # Common for both winners
                    self.store_window_size()
                    self.reset_class()
                    constant.WIN_SOUND.play()
                    # Cleaning up class data

                    return

            pygame.draw.rect(self.screen, constant.BALL_COLOR, self.entities.get_ball().rect)
            pygame.draw.rect(self.screen, constant.PADDLE_COLOR, self.entities.get_paddle1().rect)
            pygame.draw.rect(self.screen, constant.PADDLE_COLOR, self.entities.get_paddle2().rect)

            pygame.display.update()
            self.fps.tick(constant.FPS)

    def key_handler(self):
        key_down = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                # New screen_size
                width, height = event.size

                width = max(width, constant.SCREEN_MIN_WIDTH)
                height = max(height, constant.SCREEN_MIN_HEIGHT)

                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE, vsync=True)
                self.game_values.set_screen_size((width, height))

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if key_down[keybind.QUIT_GAME] and self.pause:  # Exit only when paused
                    # TODO
                    return 1
                if key_down[keybind.PAUSE_GAME]:  # Pause and unpause
                    constant.PAUSE_SOUND.play()
                    self.pause = not self.pause

        if not self.pause:  # Only allow movement when game is not paused
            if key_down[keybind.PADDLE_1_UP]:
                self.entities.get_paddle1().upd_pos(-1)

            if key_down[keybind.PADDLE_1_DOWN]:
                self.entities.get_paddle1().upd_pos(1)

            if self.game_values.get_mode() == 1:
                # Allows for arrow UP/DOWN input for player 1 by using player2-controls ONLY if playing against AI

                if key_down[keybind.PADDLE_2_UP]:
                    self.entities.get_paddle1().upd_pos(-1)

                if key_down[keybind.PADDLE_2_DOWN]:
                    self.entities.get_paddle1().upd_pos(1)
                self.entities.get_paddle2().move(self.entities.get_ball().pos_y)
                # Paddle AI uses a different move function than the standard paddle, only enabled if mode is set to 1, or AI
            else:
                if key_down[keybind.PADDLE_2_UP]:
                    self.entities.get_paddle2().upd_pos(-1)
                if key_down[keybind.PADDLE_2_DOWN]:
                    self.entities.get_paddle2().upd_pos(1)

    def store_window_size(self):
        surface = pygame.display.get_surface()
        self.game_values.set_screen_size((surface.get_width(), surface.get_height()))

    def reset_class(self, wipe=False):
        if wipe:
            self.game_values.set_game_title(constant.GAME_NAME)
            # Game title is used to display the winner of the last match.

        self.player1_score = 0
        self.player2_score = 0
        self.pause = False

        self.entities.get_ball().reset()

        surface = pygame.display.get_surface()
        self.entities.get_paddle1().pos_y = surface.get_height()/2 - constant.PADDLE_HEIGHT/2
        self.entities.get_paddle2().pos_y = surface.get_height()/2 - constant.PADDLE_HEIGHT/2

    def display_text(self, text, x, y):
        txt = self.font.render(f'{text}', True, constant.TEXT_COLOR, None)
        txt_rect = txt.get_rect()
        txt_rect.center = x, y
        self.screen.blit(txt, txt_rect)
