#!/usr/bin/env python3

import turtle
import time
import os
import random

# User created
import particle
import player
import ai


class Game(object):
    """Creates screen, draws border, creates all sprites, maps keys, draws score, and
    runs game loop."""

    GAME_FONT = ("Verdana", 36, "bold")

    def __init__(
        self,
        grid_size=3,
        relative_controls=False,
        humans=2,
        bots=0,
        testing=False,
        difficulty=1,
    ):
        turtle.setundobuffer(1)
        # self.width = 1200
        # self.height = 800
        self.determine_window_size(grid_size)
        self.relative_controls = relative_controls
        self.out_of_bounds_length = 50
        self.x_boundary = (self.width // 2) - self.out_of_bounds_length
        self.y_boundary = (self.height // 2) - self.out_of_bounds_length
        self.grid = self.create_grid()
        self.humans = humans
        self.bots = bots
        self.difficulty = difficulty
        self.players = []
        self.particles = []
        self.game_on = True
        self.testing = testing
        self.screen = turtle.Screen()
        self.create_assets()

    def determine_window_size(self, grid_size):
        if grid_size == 1:
            self.width, self.height = (800, 600)
        elif grid_size == 2:
            self.width, self.height = (1024, 768)
        elif grid_size == 3:
            self.width, self.height = (1280, 960)

    def create_grid(self):
        width = self.width - (self.out_of_bounds_length * 2)
        height = self.height - (self.out_of_bounds_length * 2)
        return [[0 for x in range(width)] for y in range(height)]

    def create_screen(self):
        """If run directly, creates screen based on user choice from self.screen_size().
        Otherwise, screen is automatically created with arguments from main.py script."""
        self.screen.bgcolor("black")
        self.screen.setup(self.width, self.height)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_border(self):
        """Border is drawn from the width and height, starting in upper
        right hand corner. Each side is 50 pixels from the edge of the screen.
        The border coordinates will be used for border detection as well."""
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
        """Generates random coordinate within playable area with 100 px padding from boundary"""
        x = random.randint(-(self.x_boundary - 100), (self.x_boundary - 100))
        y = random.randint(-(self.y_boundary - 100), (self.y_boundary - 100))
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
        prev_xcor, prev_ycor = player.prev_pos
        curr_xcor = int(player.xcor())
        curr_ycor = int(player.ycor())
        positions = []
        if prev_xcor != curr_xcor:
            start = min(prev_xcor, curr_xcor)
            end = max(prev_xcor, curr_xcor)
            for x_position in range(start + 1, end):
                coord = (x_position, prev_ycor)
                positions.append(coord)
        elif prev_ycor != curr_ycor:
            start = min(prev_ycor, curr_ycor)
            end = max(prev_ycor, curr_ycor)
            for y_position in range(start + 1, end):
                coord = (prev_xcor, y_position)
                positions.append(coord)
        # Translate to grid coordinates
        positions = [self.get_grid_coord(x, y) for x, y in positions]
        for x, y in positions:
            if self.is_collision(x, y):
                player.lose_life()
                return
            else:
                self.grid[y][x] = 1

    def create_player(self):
        """Two players are always created. P1 is blue.
        P2 is Yellow, P3 is Red, P4 is Green"""
        colors = ["#33cc33", "#ff0000", "#E3E329", "#40BBE3"]

        for i in range(self.humans):
            x, y = self.get_random_coord()
            self.players.append(player.Player("P" + str(i + 1), x, y, colors.pop()))

        for i in range(self.bots):
            x, y = self.get_random_coord()
            self.players.append(
                ai.Ai("COM" + str(i + 1), x, y, colors.pop(), self.difficulty)
            )

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
        if self.humans >= 2:
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
        x_offset = 75
        for player in self.players:
            self.score_pen.setposition(
                (self.width / -2) + x_offset, (self.height / 2) - 40
            )
            self.score_pen.pendown()
            lives = f"{player.name}: {player.lives * '*'}"
            color = player.color()[0]
            self.score_pen.color(color)
            self.score_pen.write(lives, font=("Verdana", 18, "bold"))
            self.score_pen.penup()
            x_offset += 125

    def is_game_over(self):
        """Checks to see if there's only one player left."""
        return len(list(filter(lambda player: player.lives > 0, self.players))) == 1

    def display_winner(self):
        """Once game loop finishes, this runs to display the winner."""
        self.game_text_pen.pendown()
        winner = [player.name for player in self.players if player.has_lives()][0]
        self.game_text_pen.write(f"{winner} wins!", align="center", font=Game.GAME_FONT)

    def reset_grid(self):
        for player in self.players:
            player.clear_lightcycle()
            if player.has_lives():
                x, y = self.get_random_coord()
                player.respawn(x, y)

        self.players = [player for player in self.players if player.has_lives()]
        self.grid = self.create_grid()

    def start_bgm(self):
        if os.name == "posix":
            os.system("killall afplay")
            os.system("afplay sounds/gameplay.m4a&")
            os.system("say grid is live!&")

    def countdown(self, num):
        self.game_text_pen.pendown()
        self.game_text_pen.write(str(num), align="center", font=Game.GAME_FONT)
        if os.name == "posix":
            os.system(f"say {num}&")
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

    def create_assets(self):
        self.create_screen()
        self.create_pens()
        self.create_border()
        self.create_player()
        self.create_particles()
        self.draw_score()
        for num in range(3, 0, -1):
            turtle.ontimer(self.countdown(num), 1000)
        self.start_bgm()

    def end_game(self):
        self.game_on = False
        turtle.ontimer(self.display_winner(), 2000)
        self.screen.clear()
        if os.name == "posix":
            os.system("killall afplay")

    def is_near_boundary(self, ai):
        if ai.heading() == 0 or ai.heading() == 180:
            return (
                abs(ai.xcor())
                > abs(self.x_boundary)
                - ai.min_distance_collision
                - self.border_pen.pensize()
            )
        elif ai.heading() == 90 or ai.heading() == 270:
            return (
                abs(ai.ycor())
                > abs(self.y_boundary)
                - ai.min_distance_collision
                - self.border_pen.pensize()
            )

    def make_turn_based_on_collision_distance(self, ai):
        """Get flanking distances to collision."""
        x, y = self.get_grid_coord(ai.xcor(), ai.ycor())
        x_boundary = self.width - (self.out_of_bounds_length * 2)
        y_boundary = self.height - (self.out_of_bounds_length * 2)
        i = 1
        if ai.heading() == 0 or ai.heading() == 180:
            while y + i < y_boundary and y - i > 0:
                if self.is_collision(x, y + i):
                    ai.go_south()
                    return
                if self.is_collision(x, y - i):
                    ai.go_north()
                    return
                i += 1
        elif ai.heading() == 90 or ai.heading() == 270:
            while x + i < x_boundary and x - i > 0:
                if self.is_collision(x - i, y):
                    ai.go_east()
                    return
                if self.is_collision(x + i, y):
                    ai.go_west()
                    return
                i += 1
        ai.turn_left()

    def is_near_collision(self, ai):
        i = 1
        x, y = self.get_grid_coord(ai.xcor(), ai.ycor())
        while i <= ai.min_distance_collision:
            if (
                (ai.heading() == 0 and self.is_collision(x + i, y))
                or (ai.heading() == 180 and self.is_collision(x - i, y))
                or (ai.heading() == 90 and self.is_collision(x, y + i))
                or (ai.heading() == 270 and self.is_collision(x, y - i))
            ):
                return True
            i += 1
        return False

    def ai_logic(self, ai):
        ai.frame += 1
        if ai.frame >= ai.frame_delay and (
            self.is_near_boundary(ai) or self.is_near_collision(ai)
        ):
            self.make_turn_based_on_collision_distance(ai)
            ai.reset_frames()

    def set_neighbor_coords_as_visited(self, x, y, amount=1):
        """Sets neighboring coordinates in all directions to visited by certain amount."""
        for num in range(1, amount + 1):
            self.grid[y][x + num] = 1
            self.grid[y + num][x + num] = 1
            self.grid[y + num][x] = 1
            self.grid[y + num][x - num] = 1
            self.grid[y][x - num] = 1
            self.grid[y - num][x - num] = 1
            self.grid[y - num][x] = 1
            self.grid[y - num][x + num] = 1

    def start_game(self):
        """All players are set into motion, boundary checks, and collision checks
        run continuously until a player runs out of lives."""

        while self.game_on:
            # Set controls based on menu setting
            if self.relative_controls:
                self.set_relative_keyboard_bindings()
            else:
                self.set_abs_keyboard_bindings()

            # Activate key mappings
            self.screen.listen()
            # Set players into motion and add converted coords to positions
            for player in self.players:
                if player.is_ai:
                    self.ai_logic(player)
                player.set_prev_coord()
                player.forward(player.fwd_speed)
                x, y = self.get_grid_coord(player.xcor(), player.ycor())

                # Detect collision with boundary, self, or enemy
                if self.is_outside_boundary(player) or self.is_collision(x, y):
                    player.lose_life()
                else:
                    # Add missing positions to bridge position gaps
                    self.position_range_adder(player)
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
                    self.draw_score()
                    if self.is_game_over():
                        self.end_game()
                    self.reset_grid()
            # Updates screen only when loop is complete
            self.screen.update()


if __name__ == "__main__":
    gameObj = Game(testing=False, bots=2, humans=0)
    gameObj.start_game()
