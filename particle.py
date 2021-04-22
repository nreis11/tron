import turtle
import random


class Particle(turtle.Turtle):
    """This class is used to create particle effects when there is a crash."""

    def __init__(self):
        super().__init__(shape="square")
        self.shapesize(stretch_wid=0.1, stretch_len=0.3, outline=None)
        self.speed(0)  # Refers to animation speed
        self.penup()
        self.fwd_speed = 10
        self.hideturtle()
        self.frame = 0

    def explode(self, start_x, start_y):
        self.frame = 1
        self.showturtle()
        self.setposition(start_x, start_y)
        self.setheading(random.randint(0, 360))

    def move(self):
        if self.frame > 0:
            self.forward(self.fwd_speed)
            self.frame += 1
        if self.frame > 10:
            self.frame = 0
            self.hideturtle()
            self.setposition(0, 0)

    def change_color(self, player):
        pencolor, fillcolor = player.color()
        self.color(pencolor)
