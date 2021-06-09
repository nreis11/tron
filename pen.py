import turtle


class Pen(turtle.Turtle):
    def __init__(self, color="white", size=1):
        super().__init__()
        self.speed(0)
        self.penup()
        self.hideturtle()
        self.color(color)
        self.pensize(size)
        self.font = ("Phosphate", 42, "bold")
