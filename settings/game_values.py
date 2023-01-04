import settings.constant as constant


class GameSettings:
    def __init__(self):
        """
        Object with setters and getters for variable values
        """
        self.screen_size = (1080, 720)
        self.game_title = constant.GAME_NAME
        self.start_text = constant.START_TEXT
        self.setting_text = constant.SETTING_TEXT

        self.mode = 1  # Single player as default
        self.difficulty = 1  # Easy as default

    def get_game_title(self) -> str:
        return self.game_title

    def set_game_title(self, text: str):
        self.game_title = text

    def get_screen_size(self) -> tuple:
        return self.screen_size

    def set_screen_size(self, size: tuple):
        self.screen_size = size

    def get_start_text(self) -> str:
        return self.start_text

    def set_start_text(self, text: str):
        self.start_text = text

    def get_setting_text(self) -> str:
        return self.setting_text

    def set_setting_text(self, text: str):
        self.setting_text = text

    def get_mode(self) -> int:
        return self.mode

    def set_mode(self, num: int):
        self.mode = num

    def get_difficulty(self) -> int:
        return self.difficulty

    def set_difficulty(self, num: int):
        self.difficulty = num