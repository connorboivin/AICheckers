import pygame
from constants import *

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color  # This is now RED_PLAYER or BLACK_PLAYER
        self.king = False
        
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """Calculate the x and y coordinates based on the row and column."""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """Promote piece to king."""
        self.king = True

    def draw(self, window):
        """Draw the piece on the window."""
        radius = SQUARE_SIZE // 2 - self.PADDING
        # Draw piece outline
        pygame.draw.circle(window, GRAY, (self.x, self.y), radius + self.OUTLINE)
        # Draw piece fill using the color mapping
        pygame.draw.circle(window, PIECE_COLORS[self.color], (self.x, self.y), radius)
        
        if self.king:
            # Draw crown
            crown_radius = radius // 2
            pygame.draw.circle(window, CROWN, (self.x, self.y), crown_radius)

    def move(self, row, col):
        """Move piece to a new position."""
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self):
        """String representation of the piece."""
        return f"Piece({self.row}, {self.col}, {self.color})" 