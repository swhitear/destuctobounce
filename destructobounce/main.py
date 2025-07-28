import pygame
from .config import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Destructobounce")
    game = Game(screen)
    game.run()

    running = True
    while running:
        game.handle_events()
        game.update()
        game.draw()
    
    pygame.quit()