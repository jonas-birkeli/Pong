import pygame
import sys
import json

from network.client import Client
from network.server import Server


class Menu:
    def __init__(self):
        self.game = None
        pygame.init()

        with open('settings/constant.json') as f:
            self.constant_dict = json.loads(f.read())
        with open('settings/dynamic.json') as f:
            self.dynamic_dict = json.loads(f.read())
        with open('settings/keybind.json') as f:
            self.keybind_dict = json.loads(f.read())

        self.screen = pygame.display.set_mode(self.dynamic_dict['screen_size'], pygame.RESIZABLE, vsync=True)
        pygame.display.set_caption(self.constant_dict['GAME_NAME'])

        self.big_font = pygame.font.Font('etc/FFFFORWA.ttf', 60)
        self.normal_font = pygame.font.Font('etc/FFFFORWA.ttf', 35)
        self.small_font = pygame.font.Font('etc/FFFFORWA.ttf', 20)
        self.start_sound = pygame.mixer.Sound('etc/start_win.wav')
        self.setting_change_sound = pygame.mixer.Sound('etc/setting.wav')

        self.mode = 1  # 1-player, 2-player local, 2-player socket
        self.dif = 1  # Easy, Hard, Impossible
        self.connection_await = False  # if playing over socket, wait for connection.
        self.player_win = None

        self.client_try = False
        self.socket = None

    def start(self):
        while True:
            surface = pygame.display.get_surface()

            # middle of screen ref
            sw2 = surface.get_width() / 2
            sh2 = surface.get_height() / 2

            self.screen.fill(self.constant_dict['BACKGROUND_COLOR'])
            if not self.connection_await:  # Not awaiting connection from another player
                self.key_input()
            else:
                if not self.client_try:
                    self.initiate_client()
                else:
                    self.initiate_server()
                    self.socket_client = Server(self.constant_dict["HOST"], self.constant_dict["PORT"])

                # Await here for socket connection, add a visual clue
                if pygame.key.get_pressed() == self.keybind_dict['CANCEL_CONNECTION_AWAIT']:
                    self.connection_await = False

    def initiate_client(self):
        self.socket = Client(self.constant_dict["HOST"], self.constant_dict["PORT"])
        if self.socket.connect() == -1:
            self.client_try = True
        else:
            self.start_game()



    def initiate_server(self):
        pass

    def key_input(self):
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # To only register a single press.
            if event.type == pygame.KEYUP:
                if key_pressed == self.keybind_dict['CHANGE_MODE_UP']:
                    self.change_mode(1)
                if key_pressed == self.keybind_dict['CHANGE_MODE_DOWN']:
                    self.change_mode(-1)
                if key_pressed == self.keybind_dict['CHANGE_DIF_UP']:
                    self.change_dif(1)
                if key_pressed == self.keybind_dict['CHANGE_DIF_DOWN']:
                    self.change_dif(-1)

        if key_pressed == self.keybind_dict["START_GAME"]:
            if self.mode == 3:  # Socket
                self.connection_await = True
            else:
                self.start_game()

    def start_game(self, socket=0):
        if socket:
            pass  # Do something here

        # Storing window size in case of window resize
        window_surface = pygame.display.get_surface()
        window_width = window_surface.get_width()
        window_height = window_surface.get_height()
        self.dynamic_dict['SCREEN_SIZE'] = window_width, window_height

        self.game = Game(args)
        self.start_sound.play()
        self.player_win = self.game.run()  # Returns winning player
        self.game = None  # reset

    def change_mode(self, num):
        # Num to adjust mode with arrows.
        self.mode += num
        if self.mode > 3:
            self.mode = 1
        elif self.mode < 1:
            self.mode = 3
        self.setting_change_sound.play()

    def change_dif(self, num):
        self.dif += num
        if self.dif > 3:
            self.dif = 1
        elif self.dif < 1:
            self.dif = 3
        self.setting_change_sound.play()