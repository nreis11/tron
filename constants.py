COLORS = ["#CF1FDE", "#33cc33", "#ff0000", "#E3E329", "#40BBE3"]

EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270

KEY_BINDINGS = [
    {"EAST": "d", "NORTH": "w", "WEST": "a", "SOUTH": "s"},
    {"EAST": "Right", "NORTH": "Up", "WEST": "Left", "SOUTH": "Down"},
]

OPPOSING_DIRS = {EAST: WEST, WEST: EAST, NORTH: SOUTH, SOUTH: NORTH}

SCREENS = {
    "main": {
        "path": "images/main_menu.gif",
        "cursor_positions": {
            4: (-130, 92),
            3: (-130, 35),
            2: (-130, -78),
            1: (-130, -190),
        },
        "default_cursor_idx": 4,
    },
    "options": {
        "path": "images/options.gif",
        "cursor_positions": {
            4: (-510, 195),
            3: (-510, 63),
            2: (-510, -67),
            1: (-510, -200),
        },
        "default_cursor_idx": 4,
    },
    "controls": {
        "path": "images/controls.gif",
        "cursor_positions": {1: (-5000, -5000)},
        "default_cursor_idx": 1,
    },
}

DEBUG = {"testing": True, "difficulty": 3, "bots": 2, "humans": 0, "grid_size": 1}
