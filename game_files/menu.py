import pygame
import sys

import settings.constant as constant
import settings.keybind as keybind


class Menu:
    def __init__(self, game_settings):

        self.game_values = game_settings

        pygame.init()
        self.screen = pygame.display.set_mode(self.game_values.get_screen_size(), pygame.RESIZABLE, vsync=True)
        pygame.display.set_icon(pygame.image.load('etc/pong_icon.png'))
        pygame.display.set_caption(constant.GAME_NAME)
        self.fps = pygame.time.Clock()

        # Font sizes
        self.big_font = pygame.font.Font('etc/block_font.ttf', 60)
        self.normal_font = pygame.font.Font('etc/block_font.ttf', 35)
        self.small_font = pygame.font.Font('etc/block_font.ttf', 20)

    def run(self):
        while True:
            start_game = self.key_input()  # Returns True || False
            if start_game:
                self.store_window_size()
                return  # Exit loop

            screen_size = self.game_values.get_screen_size()
            middle_width = screen_size[0] / 2
            middle_height = screen_size[1] / 2
            # Screen is resizable

            self.screen.fill(constant.BACKGROUND_COLOR)
            self.display_text(self.game_values.get_game_title(), middle_width, middle_height*0.5, self.big_font)
            self.display_text(constant.GAME_DEV, middle_width, middle_height*0.75, self.small_font)

            self.display_text(self.game_values.get_start_text(), middle_width, middle_height, self.normal_font)
            self.display_text(self.game_values.get_setting_text(), middle_width, middle_height*1.75, self.small_font)

            # Mode
            mode = self.game_values.get_mode()
            if mode == 2:
                mode_text = constant.TWO_PLAYER_LOCAL
            else:
                mode_text = constant.ONE_PLAYER

            self.display_text(mode_text, middle_width, middle_height*1.3, self.normal_font)

            # Difficulty
            difficulty = self.game_values.get_difficulty()
            if difficulty == 3:
                dif_text = constant.IMPOSSIBLE_TEXT
            elif difficulty == 2:
                dif_text = constant.HARD_TEXT
            else:
                dif_text = constant.EASY_TEXT

            if mode == 1:
                self.display_text(dif_text, middle_width, middle_height*1.5, self.normal_font)

            pygame.display.update()
            self.fps.tick(constant.FPS)

    def key_input(self) -> bool:
        key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                # New screen_size
                width, height = event.size

                width = max(width, constant.SCREEN_MIN_WIDTH)
                height = max(height, constant.SCREEN_MIN_HEIGHT)

                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE, vsync=True)
                self.game_values.set_screen_size((width, height))

            if key_pressed[keybind.QUIT_PROGRAM]:  # Exit keybind
                pygame.quit()
                sys.exit()

            if event.type == pygame.QUIT:  # Exit from button
                pygame.quit()
                sys.exit()

            # To only register a single press.
            if event.type == pygame.KEYUP:
                if key_pressed[keybind.CHANGE_MODE_UP]:
                    self.change_mode()
                if key_pressed[keybind.CHANGE_MODE_DOWN]:
                    self.change_mode()
                if key_pressed[keybind.CHANGE_DIF_UP]:
                    self.change_dif(1)  # Up
                if key_pressed[keybind.CHANGE_DIF_DOWN]:
                    self.change_dif(-1)  # Down
            if key_pressed[keybind.START_GAME]:
                return True
        return False

    def store_window_size(self) -> None:
        # Storing window size in case of window resize
        window_surface = pygame.display.get_surface()
        window_width = window_surface.get_width()
        window_height = window_surface.get_height()

        self.game_values.set_screen_size((window_width, window_height))

        constant.START_SOUND.play()

    def change_mode(self) -> None:
        mode = self.game_values.get_mode()
        mode += 1

        if mode > 2:
            mode = 1
        self.game_values.set_mode(mode)  # Stores new value

        constant.SETTING_CHANGE_SOUND.play()

    def change_dif(self, num) -> None:
        if not self.game_values.get_mode() == 1:
            return  # Only allowing difficulty changing when 1-player is selected

        difficulty = self.game_values.get_difficulty()
        difficulty += num

        if difficulty > 3:
            difficulty = 1
        elif difficulty < 1:
            difficulty = 3
        self.game_values.set_difficulty(difficulty)  # Stores new value

        constant.SETTING_CHANGE_SOUND.play()

    def display_text(self, text: str, x: float, y: float, font: pygame.font) -> None:
        txt = font.render(f'{text}', True, constant.TEXT_COLOR, None)
        txt_rect = txt.get_rect()
        txt_rect.center = x, y
        self.screen.blit(txt, txt_rect)
