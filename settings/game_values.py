import settings.constant as constant
import settings.text_norwegian as text
# import settings.text_english as text


class GameSettings:
    def __init__(self):
        """
        Object with setters and getters for variable global values
        """
        self.screen_size = [1080, 720]
        self.game_title = constant.GAME_NAME
        self.start_text = text.START_TEXT
        self.setting_text = text.SETTING_TEXT
        # Placeholder text

        self.mode = 1  # Single player as default
        self.difficulty = 1  # Easy as default
        self.random_y_offset = 0.0  # Hard AI tries to hit the ball at a wierd angle to prevent predictions

    def get_game_title(self) -> str:
        return self.game_title

    def set_game_title(self, text: str):
        self.game_title = text

    def get_screen_size(self) -> list:
        return self.screen_size

    def set_screen_size(self, size: list):
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

    def get_random_y_offset(self) -> float:
        return self.random_y_offset

    def set_random_y_offset(self, num: float):
        self.random_y_offset = num
