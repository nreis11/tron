class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = self.create_grid()

    def create_grid(self):
        return [[0 for x in range(self.width)] for y in range(self.height)]

    def get_grid_coord(self, x, y):
        x = int(x + self.width / 2)
        y = int(y + self.height / 2)
        return (x, y)

    def is_collision(self, x, y):
        """Checks for any visited coordinate and if the coordinate is out of bounds."""
        if x < 0 or y < 0:
            return True
        try:
            return self.matrix[y][x]
        except IndexError:
            # Out of Bounds
            return True

    def is_near_collision(self, ai):
        """Checks for nearby collision in the direction of the player."""
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

    def set_adjacent_coords_as_visited(self, player, x, y, amount=1):
        """Sets adjecent coordinates in all directions to visited by certain amount."""
        try:
            for num in range(1, amount + 1):
                if player.heading() == 0 or player.heading() == 180:
                    self.matrix[y - num][x] = 1
                    self.matrix[y + num][x] = 1
                elif player.heading() == 90 or player.heading() == 270:
                    self.matrix[y][x + num] = 1
                    self.matrix[y][x - num] = 1
        except IndexError:
            # Ignore out of bounds activations
            pass
