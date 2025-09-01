import pygame
import sys
from destructobounce.turret import Turret
from destructobounce.projectile import Projectile

class Game:
    def __init__(self, surface: pygame.Surface):
        # Load any assets, initialize game state here
        self.background_color = (0, 0, 0)  # black background
        self.running = True
        self.screen = surface
        self.clock = pygame.time.Clock()

        # player turret
        self.turret = Turret(self.screen.get_width(), self.screen.get_height())
        # Keep track of projectiles
        self.projectiles = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fire from the center top of the turret
                    x, y = self.turret.fire_location()
                    proj = Projectile((x, y), self.screen.get_width(), self.screen.get_height())
                    self.projectiles.append(proj)
                    
                    # bail out
                    # self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.turret.move(Turret.LEFT, dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turret.move(Turret.RIGHT, dt)

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()

        # Remove inactive ones
        self.projectiles = [p for p in self.projectiles if p.active]

        self.turret.clamp_to_screen(self.screen.get_width())

    def draw(self):
        #window
        self.screen.fill(self.background_color)
        
        # sprites and things
        self.turret.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)

        # render
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