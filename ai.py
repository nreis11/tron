import player


class Ai(player.Player):
    def __init__(self, name, start_x, start_y, color, difficulty):
        super(Ai, self).__init__(name, start_x, start_y, color)
        self.difficulty = difficulty
        self.set_speed()
        self.frame = 0
        self.frame_delay = 30 // difficulty
        self.min_distance_collision = 100 // difficulty
        self.is_ai = True

    def reset_frames(self):
        self.frame = 0

    def set_speed(self):
        """Set speed based on difficulty (1-3)."""
        self.fwd_speed = self.difficulty

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()