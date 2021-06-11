#!/usr/bin/env python3

from game import Game
from pen import Pen
from sound import Sound
from screen import Screen
from option_screen import OptionsScreen
import turtle
import os
import sys

if os.name == "nt":
    import winsound

main_screen = Screen("main")
options_screen = OptionsScreen("options")
controls_screen = Screen("controls")


class MainMenu:
    """Main menu creates a window to allow you to view the controls, edit options, start the game, and quit the game."""

    MENU = "MENU"
    GAME = "GAME"
    QUIT = "QUIT"

    def __init__(self, testing=False):
        turtle.setundobuffer(None)
        turtle.tracer(0)
        self.testing = testing
        self.window_width, self.window_height = (1.0, 1.0)
        self.screen_idx = 0
        self.screens = [main_screen, options_screen, controls_screen]
        self.screen = turtle.Screen()
        self.init_screen()
        self.audio = Sound()
        self.create_cursor()
        self.display_controller()
        self.humans = 1
        self.state = self.MENU

    def init_screen(self):
        """Create maximized main menu screen."""
        bg = self.get_curr_screen().bg
        self.screen.bgcolor("black")
        self.screen.bgpic(bg)
        self.screen.setup(self.window_width, self.window_height)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_cursor(self):
        self.cursor = turtle.Turtle()
        self.cursor.shape("square")
        self.cursor.shapesize(stretch_wid=0.4, stretch_len=1.1)
        self.cursor.pencolor("#40BBE3")
        self.cursor.penup()
        self.cursor.showturtle()

    def get_options_screen(self):
        return self.screens[1]

    def set_cursor_controller(self):
        """Runs in start menu loop."""
        curr_screen = self.get_curr_screen()
        cursor_pos = curr_screen.get_cursor_pos()
        self.cursor.setpos(cursor_pos)

    def set_keyboard_bindings(self):
        """Sets bindings depending on which screen is displayed. Either player can control cursor. """
        turtle.listen()
        curr_screen = self.get_curr_screen()
        if curr_screen.name == "main":
            turtle.onkeypress(curr_screen.cursor_up, "Up")
            turtle.onkeypress(curr_screen.cursor_up, "w")
            turtle.onkeypress(curr_screen.cursor_down, "Down")
            turtle.onkeypress(curr_screen.cursor_down, "s")
            turtle.onkeypress(None, "a")
            turtle.onkeypress(None, "d")
            turtle.onkeypress(None, "Left")
            turtle.onkeypress(None, "Right")
        elif curr_screen.name == "controls":
            turtle.onkeypress(curr_screen.cursor_up, "Right")
            turtle.onkeypress(curr_screen.cursor_up, "d")
            turtle.onkeypress(curr_screen.cursor_down, "Left")
            turtle.onkeypress(curr_screen.cursor_down, "a")
        elif curr_screen.name == "options":
            turtle.onkeypress(curr_screen.cursor_up, "Up")
            turtle.onkeypress(curr_screen.cursor_up, "w")
            turtle.onkeypress(curr_screen.cursor_down, "Down")
            turtle.onkeypress(curr_screen.cursor_down, "s")
            turtle.onkeypress(curr_screen.decrement_value, "a")
            turtle.onkeypress(curr_screen.increment_value, "d")
            turtle.onkeypress(curr_screen.decrement_value, "Left")
            turtle.onkeypress(curr_screen.increment_value, "Right")

        # Apply special function to return or space
        turtle.onkeypress(self.handle_enter_or_space_controller, "Return")
        turtle.onkeypress(self.handle_enter_or_space_controller, "space")
        turtle.onkeypress(self.prev_screen, "Escape")

    def next_screen(self):
        self.screen_idx += 1
        self.display_controller()

    def prev_screen(self):

        if hasattr(self.get_curr_screen(), "text_pen"):
            self.get_curr_screen().text_pen.clear()

        if self.screen_idx > 0:
            self.screen_idx -= 1
            self.display_controller()

    def get_curr_screen(self):
        return self.screens[self.screen_idx]

    def display_controller(self):
        curr_screen = self.get_curr_screen()
        self.screen.bgpic(curr_screen.bg)
        if curr_screen.name == "options":
            curr_screen.draw_option_values()

    def handle_enter_or_space_controller(self):
        """Depending on the current screen, passes the action to its corresponding function."""
        curr_screen = self.get_curr_screen().name
        if curr_screen == "main":
            self.handle_enter_or_space_main()
        elif curr_screen == "options":
            self.handle_enter_or_space_options()
        elif curr_screen == "controls":
            self.handle_enter_or_space_controls()

    def handle_enter_or_space_main(self):
        """Controls how enter or space function depending on the cursor position for the main screen."""
        cursor_idx = self.get_curr_screen().curr_cursor_idx
        if cursor_idx == 4:
            self.screen.clear()
            self.state = self.GAME
        elif cursor_idx == 3:
            self.humans = 2
            self.screen.clear()
            self.state = self.GAME
        elif cursor_idx == 2:
            self.next_screen()
        elif cursor_idx == 1:
            self.state = self.QUIT

    def handle_enter_or_space_controls(self):
        """Controls how enter or space function depending on the cursor position for the controls screen. """
        self.prev_screen()

    def handle_enter_or_space_options(self):
        """Controls how enter or space function depending on the cursor position for the options screen. """
        curr_screen = self.get_curr_screen()
        if curr_screen.curr_cursor_idx == 1:
            curr_screen.text_pen.clear()
            self.next_screen()

    def reset_menu(self):
        self.audio.stop_music()
        self.init_screen()
        self.display_controller()
        self.create_cursor()
        self.audio.start_music("main_menu")

    def start_menu(self):
        """Main menu loop."""
        if not self.testing:
            self.audio.start_music("main_menu")

        # Change cursor position based on keybindings
        while self.state == self.MENU:
            self.set_cursor_controller()
            self.set_keyboard_bindings()
            self.screen.update()
            while self.state == self.GAME:
                self.audio.stop_music()
                # Trim options dict to only contain name and value
                options = {
                    key: value["value"]
                    for key, value in self.get_options_screen().options.items()
                }
                gameObj = Game(**options, humans=self.humans, testing=self.testing)
                gameObj.start_game()
                self.state = self.MENU
                self.reset_menu()

        if self.state == self.QUIT:
            self.quit()

    def quit(self):
        self.audio.stop_music()
        turtle.bye()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise SystemExit("Python 3 required!")
    menu = MainMenu(True)
    menu.start_menu()
