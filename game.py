#!/usr/bin/env python3

import turtle
import os
import random
import constants
import functools

# Dev assets
from ai import Ai
from grid import Grid
from particle import Particle
from pen import Pen
from player import Player
from sound import Sound

# For windows audio
if os.name == "nt":
    import winsound


class Game(object):
    """Creates screen, draws border, creates all sprites, maps keys, draws score, and runs game loop."""

    def __init__(
        self,
        grid_size=3,
        humans=0,
        bots=2,
        testing=False,
        difficulty=1,
    ):
        self.width = 800
        self.height = 600
        self.determine_grid_size(grid_size)
        self.create_screen()
        self.audio = Sound()
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
        self.create_assets()

    def determine_grid_size(self, grid_size):
        if grid_size == 2:
            self.width, self.height = (1024, 768)
        elif grid_size == 3:
            self.width, self.height = (1280, 960)

    def create_grid(self):
        width = self.x_boundary * 2
        height = self.y_boundary * 2
        return Grid(width, height)

    def create_screen(self):
        """Maximizes screen based on monitor size."""
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(1.0, 1.0)
        self.screen.title("TURTLETRON")
        self.screen.tracer(0)

    def create_border(self):
        """Border is drawn from the width and height, starting in upper right hand corner.
        The border coordinates will be used for border detection as well."""
        self.border_pen.setposition(self.x_boundary, self.y_boundary)
        self.border_pen.pendown()
        self.border_pen.setheading(constants.WEST)
        for side in range(4):
            # Vertical
            if side % 2:
                self.border_pen.forward(self.y_boundary * 2)
                self.border_pen.forward(2)  # Extra added to match visually
                self.border_pen.left(90)
            # Horizontal
            else:
                self.border_pen.forward(self.x_boundary * 2)
                self.border_pen.forward(2)  # Extra added to match visually
                self.border_pen.left(90)
        self.border_pen.penup()

    def get_random_coord(self):
        """Generates random coordinate within playable area with buffer from boundary"""
        buffer = 100
        x = random.randint(-(self.x_boundary - buffer), (self.x_boundary - buffer))
        y = random.randint(-(self.y_boundary - buffer), (self.y_boundary - buffer))
        return (x, y)

    def position_range_adder(self, player):
        """Calculates and collects all missing positions given prev and current position. Returns grid coordinates."""
        positions = []

        def get_missing_positions(prev, curr, step):
            for pos in range(prev, curr, step):
                positions.append(pos)
            return positions

        prev_xcor, prev_ycor = player.prev_pos
        curr_xcor, curr_ycor = int(player.xcor()), int(player.ycor())
        if prev_xcor == curr_xcor and prev_ycor == curr_ycor:
            return positions

        if player.heading() == constants.EAST:
            positions = get_missing_positions(prev_xcor, curr_xcor, 1)
        elif player.heading() == constants.NORTH:
            positions = get_missing_positions(prev_ycor, curr_ycor, 1)
        elif player.heading() == constants.WEST:
            positions = get_missing_positions(prev_xcor, curr_xcor, -1)
        elif player.heading() == constants.SOUTH:
            positions = get_missing_positions(prev_ycor, curr_ycor, -1)
        # Translate to grid coordinates
        if player.heading() == constants.EAST or player.heading() == constants.WEST:
            positions = [self.grid.get_grid_coord(x, prev_ycor) for x in positions]
        elif player.heading() == constants.NORTH or player.heading() == constants.SOUTH:
            positions = [self.grid.get_grid_coord(prev_xcor, y) for y in positions]
        return positions

    def create_player(self):
        """P1 is blue, P2 is Yellow, P3 is Red, P4 is Green, P5 is Purple."""
        color_idx = len(constants.COLORS) - 1
        for i in range(self.humans):
            x, y = self.get_random_coord()
            self.players.append(
                Player("P" + str(i + 1), x, y, constants.COLORS[color_idx])
            )
            color_idx -= 1

        for i in range(self.bots):
            x, y = self.get_random_coord()
            self.players.append(
                Ai(
                    "COM" + str(i + 1),
                    x,
                    y,
                    constants.COLORS[color_idx],
                    self.difficulty,
                )
            )
            color_idx -= 1

    def create_particles(self):
        """Populates particles list. All particles act in same manner."""
        for _ in range(20):
            self.particles.append(Particle())

    def particles_explode(self, player):
        """Makes all particles explode at player crash position"""
        for particle in self.particles:
            particle.change_color(player)
            particle.explode(player.xcor(), player.ycor())

    def set_keyboard_bindings(self):
        """Maps absolute controls to player movement."""
        player_bindings = constants.KEY_BINDINGS
        for i in range(self.humans):
            self.key_mapper(self.players[i], **player_bindings[i])

    def key_mapper(self, player, EAST, NORTH, WEST, SOUTH):
        """Maps args to player controls"""

        turtle.onkeypress(
            functools.partial(player.go_dir, dir=constants.EAST),
            EAST,
        )
        turtle.onkeypress(
            functools.partial(player.go_dir, dir=constants.NORTH),
            NORTH,
        )
        turtle.onkeypress(
            functools.partial(player.go_dir, dir=constants.WEST),
            WEST,
        )
        turtle.onkeypress(
            functools.partial(player.go_dir, dir=constants.SOUTH),
            SOUTH,
        )

    def draw_score(self):
        """This draws the score on the screen once, then clears once the score changes. Start position is upper left corner.
        A dedicated score pen is needed because the clear function is called every time the score is updated."""
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
        return len([player for player in self.players if player.has_lives()]) == 1

    def display_winner(self):
        """Once game loop finishes, this runs to display the winner."""
        self.game_text_pen.pendown()
        winner = [player.name for player in self.players if player.has_lives()][0]
        self.game_text_pen.write(
            f"{winner} wins!", align="center", font=self.game_text_pen.font
        )

    def reset_grid(self):
        alive_players = [
            player for player in self.players if not player.status == player.DEAD
        ]
        for player in alive_players:
            player.clear_lightcycle()
            if player.has_lives():
                x, y = self.get_random_coord()
                player.respawn(x, y)
            else:
                player.status = player.DEAD
                if not player.is_ai:
                    self.humans -= 1

        # Speed up game if no humans are alive
        if self.humans == 0:
            for player in alive_players:
                if player.is_ai:
                    player.set_speed(6)
        self.grid = self.create_grid()

    def countdown(self, num):
        self.game_text_pen.pendown()
        self.game_text_pen.write(str(num), align="center", font=self.game_text_pen.font)
        if os.name == "posix":
            os.system(f"say {num}&")
        self.game_text_pen.clear()

    def create_pens(self):
        """Initialize all pens."""
        self.border_pen = Pen("blue", 2)
        self.score_pen = Pen()
        self.game_text_pen = Pen()

    def create_assets(self):
        self.create_pens()
        self.create_border()
        self.create_player()
        self.create_particles()
        self.draw_score()
        for num in range(3, 0, -1):
            turtle.ontimer(self.countdown(num), 1000)
        for t in turtle.turtles():
            t.setundobuffer(None)

    def end_game(self):
        """Game over cleanup."""
        self.game_on = False
        turtle.ontimer(self.display_winner(), 3000)
        self.screen.clear()
        self.audio.stop_music()

    def set_crash_sequence(self, player):
        player.lose_life()
        self.particles_explode(player)
        self.audio.play_sfx("explosion")
        self.draw_score()

    def analyze_positions(self, player, positions):
        """Check for collision. If no collision, set pos to visited."""
        for x, y in positions:
            if player.is_collision(self.grid, x, y):
                player.status = player.CRASHED
                return
            else:
                self.grid.set_pos_to_visited(x, y)
                self.grid.set_adjacent_coords_as_visited(player, x, y, 5)

    def start_game(self):
        """All players are set into motion, boundary checks, and collision checks
        run continuously until a player runs out of lives."""
        if not self.testing:
            self.audio.start_music("gameplay", True)

        # Set controls based on menu setting
        self.set_keyboard_bindings()
        while self.game_on:
            # Activate key mappings
            self.screen.listen()
            # Set players into motion and add converted coords to positions
            for player in self.players:
                if player.status == player.READY:
                    if player.is_ai:
                        player.run_ai_logic(self.grid)
                    player.set_prev_coord()
                    player.forward(player.fwd_speed)
                    positions = self.position_range_adder(player)
                    self.analyze_positions(player, positions)

            for particle in self.particles:
                particle.move()

            # If a player crashes, particles explode and reset lightcycles
            for player in self.players:
                if player.status == player.CRASHED:
                    self.set_crash_sequence(player)
                    if self.is_game_over():
                        self.end_game()
                    else:
                        self.reset_grid()
            # Updates screen only when loop is complete
            self.screen.update()


if __name__ == "__main__":
    gameObj = Game(testing=False, difficulty=2, bots=2, humans=0, grid_size=2)
    gameObj.start_game()
