import pygame

# --- Projectile class ---
class Projectile:
    COLOR = (255, 255, 255)  # white

    def __init__(self, x, y, speed=7, radius=5, color=COLOR):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.color = color
        self.active = True

    def update(self):
        """Move projectile upwards."""
        self.y -= self.speed
        # deactivate if it leaves the screen
        if self.y < -self.radius:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
# --- End Projectile class ---