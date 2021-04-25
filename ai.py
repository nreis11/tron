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

    def reset_frames(self):
        self.frame = 0

    def set_speed(self):
        """Set speed based on difficulty (1-3)."""
        self.fwd_speed = self.difficulty

    def set_custom_speed(self):
        self.fwd_speed = 6

    def set_min_distance_collision(self):
        self.min_distance_collision = 100 // self.difficulty + random.choice(
            [num for num in range(-20, 20, 10)]
        )

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()