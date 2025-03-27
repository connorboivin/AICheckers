import pygame
import numpy as np
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.create_board()

    def draw_squares(self, window):
        """Draw the checkerboard pattern."""
        window.fill(BLACK)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(window, WHITE,
                                   (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                    SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        """Initialize the game pieces on the board."""
        self.board = []
        for row in range(BOARD_SIZE):
            self.board.append([])
            for col in range(BOARD_SIZE):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED_PLAYER))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK_PLAYER))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        """Draw the complete board with squares and pieces."""
        self.draw_squares(window)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def remove(self, pieces):
        """Remove captured pieces from the board."""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == RED_PLAYER:
                self.red_left -= 1
            else:
                self.black_left -= 1

    def get_piece(self, row, col):
        """Return the piece at the given position."""
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return 0

    def move(self, piece, row, col):
        """Move a piece to a new position and handle captures."""
        # Store the original position
        original_row = piece.row
        original_col = piece.col
        
        # Move the piece
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = piece
        piece.move(row, col)

        # Check if this was a capture move
        if abs(row - original_row) == 2:
            # Remove the captured piece
            captured_row = (row + original_row) // 2
            captured_col = (col + original_col) // 2
            self.board[captured_row][captured_col] = 0
            if self.board[captured_row][captured_col] != 0:
                if self.board[captured_row][captured_col].color == RED_PLAYER:
                    self.red_left -= 1
                else:
                    self.black_left -= 1

        # Handle king promotion
        if row == 0 and piece.color == BLACK_PLAYER:
            piece.make_king()
            self.black_kings += 1
        elif row == BOARD_SIZE - 1 and piece.color == RED_PLAYER:
            piece.make_king()
            self.red_kings += 1

    def get_all_pieces(self, color):
        """Get all pieces of a given color."""
        pieces = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece_captures(self, piece):
        """Get all possible captures for a piece."""
        jumps = {}
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1

        if piece.color == RED_PLAYER or piece.king:
            # Check jumps going down for red pieces
            if row + 2 < BOARD_SIZE:
                if left - 1 >= 0 and self.board[row+1][left] != 0 and \
                   self.board[row+1][left].color != piece.color and \
                   self.board[row+2][left-1] == 0:
                    jumps[(row+2, left-1)] = [self.board[row+1][left]]
                if right + 1 < BOARD_SIZE and self.board[row+1][right] != 0 and \
                   self.board[row+1][right].color != piece.color and \
                   self.board[row+2][right+1] == 0:
                    jumps[(row+2, right+1)] = [self.board[row+1][right]]

        if piece.color == BLACK_PLAYER or piece.king:
            # Check jumps going up for black pieces
            if row - 2 >= 0:
                if left - 1 >= 0 and self.board[row-1][left] != 0 and \
                   self.board[row-1][left].color != piece.color and \
                   self.board[row-2][left-1] == 0:
                    jumps[(row-2, left-1)] = [self.board[row-1][left]]
                if right + 1 < BOARD_SIZE and self.board[row-1][right] != 0 and \
                   self.board[row-1][right].color != piece.color and \
                   self.board[row-2][right+1] == 0:
                    jumps[(row-2, right+1)] = [self.board[row-1][right]]

        return jumps

    def has_captures_available(self, color):
        """Check if any piece of the given color has available captures."""
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            if self.get_piece_captures(piece):
                return True
        return False

    def has_additional_captures(self, piece):
        """Check if a piece has additional captures available after a jump."""
        captures = self.get_piece_captures(piece)
        return len(captures) > 0

    def get_valid_moves(self, piece, must_jump=False):
        """Return all valid moves for a given piece."""
        # Get available captures for this piece
        captures = self.get_piece_captures(piece)
        
        # If this is a continuation of a multiple jump, only return captures
        if must_jump:
            return captures

        # If any piece has captures available, only return captures
        if self.has_captures_available(piece.color):
            return captures

        # If no captures are available, return regular moves
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Regular moves (non-jumps)
        if piece.color == RED_PLAYER or piece.king:
            # Check moves going down for red pieces
            if row + 1 < BOARD_SIZE:
                if left >= 0 and self.board[row+1][left] == 0:
                    moves[(row+1, left)] = []
                if right < BOARD_SIZE and self.board[row+1][right] == 0:
                    moves[(row+1, right)] = []

        if piece.color == BLACK_PLAYER or piece.king:
            # Check moves going up for black pieces
            if row - 1 >= 0:
                if left >= 0 and self.board[row-1][left] == 0:
                    moves[(row-1, left)] = []
                if right < BOARD_SIZE and self.board[row-1][right] == 0:
                    moves[(row-1, right)] = []

        return moves 