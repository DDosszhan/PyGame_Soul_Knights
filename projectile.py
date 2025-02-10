# projectile.py
import pygame
from pygame.math import Vector2
import settings

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, damage):
        super().__init__()
        # Scale the projectile's size using settings.SCALE.
        size = int(10 * settings.SCALE)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        radius = int(5 * settings.SCALE)
        pygame.draw.circle(self.image, (255, 255, 0), (size // 2, size // 2), radius)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direction = direction
        self.speed = 7 * settings.SCALE  # Projectile speed scaled if desired.
        self.damage = damage

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        # Remove projectile if it goes off-screen.
        if (self.pos.x < 0 or self.pos.x > settings.WIDTH or 
            self.pos.y < 0 or self.pos.y > settings.HEIGHT):
            self.kill()
