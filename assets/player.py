import turtle
import random


class Player(turtle.Turtle):

    CRASHED = "crashed"`
    READY = "ready"

    def __init__(self, name, start_x, start_y):
        super(Player, self).__init__()
        self.name = name
        self.speed(0)
        self.fwd_speed = 1
        self.pensize(2)
        self.start_x = start_x
        self.start_y = start_y
        self.setposition(start_x, start_y)
        self.positions = []
        self.coord = (self.start_x, self.start_y)
        self.lives = 5
        self.status = self.READY

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

    def convert_coord_to_int(self):
        """Convert coordinates to integers for more accurate collision detection"""
        x, y = self.pos()
        x = int(x)
        y = int(y)
        self.coord = (x, y)

    def clear_lightcycle(self):
        """Removes light cycle from screen"""
        self.penup()
        self.clear()

    def lose_life(self):
        """Takes away one life from player"""
        self.lives -= 1
        self.status = self.CRASHED

    def respawn(self, x, y):
        """Respawns light cycle to random coord passed as args, resets speed to 1, and
        resets the position list."""
        self.status = self.READY
        self.setposition(x, y)
        self.setheading(random.randrange(0, 360, 90))
        self.fwd_speed = 1
        self.pendown()
        self.positions = []