# destructobounce/paddle.py

import pygame

class Turret:
    def __init__(self, screen_width, screen_height):
        self.width = 100
        self.height = 20
        self.color = (200, 200, 255)
        self.speed = 400  # pixels per second

        # Start centered near bottom of the screen
        self.rect = pygame.Rect(
            (screen_width - self.width) // 2,
            screen_height - self.height - 30,
            self.width,
            self.height
        )

    def move(self, direction, dt):
        if direction == "left":
            self.rect.x -= self.speed * dt
        elif direction == "right":
            self.rect.x += self.speed * dt

    def clamp_to_screen(self, screen_width):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)