import pygame

class Screen:
    def __init__(self, config):
        self.config = config

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

    def on_enter(self):
        """Called when this screen becomes active"""
        pass

    def on_exit(self):
        """Called when this screen is being switched from"""
        pass

class TitleScreen(Screen):
    def __init__(self, config):
        super().__init__(config)
        self.font = pygame.font.Font(None, 74)
        self.title_text = 'DESTRUCTOBOUNCE'
        
        # Menu options
        self.menu_font = pygame.font.Font(None, 36)
        self.menu_items = ['Start Game', 'Options']
        self.selected_option = 0
        
        # Calculate positions
        self.title_rect = pygame.Rect(0, 0, 0, 0)
        self.title_rect.centerx = config.SCREEN_WIDTH // 2
        self.title_rect.centery = 200
        
        self.menu_rects = []
        for i, _ in enumerate(self.menu_items):
            rect = pygame.Rect(0, 0, 0, 0)
            rect.centerx = config.SCREEN_WIDTH // 2
            rect.centery = 400 + (i * 50)
            self.menu_rects.append(rect)

    def handle_events(self, events):
        from .screen_manager import ScreenManager
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_items)
                elif event.key == pygame.K_1:
                    self.selected_option = 0
                elif event.key == pygame.K_2:
                    self.selected_option = 1
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Start Game
                        from .game import Game
                        game_screen = Game(self.config)
                        ScreenManager().set_screen(game_screen)
                    elif self.selected_option == 1:  # Options
                        options_screen = OptionsScreen(self.config)
                        ScreenManager().set_screen(options_screen)

    def draw(self, surface):
        # Fill background
        surface.fill((0, 0, 0))
        
        # Draw title
        title_surface = self.font.render(self.title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=self.title_rect.center)
        surface.blit(title_surface, title_rect)
        
        # Draw menu options
        for i, (text, rect) in enumerate(zip(self.menu_items, self.menu_rects)):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text_surface = self.menu_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            surface.blit(text_surface, text_rect)

class OptionsScreen(Screen):
    def __init__(self, config):
        super().__init__(config)
        self.font = pygame.font.Font(None, 74)
        self.title_text = 'Options'
        self.title_rect = pygame.Rect(0, 0, 0, 0)
        self.title_rect.centerx = config.SCREEN_WIDTH // 2
        self.title_rect.centery = 200
        
    def handle_events(self, events):
        from .screen_manager import ScreenManager
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to title screen
                    from .screen import TitleScreen
                    title_screen = TitleScreen(self.config)
                    ScreenManager().set_screen(title_screen)

    def draw(self, surface):
        # Fill background
        surface.fill((0, 0, 0))
        
        # Draw title
        title_surface = self.font.render(self.title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=self.title_rect.center)
        surface.blit(title_surface, title_rect)