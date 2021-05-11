import player
import random


class Ai(player.Player):
    def __init__(self, name, start_x, start_y, color, difficulty):
        super(Ai, self).__init__(name, start_x, start_y, color)
        self.difficulty = difficulty
        self.set_speed()
        self.frame = 0
        self.frame_delay = 30 // difficulty
        self.min_distance_collision = 100 // self.difficulty
        self.is_ai = True

    def run_ai_logic(self, grid):
        """Make decisions based on nearby collision. Frame delay equates to reflexes."""
        self.increment_frames()
        if self.frame >= self.frame_delay and self.is_near_collision(grid):
            self.make_smart_turn(grid)
            # self.randomize_min_distance_collision()
            self.reset_frames()

    def increment_frames(self):
        self.frame += 1

    def reset_frames(self):
        self.frame = 0

    def set_speed(self, speed=0):
        """Set speed based on difficulty (1-3) or speed arg if provided."""
        self.fwd_speed = speed or self.difficulty

    def randomize_min_distance_collision(self):
        self.min_distance_collision = 100 // self.difficulty + random.choice(
            [num for num in range(-20, 20, 10)]
        )

    def make_smart_turn(self, grid):
        """Get flanking distances to collision. Whichever direction has the longest distance to a collision, turn that direction."""
        x, y = grid.get_grid_coord(self.xcor(), self.ycor())
        i = 1
        while True:
            if self.heading() == 0 or self.heading() == 180:
                if self.is_collision(grid, x, y + i):
                    self.go_south()
                    return
                elif self.is_collision(grid, x, y - i):
                    self.go_north()
                    return
            elif self.heading() == 90 or self.heading() == 270:
                if self.is_collision(grid, x - i, y):
                    self.go_east()
                    return
                elif self.is_collision(grid, x + i, y):
                    self.go_west()
                    return
            i += 1

    def is_near_collision(self, grid):
        """Checks for nearby collision in the direction of the player."""
        i = 1
        x, y = grid.get_grid_coord(self.xcor(), self.ycor())
        while i <= self.min_distance_collision:
            if (
                (self.heading() == 0 and self.is_collision(grid, x + i, y))
                or (self.heading() == 180 and self.is_collision(grid, x - i, y))
                or (self.heading() == 90 and self.is_collision(grid, x, y + i))
                or (self.heading() == 270 and self.is_collision(grid, x, y - i))
            ):
                return True
            i += 1
        return False

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()