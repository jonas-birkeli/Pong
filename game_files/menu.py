import pygame
import sys
import settings.constant as constant
import settings.keybind as keybind


class Menu:
    def __init__(self, game_settings):
        self.game_values = game_settings

        pygame.init()

        self.screen = pygame.display.set_mode(self.game_values.get_screen_size(), pygame.RESIZABLE, vsync=True)
        self.fps = pygame.time.Clock()
        pygame.display.set_caption(constant.GAME_NAME)
        pygame.display.set_icon(pygame.image.load('etc/pong_icon.png'))

        self.big_font = pygame.font.Font('etc/FFFFORWA.ttf', 60)
        self.normal_font = pygame.font.Font('etc/FFFFORWA.ttf', 35)
        self.small_font = pygame.font.Font('etc/FFFFORWA.ttf', 20)
        self.start_sound = pygame.mixer.Sound('etc/start_win.wav')
        self.setting_change_sound = pygame.mixer.Sound('etc/setting.wav')

    def start(self):
        while True:
            start_game = self.key_input()
            if start_game:
                self.start_game()
                return  # Exit loop

            # middle of screen ref
            surface = pygame.display.get_surface()
            sw2 = surface.get_width() / 2
            sh2 = surface.get_height() / 2

            self.screen.fill(constant.BACKGROUND_COLOR)
            self.display_text(self.game_values.get_game_title(), sw2, sh2 - 200, self.big_font)
            self.display_text(constant.GAME_DEV, sw2, sh2-120, self.small_font)
            self.display_text(self.game_values.get_start_text(), sw2, sh2, self.normal_font)

            # Mode
            mode = self.game_values.get_mode()
            if mode == 3:
                mode_text = constant.TWO_PLAYER_SOCKET
            elif mode == 2:
                mode_text = constant.TWO_PLAYER_LOCAL
            else:
                mode_text = constant.ONE_PLAYER

            # Difficulty
            difficulty = self.game_values.get_difficulty()
            if difficulty == 3:
                dif_text = constant.IMPOSSIBLE_TEXT
            elif difficulty == 2:
                dif_text = constant.HARD_TEXT
            else:
                dif_text = constant.EASY_TEXT

            self.display_text(mode_text, sw2, sh2+100, self.normal_font)
            if mode == 1:
                self.display_text(dif_text, sw2, sh2+150, self.normal_font)
            self.display_text(self.game_values.get_setting_text(), sw2, sh2 + 300, self.small_font)

            pygame.display.update()
            self.fps.tick(constant.FPS)

    def key_input(self) -> bool:
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if key_pressed[keybind.QUIT_PROGRAM]:
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # To only register a single press.
            if event.type == pygame.KEYUP:
                if key_pressed[keybind.CHANGE_MODE_UP]:
                    self.change_mode(1)
                if key_pressed[keybind.CHANGE_MODE_DOWN]:
                    self.change_mode(-1)
                if key_pressed[keybind.CHANGE_DIF_UP]:
                    self.change_dif(1)
                if key_pressed[keybind.CHANGE_DIF_DOWN]:
                    self.change_dif(-1)
        if key_pressed[keybind.START_GAME]:
            self.start_game()
            return True

    def start_game(self):
        # Storing window size in case of window resize
        window_surface = pygame.display.get_surface()
        window_width = window_surface.get_width()
        window_height = window_surface.get_height()
        self.game_values.set_screen_size((window_width, window_height))
        self.start_sound.play()

    def change_mode(self, num):
        mode = self.game_values.get_mode()
        mode += num
        if mode > 3:
            mode = 1
        elif mode < 1:
            mode = 3
        self.game_values.set_mode(mode)  # Stores new value
        self.setting_change_sound.play()

    def change_dif(self, num):
        if not self.game_values.get_mode() == 1:
            return  # Only allowing difficulty chaning when 1-player is selected
        difficulty = self.game_values.get_difficulty()
        difficulty += num
        if difficulty > 3:
            difficulty = 1
        elif difficulty < 1:
            difficulty = 3
        self.game_values.set_difficulty(difficulty)  # Stores new value
        self.setting_change_sound.play()

    def display_text(self, text, x, y, font):
        txt = font.render(f'{text}', True, constant.TEXT_COLOR, None)
        txt_rect = txt.get_rect()
        txt_rect.center = x, y
        self.screen.blit(txt, txt_rect)
