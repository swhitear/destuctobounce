import pygame
from .screen import Screen
from .turret import Turret
from .destructorb_group import DestructorbGroup
from .config import Config
from .block_pile import BlockPile
from .wall_block_gen import WallBlockGen
from .screen_manager import ScreenManager

class Game(Screen):
    def __init__(self, config: Config):
        super().__init__(config)
        self.background_color = self.config.COLOR_BLACK
        self.clock = pygame.time.Clock()

        self.turret = Turret(self.config)
        self.destructorbs = DestructorbGroup(self.config)
        self.wall_gen = WallBlockGen(self.config, row_count=3)
        self.block_pile = BlockPile(self.config, self.wall_gen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = self.turret.fire_location()
                    dx, dy = self.turret.fire_direction()
                    self.destructorbs.new_orb(x, y, dx, dy)
                elif event.key == pygame.K_ESCAPE:
                    # Return to title screen
                    from .screen import TitleScreen
                    title_screen = TitleScreen(self.config)
                    ScreenManager().set_screen(title_screen)

    def update(self):
        keys = pygame.key.get_pressed()
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        if keys[pygame.K_LEFT] or keys[pygame.K_z]:
            self.turret.move(Turret.LEFT, dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_c]:
            self.turret.move(Turret.RIGHT, dt)
        if keys[pygame.K_a]:
            self.turret.pivot(Turret.PIVOT_LEFT)
        if keys[pygame.K_d]:
            self.turret.pivot(Turret.PIVOT_RIGHT)

        # Update main collections
        self.block_pile.update()
        self.destructorbs.update()

        # Collision detection
        for orb in self.destructorbs:
            if self.block_pile.check_collision(orb):
                orb.kill()

    def draw(self, surface):
        # Fill background
        surface.fill(self.background_color)
        
        # Draw game objects
        self.block_pile.draw(surface)
        self.destructorbs.draw(surface)
        self.turret.draw(surface)