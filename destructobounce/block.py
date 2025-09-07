import pygame

class Block:
    def __init__(self, x, y, config, color=None, max_collisions=1, collision_cost=1):
        self.rect = pygame.Rect(x, y, config.BLOCK_WIDTH, config.BLOCK_HEIGHT)
        self.color = config.BLOCK_COLOR if color is None else color
        self.collisions = 0
        self.max_collisions = max_collisions
        self.collision_cost = collision_cost
        self.font = pygame.font.Font(None, 20)  # Choose your font and size

    def update(self):
        # change color based on remaining collisions
        self.color = (
            max(0, 200 - self.collisions * 50),
            max(0, 200 - self.collisions * 50),
            max(0, 200 - self.collisions * 50)
        )

    def defunct(self):
        return self.collisions >= self.max_collisions
    
    def is_active(self):
        return not self.defunct()
    
    def collide(self, cost: int):
          self.collisions += cost
    
    def draw(self, surface):
        if not self.defunct():
            pygame.draw.rect(surface, self.color, self.rect)

            # Draw the collision count
            text_surface = self.font.render(str(self.max_collisions - self.collisions), True, (0,0,0)) # Render text
            text_rect = text_surface.get_rect(center=self.rect.center) # Center the text
            surface.blit(text_surface, text_rect) # Draw the text