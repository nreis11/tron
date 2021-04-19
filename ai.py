import player


class Ai(player.Player):
    def __init__(self, name, start_x, start_y, color, difficulty):
        player.Player.__init__(self, name, start_x, start_y, color)
        self.difficulty = difficulty
        self.set_speed()
        self.frame = 0
        self.frame_delay = 30 // difficulty
        self.min_distance_collision = 100 // difficulty
        self.is_ai = True

    def reset_frames(self):
        self.frame = 0

    def set_speed(self):
        """Set speed based on difficulty (1-3). Defaults to easy."""
        self.fwd_speed = self.difficulty
        self.fwd_speed = 1

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()