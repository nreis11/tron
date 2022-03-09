import turtle
import random
import constants


class Player(turtle.Turtle):

    CRASHED = "crashed"
    READY = "ready"
    DEAD = "dead"

    def __init__(self, name, start_x, start_y, color):
        super(Player, self).__init__()
        self.penup()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=0.2, stretch_len=0.8, outline=None)
        self.name = name
        self.speed(0)
        self.fwd_speed = 1
        self.pensize(3)
        self.setheading(random.randrange(0, 360, 90))
        self.setposition(start_x, start_y)
        self.prev_pos = (start_x, start_y)
        self.lives = 3
        self.status = self.READY
        self.is_ai = False
        self.pendown()

    def turn_left(self):
        self.left(90)

    def turn_right(self):
        self.right(90)

    def go_dir(self, dir):
        """Determine movement based on current heading."""
        opposite_dir = constants.OPPOSING_DIRS[dir]
        if self.heading() == dir:
            self.accelerate()
        elif self.heading() == opposite_dir:
            self.decelerate()
        else:
            self.setheading(dir)

    def accelerate(self):
        """Min. speed = 1, Max. speed = 3."""
        if self.fwd_speed < 3:
            self.fwd_speed += 1
            self.forward(self.fwd_speed)

    def decelerate(self):
        """Min. speed = 1, therefore player can never stop"""
        if self.fwd_speed > 1:
            self.fwd_speed -= 1
            self.forward(self.fwd_speed)

    def set_prev_coord(self):
        """Sets prev coordinates."""
        prev_x = int(self.xcor())
        prev_y = int(self.ycor())
        self.prev_pos = (prev_x, prev_y)

    def is_collision(self, grid, x, y):
        """Checks for any visited coordinate and if the coordinate is out of bounds."""
        if x < 0 or y < 0:
            return True
        try:
            return grid.matrix[y][x]
        except IndexError:
            # Out of Bounds
            return True

    def clear_lightcycle(self):
        """Removes light cycle from screen"""
        self.hideturtle()
        self.penup()
        self.clear()

    def lose_life(self):
        """Take away one life from player"""
        self.lives -= 1

    def has_lives(self):
        return self.lives > 0

    def respawn(self, x, y):
        """Respawns light cycle to random coord passed as args, resets speed to 1, and
        resets the position list."""
        self.status = self.READY
        self.setposition(x, y)
        self.setheading(random.randrange(0, 360, 90))
        self.set_prev_coord()
        self.fwd_speed = 1
        self.showturtle()
        self.pendown()
