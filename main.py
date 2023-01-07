#!/usr/bin/env python3

from game_files.menu import Menu
from game_files.game import Game
from settings.game_values import GameSettings


def main():
    game_values = GameSettings()

    menu = Menu(game_values)
    game = Game(game_values)

    while True:
        menu.run()
        game.run()


if __name__ == '__main__':
    main()
