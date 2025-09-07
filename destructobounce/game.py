import pygame
import sys
from destructobounce.turret import Turret
from destructobounce.destructorb_group import DestructorbGroup
from destructobounce.config import Config
from destructobounce.block_pile import BlockPile
from destructobounce.wall_block_gen import WallBlockGen

class Game:
    def __init__(self, surface: pygame.Surface, config: Config):
        self.config = config
        self.background_color = self.config.COLOR_BLACK
        self.running = True
        self.screen = surface
        self.clock = pygame.time.Clock()

        self.turret = Turret(self.config)
        self.destructorbs = DestructorbGroup(self.config)
        self.wall_gen = WallBlockGen(self.config, row_count=3)
        self.block_pile = BlockPile(self.config, self.wall_gen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # handle firing once per loop
                if event.key == pygame.K_SPACE:
                    x, y = self.turret.fire_location()
                    dx, dy = self.turret.fire_direction()
                    self.destructorbs.new_orb(x, y, dx, dy)

    def update(self, dt):
        keys = pygame.key.get_pressed()
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
            for block in self.block_pile:
                if orb.rect.colliderect(block.rect):
                    # Bounce the orb and increment collisions
                    if orb.rect.x < block.rect.x or orb.rect.x > block.rect.x + block.rect.width:
                        orb.speed_x *= -1   
                    else:
                        orb.speed_y *= -1
                    orb.collide(block.collision_cost)
                    block.collide(orb.collision_cost)

        self.turret.clamp_to_screen(self.screen.get_width())

    def draw(self):
        self.screen.fill(self.background_color)
        self.turret.draw(self.screen)
        self.block_pile.draw(self.screen)
        self.destructorbs.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()