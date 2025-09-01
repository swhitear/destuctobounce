import pygame
import sys
from destructobounce.turret import Turret
from destructobounce.destructorb import Destructorb 

class Game:
    def __init__(self, surface: pygame.Surface):
        # Load any assets, initialize game state here
        self.background_color = (0, 0, 0)  # black background
        self.running = True
        self.screen = surface
        self.clock = pygame.time.Clock()

        # player turret
        self.turret = Turret(self.screen.get_width(), self.screen.get_height())
        # Keep track of destructorbs
        self.destructorbs = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fire from the turret barrel in the aimed direction
                    x, y = self.turret.fire_location()
                    dx, dy = self.turret.fire_direction()
                    orb = Destructorb(
                        (x, y),
                        self.screen.get_width(),
                        self.screen.get_height(),
                        speed=7,
                        radius=5,
                        color=(255, 255, 255)
                    )
                    orb.speed_x = dx * abs(orb.speed_y)
                    orb.speed_y = dy * abs(orb.speed_y)
                    self.destructorbs.append(orb)
                    
                    # bail out
                    # self.running = False

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

        # Update destructorbs
        for destructorb in self.destructorbs:
            destructorb.update()

        # Remove inactive ones
        self.destructorbs = [d for d in self.destructorbs if d.active]

        self.turret.clamp_to_screen(self.screen.get_width())

    def draw(self):
        #window
        self.screen.fill(self.background_color)
        
        # sprites and things
        self.turret.draw(self.screen)
        for destructorb in self.destructorbs:
            destructorb.draw(self.screen)

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