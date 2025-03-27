import pygame
from constants import *
from board import Board

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        """Initialize game state."""
        self.selected = None
        self.board = Board()
        self.turn = RED_PLAYER
        self.valid_moves = {}
        self.jumping_piece = None  # Track piece that's in the middle of multiple jumps

    def reset(self):
        """Reset the game to initial state."""
        self._init()

    def select(self, row, col):
        """Handle piece selection and move validation."""
        print(f"\nClicked position: row={row}, col={col}")
        piece = self.board.get_piece(row, col)
        print(f"Piece at position: {piece}")
        print(f"Current turn: {'Red' if self.turn == RED_PLAYER else 'Black'}")
        
        # If we have a piece that must continue jumping, only allow selecting that piece
        if self.jumping_piece:
            # If clicking on a valid move position, allow the move
            if (row, col) in self.valid_moves:
                return self._move(row, col)
            # If clicking on the jumping piece itself, do nothing but keep it selected
            elif piece == self.jumping_piece:
                return True
            # If clicking anywhere else, ignore
            return False
            
        if self.selected:
            print(f"Already selected piece: {self.selected}")
            print(f"Valid moves: {self.valid_moves}")
            # Try to move the selected piece
            result = self._move(row, col)
            print(f"Move result: {result}")
            
            if not result:
                self.selected = None
                # Try selecting a new piece
                if piece != 0 and piece.color == self.turn:
                    print(f"Selected new piece: {piece}")
                    self.selected = piece
                    self.valid_moves = self.board.get_valid_moves(piece)
                    print(f"New valid moves: {self.valid_moves}")
                return True
        else:
            if piece != 0 and piece.color == self.turn:
                print(f"Selected piece: {piece}")
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                print(f"Valid moves: {self.valid_moves}")
                return True
        
        return False

    def _move(self, row, col):
        """Move a piece if the move is valid."""
        if self.selected and (row, col) in self.valid_moves:
            print(f"Moving piece {self.selected} to ({row}, {col})")
            # Store if this was a capture move
            was_capture = abs(row - self.selected.row) == 2
            
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves.get((row, col), [])
            if skipped:
                print(f"Captured pieces: {skipped}")
                self.board.remove(skipped)
            
            # Check for additional captures
            if was_capture:
                additional_captures = self.board.get_valid_moves(self.selected, must_jump=True)
                if additional_captures:
                    self.jumping_piece = self.selected
                    self.valid_moves = additional_captures
                    self.selected = self.jumping_piece  # Keep the piece selected
                    return True
            
            self._change_turn()
            return True
        return False

    def _change_turn(self):
        """Switch turns between players."""
        self.valid_moves = {}
        self.selected = None
        self.jumping_piece = None  # Reset jumping piece when turn changes
        self.turn = BLACK_PLAYER if self.turn == RED_PLAYER else RED_PLAYER
        print(f"\nTurn changed to: {'Red' if self.turn == RED_PLAYER else 'Black'}")

    def draw_valid_moves(self, window):
        """Highlight valid moves on the board."""
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(window, BLUE,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                              row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

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

    def update(self):
        """Update the game display."""
        self.board.draw(self.window)
        self.draw_valid_moves(self.window)
        pygame.display.update()

    def ai_move(self, board):
        """Placeholder for AI move implementation."""
        pass 