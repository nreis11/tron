from constants import SCREENS


class Screen:
    def __init__(self, name):
        self.name = name
        self.curr_cursor_idx = SCREENS[name]["default_cursor_idx"]
        self.cursor_positions = SCREENS[name]["cursor_positions"]
        self.num_cursor_positions = len(self.cursor_positions)
        self.bg = SCREENS[name]["path"]

    def get_cursor_pos(self):
        if self.curr_cursor_idx in self.cursor_positions:
            return self.cursor_positions[self.curr_cursor_idx]

    def cursor_up(self):
        """Increase cursor idx by 1."""
        if self.curr_cursor_idx < self.num_cursor_positions:
            self.curr_cursor_idx += 1

    def cursor_down(self):
        """Decrease cursor idx by 1."""
        if self.curr_cursor_idx > 1:
            self.curr_cursor_idx -= 1
