import pygame

# --- Projectile class ---
class Destructorb:
    COLOR = (255, 255, 255)  # white

    def __init__(self, pos, screen_width, screen_height, speed=7, radius=5, color=COLOR):
        """pos: tuple of (x, y) coordinates as ints"""
        self.x, self.y = pos
        self.speed_x = 0  # No horizontal movement by default
        self.speed_y = -abs(speed)  # Always start moving up
        self.radius = radius
        self.color = color
        self.active = True
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        """Move projectile and bounce off top, left, and right edges."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off left edge
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x = -self.speed_x

        # Bounce off right edge
        if self.x + self.radius >= self.screen_width:
            self.x = self.screen_width - self.radius
            self.speed_x = -self.speed_x

        # Bounce off top edge
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = -self.speed_y

        # Deactivate if it somehow leaves the bottom (optional)
        if self.y - self.radius > self.screen_height:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
# --- End Projectile class ---