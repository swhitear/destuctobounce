import pygame

# --- Projectile class ---
class Destructorb:
    def __init__(self, pos, config, color=None, max_collisions=1, collision_cost=1):
        """pos: tuple of (x, y) coordinates as ints"""
        self.x, self.y = pos
        self.config = config
        self.speed_x = 0  # No horizontal movement by default
        self.speed_y = -abs(config.ORB_SPEED)  # Always start moving up
        self.radius = config.ORB_RADIUS
        self.color = color if color is not None else config.ORB_COLOR
        self.max_collisions = max_collisions
        self.collision_cost = collision_cost
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.collisions = 0

    def update_rect(self):
        """Update rectangle position without movement"""
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def update(self):
        """Move projectile and bounce off top, left, and right edges."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off left edge
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x = -self.speed_x

        # Bounce off right edge
        if self.x + self.radius >= self.config.SCREEN_WIDTH:
            self.x = self.config.SCREEN_WIDTH - self.radius
            self.speed_x = -self.speed_x

        # Bounce off top edge
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = -self.speed_y

        # Add collision cost if it leaves the bottom
        if self.y + self.radius > self.config.SCREEN_HEIGHT:
            self.collide(self.max_collisions)  # Force enough collisions to make it defunct

        # Update rectangle position
        self.update_rect()

    def leaves_bottom(self):
        return self.y - self.radius > self.config.SCREEN_HEIGHT

    def defunct(self):
        return self.collisions >= self.max_collisions
    
    def is_active(self):
        return not self.leaves_bottom() and not self.defunct()
    
    def collide(self, cost: int):
        self.collisions += cost
        
    def draw(self, screen):
        if self.is_active():
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
# --- End Projectile class ---