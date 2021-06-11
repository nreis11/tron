from pen import Pen
from screen import Screen

defaults = {
    "grid_size": {
        "value": 2,
        "min": 1,
        "max": 3,
        "labels": ["Small", "Medium", "Large"],
    },
    "bots": {"value": 1, "min": 0, "max": 3},
    "difficulty": {
        "value": 1,
        "min": 1,
        "max": 3,
        "labels": ["Easy", "Normal", "Hard"],
    },
}


class OptionsScreen(Screen):
    def __init__(self, name):
        super().__init__(name)
        self.options = defaults
        self.option_pos_map = {4: "bots", 3: "difficulty", 2: "grid_size"}
        self.text_pen = Pen()

    def increment_value(self):
        """Increases value for option according to cursor position."""
        if self.curr_cursor_idx in self.option_pos_map:
            name = self.option_pos_map[self.curr_cursor_idx]
            max_value = self.options[name]["max"]
            curr_value = self.get_option_value(name)
            if curr_value < max_value:
                self.set_option_value(name, curr_value + 1)
                self.draw_option_values()

    def decrement_value(self):
        """Decreases value for option according to cursor position."""
        if self.curr_cursor_idx in self.option_pos_map:
            name = self.option_pos_map[self.curr_cursor_idx]
            min_value = self.options[name]["min"]
            curr_value = self.get_option_value(name)
            if curr_value > min_value:
                self.set_option_value(name, curr_value - 1)
                self.draw_option_values()

    def get_option_value(self, name):
        return self.options[name]["value"]

    def set_option_value(self, name, value):
        self.options[name]["value"] = value

    def draw_option_values(self):
        self.text_pen.clear()
        y_offset = 180
        options = [
            self.options["bots"],
            self.options["difficulty"],
            self.options["grid_size"],
        ]
        for option in options:
            self.text_pen.setposition(300, y_offset)
            self.text_pen.pendown()
            value = option["value"]
            if "labels" in option:
                idx = option["value"] - 1
                value = option["labels"][idx]
            self.text_pen.write(value, align="center", font=self.text_pen.font)
            self.text_pen.penup()
            y_offset -= 140
