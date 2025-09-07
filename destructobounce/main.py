import pygame
from .config import Config
from .game import Game
print("Loading Main")
def main():
    pygame.init()

    config = Config()  # Create Config instance here (no file yet)
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Destructobounce")

    game = Game(screen, config)  # Pass it to the Game constructor
    game.run()

    pygame.quit()