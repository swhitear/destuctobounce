# game.py

import pygame
import sys

class Game:
    def __init__(self, surface: pygame.Surface):
        # Load any assets, initialize game state here
        self.background_color = (0, 0, 0)  # black background
        self.running = True
        self.screen = surface
        self.clock = pygame.time.Clock()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt = None):
        # Update game state here
        pass

    def draw(self):
        self.screen.fill(self.background_color)
        # Draw game elements here
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Limit to 60 FPS, get delta time in seconds
            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()