import pygame

pygame.mixer.init()

FPS = 60
GAME_NAME = 'Pong 1.6'
POINT_LIMIT = 10  # Playing to and included
SCREEN_MIN_WIDTH = 800
SCREEN_MIN_HEIGHT = 500

# Color
BACKGROUND_COLOR = 47, 50, 58
PADDLE_COLOR = 255, 255, 255
BALL_COLOR = 255, 255, 255
TEXT_COLOR = 255, 255, 255

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
PADDLE_LIMIT = 10  # pixels from top of surface to the bar
PADDLE_SPEED = 10
PADDLE_1_POS = 20
PADDLE_2_POS = PADDLE_WIDTH + 20  # Width of display minus this value

BALL_SIZE = 10
BALL_START_SPEED = 10
BALL_SPEED_INCREMENT = 1

GAME_DEV = 'Laget av Jonas'
START_TEXT = 'Trykk mellomrom for å starte'
SETTING_TEXT = 'Bruk piltastene for å endre instillinger'

EASY_TEXT = '< Nybegynner >'
HARD_TEXT = '< Vanskelig >'
IMPOSSIBLE_TEXT = '< Umulig >'

ONE_PLAYER = '1-spiller'
TWO_PLAYER_LOCAL = '2-spiller'

PAUSE_TEXT = 'Spill pauset!'
UNPAUSE_TEXT = 'Trykk ESC for å fortsette'
PAUSE_EXIT = 'Trykk Enter for å avslutte'

START_SOUND = pygame.mixer.Sound('etc/start_win.wav')
SETTING_CHANGE_SOUND = pygame.mixer.Sound('etc/setting.wav')
PAUSE_SOUND = pygame.mixer.Sound('etc/pause.mp3')
WIN_SOUND = pygame.mixer.Sound('etc/start_win.wav')
PADDLE_HIT_SOUND = pygame.mixer.Sound('etc/paddle_hit.wav')
WALL_HIT_SOUND = pygame.mixer.Sound('etc/ground_roof_hit.wav')
SCORE_SOUND = pygame.mixer.Sound('etc/wall_hit.wav')