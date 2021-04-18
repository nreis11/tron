import player


class Ai(player.Player):
    def __init__(self, name, start_x, start_y, color, difficulty):
        super(Ai, self).__init__(name, start_x, start_y, color)
        self.difficulty = difficulty
        self.set_speed()
        self.frame = 0
        self.frame_delay = 30 // difficulty
        self.min_distance_collision = 100 // difficulty
        self.test_frame = 0
        self.test_draw_length = 10
        self.is_ai = True

    def reset_frames(self):
        self.frame = 0

    def set_speed(self):
        """Set speed based on difficulty (1-3). Defaults to easy."""
        self.fwd_speed = self.difficulty

    def respawn(self, x, y):
        super(Ai, self).respawn(x, y)
        self.set_speed()

    def run_test(self):
        self.test_frame += 1
        if self.test_draw_length == self.test_frame:
            self.turn_right()
            self.test_frame = 0
            self.test_draw_length += 3
