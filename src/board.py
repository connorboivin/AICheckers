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
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = piece
        piece.move(row, col)

        if row == 0 and piece.color == BLACK_PLAYER:
            piece.make_king()
            self.black_kings += 1
        elif row == BOARD_SIZE - 1 and piece.color == RED_PLAYER:
            piece.make_king()
            self.red_kings += 1

    def get_valid_moves(self, piece):
        """Return all valid moves for a given piece."""
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

        # Jump moves
        jumps = {}
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

        # If there are any jumps available, they are mandatory
        if jumps:
            return jumps
        return moves 