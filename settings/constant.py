import pygame

FPS = 60
GAME_NAME = 'Pong 1.6'
POINT_LIMIT = 10  # Playing to and included
SCREEN_MIN_WIDTH = 800
SCREEN_MIN_HEIGHT = 500
SCREEN_OFFSET = 10  # Similar to padding in CSS

# Dark mode
BACKGROUND_COLOR = 47, 50, 58
PADDLE_COLOR = 255, 255, 255
BALL_COLOR = 255, 255, 255
TEXT_COLOR = 255, 255, 255
SETTINGS_TEXT_COLOR = 100, 100, 100

# Light mode
# BACKGROUND_COLOR = 228, 229, 241
# PADDLE_COLOR = 72, 75, 106
# BALL_COLOR = 72, 75, 106
# TEXT_COLOR = 72, 75, 106
# SETTINGS_TEXT_COLOR = 255, 255, 255


PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
PADDLE_SPEED = 10
PADDLE_1_POS = 20
PADDLE_2_POS = PADDLE_WIDTH + 20  # Width of display minus this value

BALL_SIZE = 10
BALL_START_SPEED = 10
BALL_SPEED_INCREMENT = 1

pygame.mixer.init()

START_SOUND = pygame.mixer.Sound('etc/start_win.wav')
SETTING_CHANGE_SOUND = pygame.mixer.Sound('etc/setting.wav')
PAUSE_SOUND = pygame.mixer.Sound('etc/pause.mp3')
WIN_SOUND = pygame.mixer.Sound('etc/start_win.wav')
PADDLE_HIT_SOUND = pygame.mixer.Sound('etc/paddle_hit.wav')
WALL_HIT_SOUND = pygame.mixer.Sound('etc/ground_roof_hit.wav')
SCORE_SOUND = pygame.mixer.Sound('etc/wall_hit.wav')

MENU_BACKGROUND_MUSIC = pygame.mixer.Sound('etc/menu_background_music.mp3')
GAME_BACKGROUND_MUSIC = pygame.mixer.Sound('etc/game_background_music.mp3')