#!/usr/bin/env python3

import turtle
import time
import os
import random

# User created
import particle
import player
import ai
import grid

# For windows audio
if os.name == "nt":
    import winsound


class Game(object):
    """Creates screen, draws border, creates all sprites, maps keys, draws score, and
    runs game loop."""

    GAME_FONT = ("Phosphate", 42, "bold")

    def __init__(
        self,
        grid_size=3,
        relative_controls=False,
        humans=0,
        bots=2,
        testing=False,
        difficulty=1,
    ):
        turtle.setundobuffer(None)
        self.grid_size = grid_size
        self.width = 800
        self.height = 600
        self.determine_grid_size()
        self.create_screen()
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
        self.create_assets()

    def determine_grid_size(self):
        if self.grid_size == 2:
            self.width, self.height = (1024, 768)
        elif self.grid_size == 3:
            self.width, self.height = (1280, 960)

    def create_grid(self):
        width = self.x_boundary * 2
        height = self.y_boundary * 2
        return grid.Grid(width, height)

    def create_screen(self):
        """Maximizes screen based on monitor size."""
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(1.0, 1.0)
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
        self.border_pen.hideturtle()

    def get_random_coord(self):
        """Generates random coordinate within playable area with 100 px padding from boundary"""
        x = random.randint(-(self.x_boundary - 100), (self.x_boundary - 100))
        y = random.randint(-(self.y_boundary - 100), (self.y_boundary - 100))
        return (x, y)

    def position_range_adder(self, player):
        """Calculates and collects all missing positions given prev and current position."""
        positions = []

        def get_missing_positions(prev, curr, step):
            for pos in range(prev, curr, step):
                positions.append(pos)
            return positions

        prev_xcor, prev_ycor = player.prev_pos
        curr_xcor, curr_ycor = int(player.xcor()), int(player.ycor())
        if prev_xcor == curr_xcor and prev_ycor == curr_ycor:
            return positions

        if player.heading() == 0:
            positions = get_missing_positions(prev_xcor, curr_xcor, 1)
        elif player.heading() == 90:
            positions = get_missing_positions(prev_ycor, curr_ycor, 1)
        elif player.heading() == 180:
            positions = get_missing_positions(prev_xcor, curr_xcor, -1)
        elif player.heading() == 270:
            positions = get_missing_positions(prev_ycor, curr_ycor, -1)
        # Translate to grid coordinates
        if player.heading() == 0 or player.heading() == 180:
            positions = [self.grid.get_grid_coord(x, prev_ycor) for x in positions]
        elif player.heading() == 90 or player.heading() == 270:
            positions = [self.grid.get_grid_coord(prev_xcor, y) for y in positions]
        return positions

    def create_player(self):
        """P1 is blue, P2 is Yellow, P3 is Red, P4 is Green, P5 is Purple."""
        colors = ["#CF1FDE", "#33cc33", "#ff0000", "#E3E329", "#40BBE3"]

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

    def set_relative_keyboard_bindings(self):
        """Maps relative controls to player movement."""
        # Set P1 keyboard bindings
        if self.humans >= 1:
            turtle.onkeypress(self.players[0].turn_left, "a")
            turtle.onkeypress(self.players[0].turn_right, "d")
            turtle.onkeypress(self.players[0].accelerate, "w")
            turtle.onkeypress(self.players[0].decelerate, "s")

        # Set P2 keyboard bindings
        if self.humans >= 2:
            turtle.onkeypress(self.players[1].turn_left, "Left")
            turtle.onkeypress(self.players[1].turn_right, "Right")
            turtle.onkeypress(self.players[1].accelerate, "Up")
            turtle.onkeypress(self.players[1].decelerate, "Down")

    def set_abs_keyboard_bindings(self):
        """Maps absolute controls to player movement."""

        # Set P1 keyboard bindings
        if self.humans >= 1:
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
        """Maps args to player controls"""
        turtle.onkeypress(player.turn_left, left)
        turtle.onkeypress(player.turn_right, right)
        turtle.onkeypress(player.accelerate, accel)
        turtle.onkeypress(player.decelerate, decel)

    def draw_score(self):
        """This draws the score on the screen once, then clears once
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

    def start_bgm(self):
        bgm = "sounds/gameplay.wav"
        if os.name == "posix":
            os.system("killall afplay")
            os.system(f"afplay {bgm}&")
            os.system("say grid is live!&")
        elif os.name == "nt":
            winsound.PlaySound(bgm, winsound.SND_ASYNC)

    def countdown(self, num):
        self.game_text_pen.pendown()
        self.game_text_pen.write(str(num), align="center", font=Game.GAME_FONT)
        if os.name == "posix":
            os.system(f"say {num}&")
        self.game_text_pen.clear()

    def create_pens(self):
        """Initialize all pens."""
        self.border_pen = turtle.Turtle()
        self.score_pen = turtle.Turtle()
        self.game_text_pen = turtle.Turtle()

        self.border_pen.speed(0)
        self.border_pen.pensize(2)
        self.border_pen.color("blue")
        self.game_text_pen.hideturtle()
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.color("white")
        self.game_text_pen.color("white")

    def create_assets(self):
        self.create_pens()
        self.create_border()
        self.create_player()
        self.create_particles()
        self.draw_score()
        for num in range(3, 0, -1):
            turtle.ontimer(self.countdown(num), 1000)
        self.start_bgm()

    def end_game(self):
        """Game over cleanup."""
        self.game_on = False
        turtle.ontimer(self.display_winner(), 3000)
        self.screen.clear()
        self.stop_music()

    def stop_music(self):
        if os.name == "posix":
            os.system("killall afplay")
        elif os.name == "nt":
            winsound.PlaySound(None, winsound.SND_PURGE)

    def play_sfx(self, sound):
        if os.name == "posix":
            os.system(f"afplay {sound}&")
        elif os.name == "nt":
            # winsound.PlaySound(sound, winsound.SND_ASYNC)
            # can't play simoutaneous sounds
            pass

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

        while self.game_on:
            # Set controls based on menu setting
            self.set_relative_keyboard_bindings() if self.relative_controls else self.set_abs_keyboard_bindings()
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
                    player.lose_life()
                    self.particles_explode(player)
                    self.play_sfx("sounds/explosion.wav")
                    self.draw_score()
                    if self.is_game_over():
                        self.end_game()
                    self.reset_grid()
            # Updates screen only when loop is complete
            self.screen.update()


if __name__ == "__main__":
    gameObj = Game(testing=False, difficulty=3, bots=4, humans=0, grid_size=3)
    gameObj.start_game()
