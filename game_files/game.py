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

        self.font = pygame.font.Font('etc/FFFFORWA.ttf', 40)
        self.pause_sound = pygame.mixer.Sound('etc/pause.mp3')
        self.win_sound = pygame.mixer.Sound('etc/start_win.wav')

        self.pause = False

        self.player1_score = 0
        self.player2_score = 0

    def run(self):
        while True:
            if self.game_values.get_socket is not None:  # Socket connection established
                if self.game_values.get_first_client() is True:
                    self.entities.get_paddle2().pos_y = self.game_values.get_socket().receive()
                elif self.game_values.get_first_client is False:
                    self.entities.get_paddle1().pos_y = self.game_values.get_socket().receive()
            surface = pygame.display.get_surface()
            sw2 = surface.get_width() / 2
            sh2 = surface.get_height() / 2

            self.screen.fill(constant.BACKGROUND_COLOR)

            self.display_text(f'{self.player1_score}', surface.get_width() / 3, surface.get_height() / 15)
            self.display_text(f'{self.player2_score}', (surface.get_width() / 3) * 2, surface.get_height() / 15)

            menu_exit = self.key_input()
            if menu_exit == 1:  # 1 means exit game
                self.game_values.set_game_title(constant.GAME_NAME)
                # Restore to default game title. This value is changed when a player wins the game.
                self.player1_score = 0
                self.player2_score = 0
                self.pause = False
                return 0  # Exit game

            get_player_scored = 0  # outer scope
            if not self.pause:
                get_player_scored = self.entities.get_ball().move()
            else:
                self.display_text(constant.PAUSE_TEXT, sw2, sh2 - 100)
                self.display_text(constant.UNPAUSE_TEXT, sw2, sh2 + 50)
                self.display_text(constant.PAUSE_EXIT, sw2, sh2 + 150)
            if get_player_scored == 1:
                self.player1_score += 1
                if self.player1_score == constant.POINT_LIMIT:
                    # Cleaning up class data and returning winner
                    self.game_values.set_game_title(f'Spiller 1 vant med {self.player1_score} - {self.player2_score}')
                    self.player1_score = 0
                    self.player2_score = 0
                    self.win_sound.play()

                    # Remember window size in case of resize
                    surface = pygame.display.get_surface()
                    self.game_values.set_screen_size((surface.get_width(), surface.get_height()))
                    return 0
                self.entities.get_ball().reset()
            elif get_player_scored == 2:
                self.player2_score += 1
                if self.player2_score == constant.POINT_LIMIT:
                    # Cleaning up class data and returning winner
                    self.game_values.set_game_title(f'Spiller 2 vant med {self.player2_score} - {self.player1_score}')
                    self.player2_score = 0
                    self.player1_score = 0
                    self.win_sound.play()

                    # Remember window size in case of resize
                    surface = pygame.display.get_surface()
                    self.game_values.set_screen_size((surface.get_width(), surface.get_height()))

                    return 0
                self.entities.get_ball().reset()
            if not self.pause:
                self.entities.get_ball().move()
            pygame.draw.rect(self.screen, constant.BALL_COLOR, self.entities.get_ball().rect)
            pygame.draw.rect(self.screen, constant.PADDLE_COLOR, self.entities.get_paddle1().rect)
            pygame.draw.rect(self.screen, constant.PADDLE_COLOR, self.entities.get_paddle2().rect)
            pygame.display.update()
            self.fps.tick(constant.FPS)

            if self.game_values.get_first_client() is True:
                self.game_values.send(self.entities.get_paddle1().pos_y)
            elif self.game_values.get_first_client() is False:
                self.game_values.send(self.entities.get_paddle2().pos_y)

    def display_text(self, text, x, y):
        txt = self.font.render(f'{text}', True, constant.TEXT_COLOR, None)
        txt_rect = txt.get_rect()
        txt_rect.center = x, y
        self.screen.blit(txt, txt_rect)

    def key_input(self):
        key_down = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if key_down[keybind.QUIT_GAME] and self.pause:  # Exit only when paused
                    # TODO
                    return 1
                if key_down[keybind.PAUSE_GAME]:  # Pause and unpause
                    self.pause_sound.play()
                    self.pause = not self.pause

        if not self.pause:  # Only allow movement when game is not paused
            if self.game_values.get_first_client() is True:
                if key_down[keybind.PADDLE_1_UP]:
                    self.entities.get_paddle1().upd_pos(-constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_1_DOWN]:
                    self.entities.get_paddle1().upd_pos(constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_2_UP]:
                    self.entities.get_paddle1().upd_pos(-constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_2_DOWN]:
                    self.entities.get_paddle1().upd_pos(constant.PADDLE_SPEED)
            elif self.game_values.get_first_client() is False:
                if key_down[keybind.PADDLE_1_UP]:
                    self.entities.get_paddle2().upd_pos(-constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_1_DOWN]:
                    self.entities.get_paddle2().upd_pos(constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_2_UP]:
                    self.entities.get_paddle2().upd_pos(-constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_2_DOWN]:
                    self.entities.get_paddle2().upd_pos(constant.PADDLE_SPEED)
            else:
                if key_down[keybind.PADDLE_1_UP]:
                    self.entities.get_paddle1().upd_pos(-constant.PADDLE_SPEED)
                if key_down[keybind.PADDLE_1_DOWN]:
                    self.entities.get_paddle1().upd_pos(constant.PADDLE_SPEED)
                if self.game_values.get_mode() == 1:
                    # Allows for arrow UP/DOWN input for player 1 by using player2-controls ONLY if playing against AI
                    if key_down[keybind.PADDLE_2_UP]:
                        self.entities.get_paddle1().upd_pos(-constant.PADDLE_SPEED)
                    if key_down[keybind.PADDLE_2_DOWN]:
                        self.entities.get_paddle1().upd_pos(constant.PADDLE_SPEED)

                    # Paddle AI uses a different move function than the standard paddle, only enabled if mode is set to 1, or AI
                    self.entities.get_paddle2().move(
                        self.entities.get_ball().pos_y,  # Ball pos ref
                        constant.PADDLE_SPEED
                    )
                else:
                    if key_down[keybind.PADDLE_2_UP]:
                        self.entities.get_paddle2().upd_pos(-constant.PADDLE_SPEED)
                    if key_down[keybind.PADDLE_2_DOWN]:
                        self.entities.get_paddle2().upd_pos(constant.PADDLE_SPEED)

# Pause
# Exit
# Get pad pos
# Send pad pos
