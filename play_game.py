import pygame
import sys
import argparse
from src.game import Game
from src.constants import *
from src.ai.agent import CheckersAI

def main():
    parser = argparse.ArgumentParser(description='Play checkers against AI')
    parser.add_argument('--model', type=str, required=True, help='Path to the AI model file')
    parser.add_argument('--player_color', type=str, default='black', choices=['red', 'black'],
                      help='Choose your color (red or black)')
    args = parser.parse_args()

    # Initialize Pygame
    pygame.init()
    
    # Create the game window
    WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Checkers vs AI')
    
    # Initialize game
    game = Game(WIN)
    
    # Initialize AI
    ai = CheckersAI()
    ai.load_model(args.model)
    
    # Set player and AI colors
    player_color = RED_PLAYER if args.player_color.lower() == 'red' else BLACK_PLAYER
    ai_color = BLACK_PLAYER if player_color == RED_PLAYER else RED_PLAYER
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        
        # If it's AI's turn
        if game.turn == ai_color:
            # Get board state and valid moves
            board_state = game.board.get_state()
            valid_moves = game.board.get_valid_moves_mask()
            
            # Get AI's move
            pieces = game.board.get_all_pieces(ai_color)
            for piece in pieces:
                moves = game.board.get_valid_moves(piece)
                if moves:
                    # AI selects this piece
                    game.select(piece.row, piece.col)
                    # Get AI's chosen move
                    move_positions = list(moves.keys())
                    if move_positions:
                        row, col = move_positions[0]  # Take first valid move
                        game.select(row, col)
                        break
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle player moves
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == player_color:
                pos = pygame.mouse.get_pos()
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                game.select(row, col)
        
        # Update display
        game.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 