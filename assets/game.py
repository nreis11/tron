#!/usr/bin/env python3

import turtle
import time
import os
import random
from assets import particle
from assets import player


class Game(object):
    """Creates screen, draws border, creates all sprites, maps keys, draws score, and
    runs game loop."""

    def __init__(self, width=None, height=None, relative_controls=False):
        self.width = width
        self.height = height
        self.relative_controls = relative_controls
        self.game_on = True
        self.testing = True
        turtle.setundobuffer(1)

    def screen_size(self):
        """Only used if script runs directly."""
        size = ""
        while True:
            size = input("Grid size: (Small, Medium, Large) ").lower().strip()
            if size == "small":
                return (640, 480)
            elif size == "medium":
                return (800, 600)
            elif size == "large":
                return (1024, 768)
            else:
                print("{} is not a valid size.".format(size))

    def create_screen(self):
        """If run directly, creates screen based on user choice from self.screen_size().
        Otherwise, screen is automatically created with arguments from main.py script."""
        if not self.width or not self.height:
            self.width, self.height = self.screen_size()
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(self.width, self.height, startx=None, starty=None)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_border(self):
        """Border is drawn from the width and height, starting in upper
        right hand corner. Each side is 50 pixels from the edge of the screen.
        The border coordinates will be used for border detection as well."""
        self.x_boundary = (self.width / 2) - 50
        self.y_boundary = (self.height / 2) - 50
        self.border_pen.penup()
        self.border_pen.setposition(self.x_boundary, self.y_boundary)
        self.border_pen.pendown()
        self.border_pen.setheading(180)  # Start drawing west
        # Square is drawn
        for side in range(4):
            # Vertical
            if side % 2:
                self.border_pen.forward(self.height - 100)
                self.border_pen.left(90)
            # Horizontal
            else:
                self.border_pen.forward(self.width - 100)
                self.border_pen.left(90)
        self.border_pen.penup()
        self.border_pen.hideturtle()

    def random_coord(self):
        """Generates random coordinate within playable area with 50 px padding from boundary"""
        x = random.randint(-(self.x_boundary - 50), (self.x_boundary - 50))
        y = random.randint(-(self.y_boundary - 50), (self.y_boundary - 50))
        return (x, y)

    def is_outside_boundary(self, player):
        """Checks if light cycle is out of bounds using border coord.
        Deviation of 3 on edge to cosmetically match impact."""
        if (
            abs(player.xcor()) > abs(self.x_boundary) - self.border_pen.pensize()
            or abs(player.ycor()) > abs(self.y_boundary) - self.border_pen.pensize()
        ):
            return True

    def position_range_adder(self, player):
        """If speed is > 1, the positions aren't recorded between the speed gap. Therefore,
        this function is needed to fill in the gaps and append the missing positions"""
        prev_x_pos, prev_y_pos = player.positions[-2]  # tuple unpacking
        next_x_pos, next_y_pos = player.positions[-1]
        positions_range = []
        # X coord are changing and the difference between them is greater than 1
        if abs(prev_x_pos - next_x_pos) > 1:
            start = min(prev_x_pos, next_x_pos) + 1
            end = max(prev_x_pos, next_x_pos)
            for x_position in range(start, end):
                coord = (x_position, prev_y_pos)
                positions_range.append(coord)
        # Y coord are changing and the difference between them is greater than 1
        elif abs(prev_y_pos - next_y_pos) > 1:
            start = min(prev_y_pos, next_y_pos) + 1
            end = max(prev_y_pos, next_y_pos)
            for y_position in range(start, end):
                coord = (prev_x_pos, y_position)
                positions_range.append(coord)
        # Unique coordinates to add
        if positions_range:
            for position in positions_range:
                if position not in player.positions:
                    player.positions.append(position)

    def create_player(self, number=2):
        """Two players are always created. P1 is blue.
        P2 is Yellow, P3 is Red, P4 is Green"""

        if number > 4:
            raise ValueError("No more than 4 players allowed.")

        self.players = []
        colors = ["#40BBE3", "#E3E329", "#ff0000", "#33cc33"]

        for i in range(number):
            x, y = self.random_coord()
            self.players.append(player.Player("P" + str(i + 1), x, y))
            self.players[i].color(colors[i])

    def create_particles(self):
        """Creates particles list. All particles act in same manner."""
        self.particles = []
        for i in range(20):
            self.particles.append(particle.Particle())

    def particles_explode(self, player):
        """Makes all particles explode at player crash position"""
        for particle in self.particles:
            particle.change_color(player)
            particle.explode(player.xcor(), player.ycor())

    def is_collision_with_enemy(self, player):
        """Collision check with other player."""
        # Get the current position, iterate through the positions list, and don't check its own
        # positions, check if position is in list
        for i in range(len(self.players)):
            if player.name != self.players[i].name:
                for position in player.positions[-5:]:
                    if position in self.players[i].positions:
                        return True

    def is_collision_with_self(self, player):
        for position in player.positions[
            -10:
        ]:  # Multiple positions to cover speed gap (0 - 3)
            if position in player.positions[:-10]:
                return True

    def set_relative_keyboard_bindings(self):
        """Maps relative controls to player movement."""
        # Set P1 keyboard bindings
        turtle.onkeypress(self.players[0].turn_left, "a")
        turtle.onkeypress(self.players[0].turn_right, "d")
        turtle.onkeypress(self.players[0].accelerate, "w")
        turtle.onkeypress(self.players[0].decelerate, "s")

        # Set P2 keyboard bindings
        turtle.onkeypress(self.players[1].turn_left, "Left")
        turtle.onkeypress(self.players[1].turn_right, "Right")
        turtle.onkeypress(self.players[1].accelerate, "Up")
        turtle.onkeypress(self.players[1].decelerate, "Down")

    def set_abs_keyboard_bindings(self):
        """Maps absolute controls to player movement."""

        # Set P1 keyboard bindings
        if self.players[0].heading() == 0:  # East
            self.abs_key_mapper(self.players[0], "w", "s", "d", "a")
        elif self.players[0].heading() == 90:  # North
            self.abs_key_mapper(self.players[0], "a", "d", "w", "s")
        elif self.players[0].heading() == 180:  # West
            self.abs_key_mapper(self.players[0], "s", "w", "a", "d")
        elif self.players[0].heading() == 270:  # South
            self.abs_key_mapper(self.players[0], "d", "a", "s", "w")
        # Set P2 keyboard bindings
        if self.players[1].heading() == 0:  # East
            self.abs_key_mapper(self.players[1], "Up", "Down", "Right", "Left")
        elif self.players[1].heading() == 90:  # North
            self.abs_key_mapper(self.players[1], "Left", "Right", "Up", "Down")
        elif self.players[1].heading() == 180:  # West
            self.abs_key_mapper(self.players[1], "Down", "Up", "Left", "Right")
        elif self.players[1].heading() == 270:  # South
            self.abs_key_mapper(self.players[1], "Right", "Left", "Down", "Up")

    def abs_key_mapper(self, player, left, right, accel, decel):
        """Maps passed in args to player controls"""
        turtle.onkeypress(player.turn_left, left)
        turtle.onkeypress(player.turn_right, right)
        turtle.onkeypress(player.accelerate, accel)
        turtle.onkeypress(player.decelerate, decel)

    def draw_score(self):
        """Using a turtle, this draws the score on the screen once, then clears once
        the score changes. Start position is upper left corner. A dedicated score
        pen is needed because the clear function is called every time the score
        is updated."""
        self.score_pen.clear()
        self.score_pen.setposition((self.width / -2) + 75, (self.height / 2) - 40)
        self.score_pen.pendown()
        p1lives = "P1: %s" % (self.players[0].lives * "*")
        p2lives = "P2: %s" % (self.players[1].lives * "*")
        self.score_pen.write(p1lives, font=("Verdana", 18, "bold"))
        self.score_pen.penup()
        self.score_pen.setposition((self.width / -2) + 205, (self.height / 2) - 40)
        self.score_pen.pendown()
        self.score_pen.write(p2lives, font=("Verdana", 18, "bold"))
        self.score_pen.penup()

    def is_game_over(self):
        """Checks to see if any player has run out of lives."""
        for player in self.players:
            if player.lives == 0:
                return True

    def display_winner(self):
        """Once game loop finishes, this runs to display the winner."""
        self.game_text_pen.pendown()
        for player in self.players:
            if player.lives > 0:
                winner = player.name
        self.game_text_pen.write(
            winner + " wins!", align="center", font=("Verdana", 36, "bold")
        )

    def reset_grid(self):
        for player in self.players:
            x, y = self.random_coord()
            player.clear_lightcycle()
            player.respawn(x, y)

    def start_bgm(self):
        if os.name == "posix":
            os.system("killall afplay")
            os.system("afplay sounds/gameplay.m4a&")
            os.system("say grid is live!&")

    def countdown(self):
        for num in range(3, 0, -1):
            self.game_text_pen.pendown()
            self.game_text_pen.write(
                str(num), align="center", font=("Verdana", 36, "bold")
            )
            if os.name == "posix":
                os.system(f"say {num}&")
            time.sleep(1)
            self.game_text_pen.clear()

    def create_pens(self):
        """Self.pen is for the border."""
        self.border_pen = turtle.Turtle()
        self.score_pen = turtle.Turtle()
        self.game_text_pen = turtle.Turtle()

        self.border_pen.speed(0)
        self.border_pen.pensize(3)
        self.border_pen.color("blue")
        self.game_text_pen.hideturtle()
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.color("white")
        self.game_text_pen.color("white")
        self.game_text_pen.setposition(0, 0)

    def create_assets(self):
        self.create_screen()
        self.create_pens()
        self.create_border()
        self.create_player()
        self.create_particles()
        self.draw_score()
        if not self.testing:
            self.countdown()
            self.start_bgm()

    def start_game(self):
        """All players are set into motion, boundary checks, and collision checks
        run continuously until a player runs out of lives."""
        self.create_assets()

        while self.game_on:
            # Updates screen only when loop is complete
            turtle.update()
            # Set controls based on menu setting
            if self.relative_controls:
                self.set_relative_keyboard_bindings()
            else:
                self.set_abs_keyboard_bindings()

            # Activate key mappings
            turtle.listen()
            # Set players into motion and add converted coords to positions
            for player in self.players:
                player.forward(player.fwd_speed)
                player.convert_coord_to_int()
                player.positions.append(player.coord)

                # Detect collision with boundary, self, or enemy
                if (
                    self.is_outside_boundary(player)
                    or self.is_collision_with_enemy(player)
                    or self.is_collision_with_self(player)
                ):
                    player.lose_life()
                # Add missing positions to bridge position gaps
                if len(player.positions) > 1:
                    self.position_range_adder(player)

            # Particle movement
            for particle in self.particles:
                particle.move()

            # If a player crashes, particles explode and reset lightcycles
            for player in self.players:
                if player.status == player.CRASHED:
                    self.particles_explode(player)
                    if os.name == "posix":
                        os.system("afplay sounds/explosion.wav&")
                    self.reset_grid()
                    self.draw_score()

            if self.is_game_over():
                self.game_on = False

        # Game ends
        self.display_winner()
        time.sleep(2)
        self.screen.clear()
        if os.name == "posix":
            os.system("killall afplay")


if __name__ == "__main__":
    gameObj = Game()
    gameObj.start_game()
