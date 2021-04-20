#!/usr/bin/env python3

import turtle
import os
import sys
import game


class MainMenu(object):
    """Main menu creates a 800 x 600 window to allow you to view the controls, change the grid size, start the game, and quit the game."""

    MENU = "MENU"
    GAME = "GAME"
    QUIT = "QUIT"

    def __init__(self):
        turtle.setundobuffer(1)
        self.screen = turtle.Screen()
        self.window_width, self.window_height = (800, 600)
        self.set_screen()
        self.create_cursor()
        self.create_text_pen()
        self.display_main()
        self.set_keyboard_bindings()
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
        # self.start_music()
        self.state = self.MENU

    def set_screen(self):
        """Create medium sized main menu."""
        self.screen.bgcolor("black")
        self.screen.bgpic("images/main_menu.gif")
        self.screen.setup(self.window_width, self.window_height)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

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
        if self.current_screen == "main":
            self.set_cursor_main()
        elif self.current_screen == "options":
            self.set_cursor_options()
        elif self.current_screen == "controls":
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
        key = self.option_pos_map[self.pen.cursor_pos]
        max_value = self.options[key]["max"]
        if self.options[key]["value"] < max_value:
            self.options[key]["value"] += 1
            self.draw_option_values()

    def decrement_value(self):
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
        if self.current_screen == "main":
            turtle.onkeypress(self.cursor_up, "Up")
            turtle.onkeypress(self.cursor_up, "w")
            turtle.onkeypress(self.cursor_down, "Down")
            turtle.onkeypress(self.cursor_down, "s")
        elif self.current_screen == "controls":
            turtle.onkeypress(self.cursor_up, "Right")
            turtle.onkeypress(self.cursor_up, "d")
            turtle.onkeypress(self.cursor_down, "Left")
            turtle.onkeypress(self.cursor_down, "a")
        elif self.current_screen == "options":
            turtle.onkeypress(self.cursor_up, "Up")
            turtle.onkeypress(self.cursor_up, "w")
            turtle.onkeypress(self.cursor_down, "Down")
            turtle.onkeypress(self.decrement_value, "a")
            turtle.onkeypress(self.increment_value, "d")
            turtle.onkeypress(self.decrement_value, "Left")
            turtle.onkeypress(self.increment_value, "Right")

        # Apply special function to return or space
        turtle.onkeypress(self.press_enter_or_space_master, "Return")
        turtle.onkeypress(self.press_enter_or_space_master, "space")
        turtle.onkeypress(self.display_main, "Escape")

    def press_enter_or_space_master(self):
        """Depending on the current screen, passes the action to its corresponding function."""
        if self.current_screen == "main":
            self.press_enter_or_space_main()
        elif self.current_screen == "options":
            self.press_enter_or_space_options()
        elif self.current_screen == "controls":
            self.press_enter_or_space_controls()

    def press_enter_or_space_main(self):
        """Controls how enter or space function depending on the cursor position for the main screen. """
        if self.pen.cursor_pos == 3:
            self.screen.clear()
            self.stop_music()
            self.state = self.GAME
        elif self.pen.cursor_pos == 2:
            self.display_options()
            # Needed to show saved control setting
        elif self.pen.cursor_pos == 1:
            self.state = self.QUIT

    def press_enter_or_space_controls(self):
        """Controls how enter or space function depending on the cursor position
        for the controls screen.
        """
        relative_controls = self.options["relative_controls"]["value"]
        if self.pen.cursor_pos == 1:
            relative_controls = True
        else:
            relative_controls = False
        self.pen.cursor_pos = 5  # Return to last main menu position
        self.display_options()

    def press_enter_or_space_options(self):
        """Controls how enter or space function depending on the cursor position
        for the grid size screen.
        """
        if self.pen.cursor_pos == 1:
            relative_controls = self.options["relative_controls"]["value"]
            if relative_controls:
                self.pen.cursor_pos = 1
            else:
                self.pen.cursor_pos = 2
            self.display_controls()
            self.text_pen.clear()

    def display_controls(self):
        """Displays control screen. User can choose between relative or absolute
        control scheme.
        """
        self.current_screen = "controls"
        if self.pen.cursor_pos == 1:
            self.screen.bgpic("images/controls_relative.gif")
        else:
            self.screen.bgpic("images/controls_absolute.gif")

    def display_main(self):
        """Displays the main menu."""
        self.text_pen.clear()
        self.current_screen = "main"
        self.screen.bgpic("images/main_menu.gif")

    def display_options(self):
        """Displays grid size options, after selecting to start."""
        self.pen.cursor_pos = 5
        self.current_screen = "options"
        self.screen.bgpic("images/options.gif")
        self.draw_option_values()

    def draw_option_values(self):
        self.text_pen.clear()
        y_offset = 110
        values = [
            self.options["humans"],
            self.options["bots"],
            self.options["difficulty"],
            self.options["grid_size"],
        ]
        for i, option in enumerate(values):
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
        self.set_screen()
        self.display_main()
        self.create_cursor()
        self.start_music()

    def stop_music(self):
        if os.name == "posix":
            os.system("killall afplay")

    def start_music(self):
        if os.name == "posix":
            self.stop_music()
            os.system("afplay sounds/main_menu.m4a&")

    def start_menu(self):
        """Main menu loop."""

        # Change cursor position based on keybindings
        while self.state == self.MENU:
            self.set_cursor_controller()
            self.set_keyboard_bindings()
            self.screen.update()
            while self.state == self.GAME:
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
