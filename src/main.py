import pygame
from constants import *
from game import Game

def get_row_col_from_mouse(pos):
    """Convert mouse position to board coordinates."""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    """Main game loop."""
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Checkers')
    
    game = Game(window)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        if game.winner() is not None:
            print(f"Winner: {'Red' if game.winner() == RED_PLAYER else 'Black'}")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == '__main__':
    main() 