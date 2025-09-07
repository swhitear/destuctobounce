# destructobounce/paddle.py

import math
import pygame

class Turret:
    LEFT = "left"
    RIGHT = "right"
    PIVOT_LEFT = "pivot_left"
    PIVOT_RIGHT = "pivot_right"

    def __init__(self, config):
        self.width = 40
        self.height = 20
        self.barrel_length = 15
        self.color = config.COLOR_WHITE
        self.barrel_color = config.COLOR_YELLOW
        self.speed = 400  # pixels per second

        # Start centered near bottom of the screen
        self.rect = pygame.Rect(
            (config.SCREEN_WIDTH - self.width) // 2,
            config.SCREEN_HEIGHT - self.height - 30,
            self.width,
            self.height
        )
        self.pivot_angle = 90  # 90 degrees = straight up
        self.min_angle = 15    # 90 - 75 = 15 degrees (left limit)
        self.max_angle = 165   # 90 + 75 = 165 degrees (right limit)

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def fire_location(self):
        # Return (x, y) coordinates for the projectile spawn point (center top of turret)
        return (self.x + self.width // 2, self.y)

    def fire_direction(self):
        # Returns a unit vector (dx, dy) in the direction of the current pivot_angle
        radians = math.radians(self.pivot_angle)
        dx = math.cos(radians)
        dy = -math.sin(radians)
        return (dx, dy)

    def move(self, direction, dt):
        if direction == Turret.LEFT:
            self.rect.x -= self.speed * dt
        elif direction == Turret.RIGHT:
            self.rect.x += self.speed * dt

    def pivot(self, direction):
        if direction == Turret.PIVOT_LEFT:
            self.pivot_angle = min(self.pivot_angle + 1, self.max_angle)
        elif direction == Turret.PIVOT_RIGHT:
            self.pivot_angle = max(self.pivot_angle - 1, self.min_angle)

    def clamp_to_screen(self, screen_width):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, surface):
        # Draw the turret base
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw the turret barrel as a line
        center_x = self.x + self.width // 2
        center_y = self.y
        dx, dy = self.fire_direction()
        end_x = int(center_x + self.barrel_length * dx)
        end_y = int(center_y + self.barrel_length * dy)
        pygame.draw.line(surface, self.barrel_color, (center_x, center_y), (end_x, end_y), 4)