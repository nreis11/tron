import turtle
import random


class Player(turtle.Turtle):

    CRASHED = "crashed"
    READY = "ready"

    def __init__(self, name, start_x, start_y, color):
        super(Player, self).__init__()
        self.penup()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=0.3, stretch_len=1, outline=None)
        self.name = name
        self.speed(0)
        self.fwd_speed = 1
        self.pensize(2)
        self.setposition(start_x, start_y)
        self.prev_pos = (start_x, start_y)
        self.curr_pos = (start_x, start_y)
        self.lives = 2
        self.status = Player.READY
        self.pendown()

    def turn_left(self):
        """90 Degree left turn."""
        self.left(90)

    def turn_right(self):
        """90 Degree right turn."""
        self.right(90)

    def accelerate(self):
        """Min. speed = 1, Max. speed = 3."""
        if self.fwd_speed < 3:
            self.fwd_speed += 1
            self.forward(self.fwd_speed)  # Needs to be run only if speed changes

    def decelerate(self):
        """Min. speed = 1, therefore player can never stop"""
        if self.fwd_speed > 1:
            self.fwd_speed -= 1
            self.forward(self.fwd_speed)  # Needs to be run only if speed changes

    def set_coord(self, x, y):
        """Sets grid coordinates. Keeps track of prev and current."""
        self.prev_pos = self.curr_pos
        self.curr_pos = (x, y)

    def clear_lightcycle(self):
        """Removes light cycle from screen"""
        self.penup()
        self.clear()

    def lose_life(self):
        """Takes away one life from player"""
        self.lives -= 1
        self.status = Player.CRASHED

    def respawn(self, x, y):
        """Respawns light cycle to random coord passed as args, resets speed to 1, and
        resets the position list."""
        self.status = Player.READY
        self.setposition(x, y)
        self.setheading(random.randrange(0, 360, 90))
        self.prev_pos = (x, y)
        self.curr_pos = (x, y)
        self.fwd_speed = 1
        self.pendown()