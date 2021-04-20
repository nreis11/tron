import turtle
import random


class Player(turtle.Turtle):

    CRASHED = "crashed"
    READY = "ready"
    DIED = "died"

    def __init__(self, name, start_x, start_y, color):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=0.2, stretch_len=0.8, outline=None)
        self.name = name
        self.speed(0)
        self.fwd_speed = 1
        self.pensize(2)
        self.setheading(random.randrange(0, 360, 90))
        self.setposition(start_x, start_y)
        self.prev_pos = (start_x, start_y)
        self.lives = 3
        self.status = self.READY
        self.is_ai = False
        self.pendown()

    def turn_left(self):
        """90 Degree left turn."""
        self.left(90)

    def turn_right(self):
        """90 Degree right turn."""
        self.right(90)

    def go_east(self):
        if self.heading != 180:
            self.setheading(0)

    def go_north(self):
        if self.heading != 270:
            self.setheading(90)

    def go_west(self):
        if self.heading != 0:
            self.setheading(180)

    def go_south(self):
        if self.heading != 90:
            self.setheading(270)

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

    def set_prev_coord(self):
        """Sets prev coordinates."""
        prev_x = int(self.xcor())
        prev_y = int(self.ycor())
        self.prev_pos = (prev_x, prev_y)

    def clear_lightcycle(self):
        """Removes light cycle from screen"""
        self.hideturtle()
        self.penup()
        self.clear()

    def lose_life(self):
        """Take away one life from player"""
        self.lives -= 1
        self.status = self.CRASHED

    def has_lives(self):
        return self.lives > 0

    def respawn(self, x, y):
        """Respawns light cycle to random coord passed as args, resets speed to 1, and
        resets the position list."""
        self.status = self.READY
        self.setposition(x, y)
        self.setheading(random.randrange(0, 360, 90))
        self.prev_pos = (x, y)
        self.fwd_speed = 1
        self.showturtle()
        self.pendown()
