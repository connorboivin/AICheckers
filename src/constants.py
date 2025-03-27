import pygame

# Window dimensions
WINDOW_SIZE = 600
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colors (RGB values)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CROWN = (255, 215, 0)  # Gold color for the crown

# Players and Pieces
RED_PLAYER = 1
BLACK_PLAYER = 2

# Piece colors (using the RGB values)
PIECE_COLORS = {
    RED_PLAYER: RED,
    BLACK_PLAYER: BLACK
}

# Directions (row, col)
DIRECTIONS = {
    RED_PLAYER: [(-1, -1), (-1, 1)],  # Red moves up
    BLACK_PLAYER: [(1, -1), (1, 1)]    # Black moves down
} 