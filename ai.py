import player
import random
import constants


class Ai(player.Player):
    def __init__(self, name, start_x, start_y, color, difficulty):
        super(Ai, self).__init__(name, start_x, start_y, color)
        self.difficulty = difficulty
        self.set_speed()
        self.frame = 0
        self.frame_delay = 30 // difficulty
        self.min_collision_distance = 100 // self.difficulty
        self.is_ai = True

    def run_ai_logic(self, grid):
        """Make decisions based on nearby collision. Frame delay equates to reflexes."""
        self.increment_frames()
        if self.frame >= self.frame_delay and self.is_near_collision(grid):
            dir = self.determine_turn(grid)
            self.go_dir(dir)
            # self.randomize_min_distance_collision()
            self.reset_frames()

    def increment_frames(self):
        self.frame += 1

    def reset_frames(self):
        self.frame = 0

    def set_speed(self, speed=0):
        """Set speed based on difficulty (1-3) or speed arg if provided."""
        self.fwd_speed = speed or self.difficulty

    def randomize_min_collision_distance(self):
        self.min_collision_distance = 100 // self.difficulty + random.choice(
            [num for num in range(-20, 20, 10)]
        )

    def determine_turn(self, grid):
        """Get flanking distances to collision. Whichever direction has the longest distance to a collision, turn that direction."""
        x, y = grid.get_grid_coord(self.xcor(), self.ycor())
        i = 1
        while True:
            if self.heading() == constants.EAST or self.heading() == constants.WEST:
                if self.is_collision(grid, x, y + i):
                    return constants.SOUTH
                elif self.is_collision(grid, x, y - i):
                    return constants.NORTH
            elif self.heading() == constants.NORTH or self.heading() == constants.SOUTH:
                if self.is_collision(grid, x - i, y):
                    return constants.EAST
                elif self.is_collision(grid, x + i, y):
                    return constants.WEST
            i += 1

    def is_near_collision(self, grid):
        """Checks for nearby collision in the direction of the player."""
        i = 1
        x, y = grid.get_grid_coord(self.xcor(), self.ycor())
        while i <= self.min_collision_distance:
            if (
                (self.heading() == constants.EAST and self.is_collision(grid, x + i, y))
                or (
                    self.heading() == constants.WEST
                    and self.is_collision(grid, x - i, y)
                )
                or (
                    self.heading() == constants.NORTH
                    and self.is_collision(grid, x, y + i)
                )
                or (
                    self.heading() == constants.SOUTH
                    and self.is_collision(grid, x, y - i)
                )
            ):
                return True
            i += 1
        return False

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()