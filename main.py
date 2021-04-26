#!/usr/bin/env python3

import turtle
import os
import sys
import game

if os.name == "nt":
    import winsound


class MainMenu(object):
    """Main menu creates a 800 x 600 window to allow you to view the controls, change the grid size, start the game, and quit the game."""

    MENU = "MENU"
    GAME = "GAME"
    QUIT = "QUIT"

    def __init__(self):
        turtle.setundobuffer(None)
        turtle.tracer(0)
        self.screen = turtle.Screen()
        self.window_width, self.window_height = (800, 600)
        self.set_screen()
        self.screen_stack = ["main"]
        self.create_pens()
        self.display_main()
        self.cursor_positions = 3
        self.options = {
            "grid_size": {
                "value": 2,
                "min": 1,
                "max": 3,
                "labels": ["Small", "Medium", "Large"],
            },
            "relative_controls": {"value": False},
            "humans": {"value": 1, "min": 1, "max": 2},
            "bots": {"value": 1, "min": 0, "max": 3},
            "difficulty": {
                "value": 1,
                "min": 1,
                "max": 3,
                "labels": ["Easy", "Normal", "Hard"],
            },
        }
        self.option_pos_map = {5: "humans", 4: "bots", 3: "difficulty", 2: "grid_size"}
        self.state = self.MENU

    def set_screen(self):
        """Create medium sized main menu."""
        self.screen.bgcolor("black")
        self.screen.bgpic("images/main_menu.gif")
        self.screen.setup(self.window_width, self.window_height)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_pens(self):
        """Create selection cursor and text pen for option values."""
        self.create_cursor()
        self.create_text_pen()

    def create_cursor(self):
        self.pen = turtle.Turtle()
        self.pen.shapesize(stretch_wid=3, stretch_len=3, outline=None)
        self.pen.cursor_pos = 3
        self.pen.pencolor("#40BBE3")
        self.pen.penup()
        self.pen.showturtle()

    def create_text_pen(self):
        self.text_pen = turtle.Turtle()
        self.text_pen.color("white")
        self.text_pen.penup()
        self.text_pen.hideturtle()

    def set_cursor_controller(self):
        """Runs in start menu loop. Controlled by cursor_up and cursor_down functions."""
        if self.get_curr_screen() == "main":
            self.set_cursor_main()
        elif self.get_curr_screen() == "options":
            self.set_cursor_options()
        elif self.get_curr_screen() == "controls":
            self.set_cursor_controls()

    def set_cursor_main(self):
        """Main: Start = 3, Controls = 2, Quit = 1"""
        self.cursor_positions = 3
        if self.pen.cursor_pos == 1:
            self.pen.setposition(-82, -131)
        elif self.pen.cursor_pos == 2:
            self.pen.setposition(-82, -28)
        else:
            self.pen.setposition(-82, 74)

    def set_cursor_controls(self):
        """Controls: Relative = 1, Absolute = 2."""
        self.cursor_positions = 2
        if self.pen.cursor_pos == 1:
            self.pen.setposition(-285, -215)
        else:
            self.pen.setposition(145, -215)
        self.display_controls()

    def set_cursor_options(self):
        self.cursor_positions = 5
        if self.pen.cursor_pos == 5:
            self.pen.setposition(-325, 130)
        elif self.pen.cursor_pos == 4:
            self.pen.setposition(-325, 65)
        elif self.pen.cursor_pos == 3:
            self.pen.setposition(-325, 0)
        elif self.pen.cursor_pos == 2:
            self.pen.setposition(-325, -65)
        else:
            self.pen.setposition(-325, -130)

    def cursor_up(self):
        """Increase cursor pos by 1."""
        if self.pen.cursor_pos < self.cursor_positions:
            self.pen.cursor_pos += 1

    def cursor_down(self):
        """Decrease cursor pos by 1."""
        if self.pen.cursor_pos > 1:
            self.pen.cursor_pos -= 1

    def increment_value(self):
        """Increases value for option according to cursor position."""
        if self.pen.cursor_pos in self.option_pos_map:
            key = self.option_pos_map[self.pen.cursor_pos]
            max_value = self.options[key]["max"]
            if self.options[key]["value"] < max_value:
                self.options[key]["value"] += 1
                self.draw_option_values()

    def decrement_value(self):
        """Decreases value for option according to cursor position."""
        if self.pen.cursor_pos in self.option_pos_map:
            key = self.option_pos_map[self.pen.cursor_pos]
            min_value = self.options[key]["min"]
            if self.options[key]["value"] > min_value:
                self.options[key]["value"] -= 1
                self.draw_option_values()

    def set_keyboard_bindings(self):
        """Sets bindings depending on which screen is displayed. Either player
        can control cursor.
        """
        turtle.listen()
        if self.get_curr_screen() == "main":
            turtle.onkeypress(self.cursor_up, "Up")
            turtle.onkeypress(self.cursor_up, "w")
            turtle.onkeypress(self.cursor_down, "Down")
            turtle.onkeypress(self.cursor_down, "s")
            turtle.onkeypress(None, "a")
            turtle.onkeypress(None, "d")
            turtle.onkeypress(None, "Left")
            turtle.onkeypress(None, "Right")
        elif self.get_curr_screen() == "controls":
            turtle.onkeypress(self.cursor_up, "Right")
            turtle.onkeypress(self.cursor_up, "d")
            turtle.onkeypress(self.cursor_down, "Left")
            turtle.onkeypress(self.cursor_down, "a")
        elif self.get_curr_screen() == "options":
            turtle.onkeypress(self.cursor_up, "Up")
            turtle.onkeypress(self.cursor_up, "w")
            turtle.onkeypress(self.cursor_down, "Down")
            turtle.onkeypress(self.cursor_down, "s")
            turtle.onkeypress(self.decrement_value, "a")
            turtle.onkeypress(self.increment_value, "d")
            turtle.onkeypress(self.decrement_value, "Left")
            turtle.onkeypress(self.increment_value, "Right")

        # Apply special function to return or space
        turtle.onkeypress(self.press_enter_or_space_controller, "Return")
        turtle.onkeypress(self.press_enter_or_space_controller, "space")
        turtle.onkeypress(self.pop_from_screen_stack, "Escape")

    def pop_from_screen_stack(self):
        if len(self.screen_stack) > 1:
            self.screen_stack.pop()
            self.display_controller()

    def get_curr_screen(self):
        return self.screen_stack[-1]

    def display_controller(self):
        if self.get_curr_screen() == "main":
            self.display_main()
        elif self.get_curr_screen() == "options":
            self.display_options()
        elif self.get_curr_screen() == "controls":
            self.display_controls()

    def press_enter_or_space_controller(self):
        """Depending on the current screen, passes the action to its corresponding function."""
        if self.get_curr_screen() == "main":
            self.press_enter_or_space_main()
        elif self.get_curr_screen() == "options":
            self.press_enter_or_space_options()
        elif self.get_curr_screen() == "controls":
            self.press_enter_or_space_controls()

    def press_enter_or_space_main(self):
        """Controls how enter or space function depending on the cursor position for the main screen."""
        if self.pen.cursor_pos == 3:
            self.screen.clear()
            self.state = self.GAME
        elif self.pen.cursor_pos == 2:
            self.screen_stack.append("options")
            self.display_options()
        elif self.pen.cursor_pos == 1:
            self.state = self.QUIT

    def press_enter_or_space_controls(self):
        """Controls how enter or space function depending on the cursor position
        for the controls screen.
        """
        if self.pen.cursor_pos == 1:
            self.options["relative_controls"]["value"] = True
        else:
            self.options["relative_controls"]["value"] = False
        self.pop_from_screen_stack()

    def press_enter_or_space_options(self):
        """Controls how enter or space function depending on the cursor position
        for the grid size screen.
        """
        if self.pen.cursor_pos == 1:
            relative_controls = self.options["relative_controls"]["value"]
            self.pen.cursor_pos = 1 if relative_controls else 2
            self.screen_stack.append("controls")
            self.display_controls()
            self.text_pen.clear()

    def display_controls(self):
        """Displays control screen. User can choose between relative or absolute
        control scheme.
        """
        img_name = "controls_absolute"
        if self.pen.cursor_pos == 1:
            img_name = "controls_relative"
        self.screen.bgpic(f"images/{img_name}.gif")

    def display_main(self):
        """Displays the main menu."""
        self.text_pen.clear()
        self.screen.bgpic("images/main_menu.gif")

    def display_options(self):
        """Display game options. Option values are controlled by self.text_pen."""
        self.pen.cursor_pos = 5
        self.screen.bgpic("images/options.gif")
        self.draw_option_values()

    def draw_option_values(self):
        self.text_pen.clear()
        y_offset = 110
        options = [
            self.options["humans"],
            self.options["bots"],
            self.options["difficulty"],
            self.options["grid_size"],
        ]
        for option in options:
            self.text_pen.setposition(200, y_offset)
            self.text_pen.pendown()
            value = option["value"]
            if "labels" in option:
                idx = option["value"] - 1
                value = option["labels"][idx]
            self.text_pen.write(value, align="center", font=("Helvetica", 28, "bold"))
            self.text_pen.penup()
            y_offset -= 65

    def reset_menu(self):
        self.stop_music()
        self.set_screen()
        self.display_main()
        self.create_cursor()
        self.start_music()

    def stop_music(self):
        if os.name == "posix":
            os.system("killall afplay")
        elif os.name == "nt":
            winsound.PlaySound(None, winsound.SND_PURGE)

    def start_music(self):
        bgm_path = "sounds/main_menu.wav"
        if os.name == "posix":
            os.system(f"afplay {bgm_path}&")
        elif os.name == "nt":
            winsound.SND_ASYNC
            winsound.PlaySound(bgm_path, winsound.SND_ASYNC)

    def start_menu(self):
        """Main menu loop."""
        self.start_music()

        # Change cursor position based on keybindings
        while self.state == self.MENU:
            self.set_cursor_controller()
            self.set_keyboard_bindings()
            self.screen.update()
            while self.state == self.GAME:
                self.stop_music()
                # Trim options dict to only contain name and value
                options = {key: value["value"] for key, value in self.options.items()}
                gameObj = game.Game(**options)
                gameObj.start_game()
                self.state = self.MENU
                self.reset_menu()

        if self.state == "QUIT":
            self.quit()

    def quit(self):
        self.stop_music()
        turtle.bye()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise SystemExit("Python 3 required!")
    menu = MainMenu()
    menu.start_menu()
