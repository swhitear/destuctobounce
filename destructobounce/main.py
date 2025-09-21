import pygame
from .config import Config
from .screen_manager import ScreenManager
from .screen import TitleScreen

def main():
    pygame.init()

    config = Config()
    surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Destructobounce")

    # Initialize screen manager with title screen
    screen_manager = ScreenManager()
    title_screen = TitleScreen(config)
    screen_manager.set_screen(title_screen)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Handle events and update current screen
        screen_manager.handle_events(events)
        screen_manager.update()
        
        # Clear screen and draw current screen
        surface.fill((0, 0, 0))
        screen_manager.draw(surface)
        
        pygame.display.flip()