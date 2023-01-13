import pygame
import sys

import settings.constant as constant
import settings.text_norwegian as text
# import settings.text_english as text
import settings.keybind as keybind


class Menu:
    def __init__(self, game_values):
        """
        Menu object, handles settings and general info
        :parameter game_values: ref
        """
        self.game_values = game_values

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
        if not self.game_values.get_music_muted():
            constant.MENU_BACKGROUND_MUSIC.play(loops=-1)
            # Background music if music not muted

        while True:

            start_game = self.key_input()
            if start_game:
                # User has hit the start button
                self.store_window_size()
                return  # Exit Menu

            screen_size = self.game_values.get_screen_size()
            middle_width = screen_size[0] / 2
            middle_height = screen_size[1] / 2
            # Screen is resizable

            self.screen.fill(constant.BACKGROUND_COLOR)
            self.display_text(self.game_values.get_game_title(), middle_width, middle_height*0.5, self.big_font)
            self.display_text(text.GAME_DEV, middle_width, middle_height*0.75, self.small_font, constant.SETTINGS_TEXT_COLOR)

            self.display_text(self.game_values.get_start_text(), middle_width, middle_height, self.normal_font)
            self.display_text(self.game_values.get_setting_text(), middle_width, middle_height*1.75, self.small_font, constant.SETTINGS_TEXT_COLOR)

            # Mute
            muted = self.game_values.get_music_muted()
            if muted:
                self.display_text(text.MUTE_TEXT, middle_width, middle_height*1.9, self.small_font, constant.SETTINGS_TEXT_COLOR)
            else:
                self.display_text(text.UNMUTE_TEXT, middle_width, middle_height*1.9, self.small_font, constant.SETTINGS_TEXT_COLOR)

            # Mode
            mode = self.game_values.get_mode()
            if mode == 2:
                mode_text = text.TWO_PLAYER_LOCAL
            else:
                mode_text = text.ONE_PLAYER

            self.display_text(mode_text, middle_width, middle_height*1.3, self.normal_font)

            # Difficulty
            difficulty = self.game_values.get_difficulty()
            if difficulty == 3:
                dif_text = text.IMPOSSIBLE_DIFFICULTY
            elif difficulty == 2:
                dif_text = text.HARD_DIFFICULTY
            else:
                dif_text = text.EASY_DIFFICULTY

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

                # Cap on small window sizes, as smaller breaks the game
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

                if key_pressed[keybind.MUTE]:
                    if self.game_values.get_music_muted():
                        self.game_values.set_music_muted(False)
                        constant.MENU_BACKGROUND_MUSIC.play()
                    else:
                        self.game_values.set_music_muted(True)
                        pygame.mixer.stop()
                        # Basic mute functon

                if key_pressed[keybind.CHANGE_MODE_UP]:
                    self.change_setting(name_space='mode', iterator=1, max=2)
                if key_pressed[keybind.CHANGE_MODE_DOWN]:
                    self.change_setting(name_space='mode', iterator=-1, max=2, )
                if key_pressed[keybind.CHANGE_DIF_UP]:
                    self.change_setting(name_space='difficulty', iterator=1, max=3)
                if key_pressed[keybind.CHANGE_DIF_DOWN]:
                    self.change_setting(name_space='difficulty', iterator=-1, max=3)

                if key_pressed[keybind.START_GAME]:
                    pygame.mixer.stop()
                    # Stops background music

                    # Input says start game
                    return True

        return False

    def store_window_size(self) -> None:
        # Storing window size in case of window resize
        window_surface = pygame.display.get_surface()
        window_width = window_surface.get_width()
        window_height = window_surface.get_height()

        self.game_values.set_screen_size((window_width, window_height))

        constant.START_SOUND.play()

    def change_setting(self, name_space: str, iterator: int, max: int, ) -> None:
        """
        Changes a setting by iterator up to max.
        :param iterator: num to iterate
        :param max: max value setting can have
        :param name_space: what value to change
        :return: None
        """
        if name_space == 'difficulty' and self.game_values.get_mode() != 1:
            # Changing difficulty while having 2-player selected does not make sense
            return

        num = 0

        # Get value
        if name_space == 'difficulty':
            num = self.game_values.get_difficulty()
        elif name_space == 'mode':
            num = self.game_values.get_mode()

        num += iterator

        if num > max:
            num = 1
        elif num < 1:
            num = max

        # Set value
        if name_space == 'difficulty':
            self.game_values.set_difficulty(num)
        elif name_space == 'mode':
            self.game_values.set_mode(num)

        constant.SETTING_CHANGE_SOUND.play()

    def display_text(self, text: str, x: float, y: float, font: pygame.font, text_color=constant.TEXT_COLOR) -> None:
        txt = font.render(f'{text}', True, text_color, None)
        txt_rect = txt.get_rect()
        txt_rect.center = x, y
        self.screen.blit(txt, txt_rect)
