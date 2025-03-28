import pygame
from src.constants import *
from src.board import Board

class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.turn = RED_PLAYER
        self.selected = None
        self.valid_moves = {}
        self.jumping_piece = None  # Track piece that's in the middle of multiple jumps

    def update(self):
        """Update the game display."""
        self.board.draw(self.window)
        self.draw_valid_moves()
        pygame.display.update()

    def select(self, row, col):
        """Handle piece selection and moves."""
        print(f"Clicked position: row={row}, col={col}")
        piece = self.board.get_piece(row, col)
        print(f"Piece at position: {piece}")
        print(f"Current turn: {'Red' if self.turn == RED_PLAYER else 'Black'}")
        
        # If a piece is already selected
        if self.selected:
            print(f"Already selected piece: {self.selected}")
            print(f"Valid moves: {self.valid_moves}")
            # Try to make a move
            result = self._move(row, col)
            if result:
                print(f"Moving piece {self.selected} to ({row}, {col})")
                print(f"Turn changed to: {'Black' if self.turn == BLACK_PLAYER else 'Red'}")
            print(f"Move result: {result}")
            if not result:
                # If move failed, clear selection and try selecting new piece
                self.selected = None
                return self.select(row, col)
            return True
        
        # If no piece is selected, try to select one
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            print(f"Selected piece: {piece}")
            print(f"Valid moves: {self.valid_moves}")
            return True
            
        return False

    def _move(self, row, col):
        """Execute a move if it's valid."""
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
            return True
        return False

    def change_turn(self):
        """Switch turns between players."""
        self.valid_moves = {}
        self.selected = None
        self.jumping_piece = None  # Reset jumping piece when turn changes
        self.turn = BLACK_PLAYER if self.turn == RED_PLAYER else RED_PLAYER
        print(f"\nTurn changed to: {'Red' if self.turn == RED_PLAYER else 'Black'}")

    def draw_valid_moves(self):
        """Highlight valid moves on the board."""
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE,
                             (col * SQUARE_SIZE + SQUARE_SIZE//2,
                              row * SQUARE_SIZE + SQUARE_SIZE//2),
                             15)

    def winner(self):
        """Check if there's a winner."""
        if self.board.red_left <= 0:
            return BLACK_PLAYER
        elif self.board.black_left <= 0:
            return RED_PLAYER
        return None

    def get_board(self):
        """Return the game board."""
        return self.board

    def ai_move(self, board):
        """Placeholder for AI move implementation."""
        pass

    def make_move_from_action(self, action):
        """Make a move based on the AI's action."""
        if action is None:
            return False
            
        start_pos, end_pos = action
        
        # First select the piece
        if not self.selected:
            row, col = start_pos
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
        
        # Then make the move
        if self.selected:
            row, col = end_pos
            if (row, col) in self.valid_moves:
                self.board.move(self.selected, row, col)
                self.change_turn()
                return True
            
        return False 