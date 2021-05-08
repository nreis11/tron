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
