#!/usr/bin/env python3

from game_files.menu import Menu
from game_files.game import Game
from settings.game_values import GameValues


def main():
    game_values = GameValues()

    menu = Menu(game_values)
    game = Game(game_values)

    while True:
        menu.run()
        game.run()


if __name__ == '__main__':
    main()
