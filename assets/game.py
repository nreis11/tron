#!/usr/bin/env python3

import turtle
import time
import os
import random

# from assets import particle
# from assets import player

import particle
import player


class Game(object):
    """Creates screen, draws border, creates all sprites, maps keys, draws score, and
    runs game loop."""

    GAME_FONT = ("Verdana", 36, "bold")

    def __init__(self, width=1200, height=800, relative_controls=False):
        turtle.setundobuffer(1)
        self.width = width
        self.height = height
        self.relative_controls = relative_controls
        self.out_of_bounds_length = 50
        self.grid = self.create_grid()
        self.players = []
        self.particles = []
        self.game_on = True
        self.testing = True
        self.create_assets()

    def create_grid(self):
        width = self.width - (self.out_of_bounds_length * 2)
        height = self.height - (self.out_of_bounds_length * 2)
        return [[0 for x in range(width)] for y in range(height)]

    def create_screen(self):
        """If run directly, creates screen based on user choice from self.screen_size().
        Otherwise, screen is automatically created with arguments from main.py script."""
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(self.width, self.height, startx=None, starty=None)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_border(self):
        """Border is drawn from the width and height, starting in upper
        right hand corner. Each side is 50 pixels from the edge of the screen.
        The border coordinates will be used for border detection as well."""
        self.x_boundary = (self.width // 2) - self.out_of_bounds_length
        self.y_boundary = (self.height // 2) - self.out_of_bounds_length
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

    def get_random_coord(self):
        """Generates random coordinate within playable area with 50 px padding from boundary"""
        x = random.randint(-(self.x_boundary - 50), (self.x_boundary - 50))
        y = random.randint(-(self.y_boundary - 50), (self.y_boundary - 50))
        return (x, y)

    def is_outside_boundary(self, player):
        """Checks if light cycle is out of bounds using border coord."""
        return (
            abs(player.xcor()) > abs(self.x_boundary) - self.border_pen.pensize()
            or abs(player.ycor()) > abs(self.y_boundary) - self.border_pen.pensize()
        )

    def position_range_adder(self, player):
        """If speed is > 1, the positions aren't recorded between the speed gap. Therefore,
        this function is needed to fill in the gaps and append the missing positions"""
        prev_xcor, prev_ycor = player.prev_pos  # tuple unpacking
        curr_xcor = int(player.xcor())
        curr_ycor = int(player.ycor())
        positions = []
        # X coord are changing and the difference between them is greater than 1
        if prev_xcor != curr_xcor:
            start = min(prev_xcor, curr_xcor)
            end = max(prev_xcor, curr_xcor)
            for x_position in range(start, end):
                coord = (x_position, prev_ycor)
                positions.append(coord)
        # Y coord are changing and the difference between them is greater than 1
        elif prev_ycor != curr_ycor:
            start = min(prev_ycor, curr_ycor)
            end = max(prev_ycor, curr_ycor)
            for y_position in range(start, end):
                coord = (prev_xcor, y_position)
                positions.append(coord)
        # Translate to grid coordinates
        positions = [self.get_grid_coord(x, y) for x, y in positions]
        if positions and player.name == "P1":
            for x, y in positions:
                print(f"Adding {x},{y}")
        return positions

    def create_player(self, number=2):
        """Two players are always created. P1 is blue.
        P2 is Yellow, P3 is Red, P4 is Green"""
        colors = ["#40BBE3", "#E3E329", "#ff0000", "#33cc33"]

        for i in range(number):
            x, y = self.get_random_coord()
            self.players.append(player.Player("P" + str(i + 1), x, y, colors[i]))

    def create_particles(self):
        """Populates particles list. All particles act in same manner."""
        for _ in range(20):
            self.particles.append(particle.Particle())

    def particles_explode(self, player):
        """Makes all particles explode at player crash position"""
        for particle in self.particles:
            particle.change_color(player)
            particle.explode(player.xcor(), player.ycor())

    def is_collision(self, x, y):
        return self.grid[y][x]

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
        self.game_text_pen.write(winner + " wins!", align="center", font=Game.GAME_FONT)

    def reset_grid(self):
        for player in self.players:
            x, y = self.get_random_coord()
            player.clear_lightcycle()
            player.respawn(x, y)
        self.grid = self.create_grid()

    def start_bgm(self):
        if os.name == "posix":
            os.system("killall afplay")
            os.system("afplay sounds/gameplay.m4a&")
            os.system("say grid is live!&")

    def countdown(self):
        for num in range(3, 0, -1):
            self.game_text_pen.pendown()
            self.game_text_pen.write(str(num), align="center", font=Game.GAME_FONT)
            if os.name == "posix":
                os.system(f"say {num}&")
            time.sleep(1)
            self.game_text_pen.clear()

    def get_grid_coord(self, x, y):
        x = int(x + (self.width / 2) - self.out_of_bounds_length)
        y = int(y + (self.height / 2) - self.out_of_bounds_length)
        return (x, y)

    def create_pens(self):
        """Initialize all pens."""
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

    def end_game(self):
        self.game_on = False
        self.display_winner()
        time.sleep(2)
        self.screen.clear()
        if os.name == "posix":
            os.system("killall afplay")

    def start_game(self):
        """All players are set into motion, boundary checks, and collision checks
        run continuously until a player runs out of lives."""

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
                player.set_coord()
                player.forward(player.fwd_speed)
                x, y = self.get_grid_coord(player.xcor(), player.ycor())

                # Detect collision with boundary, self, or enemy
                if self.is_outside_boundary(player) or self.is_collision(x, y):
                    player.lose_life()
                else:
                    # Add missing positions to bridge position gaps
                    positions = self.position_range_adder(player)
                    for x, y in positions:
                        self.grid[y][x] = 1

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
                self.end_game()


if __name__ == "__main__":
    gameObj = Game()
    gameObj.start_game()
