# room.py
import pygame
import random
import settings
from enemy import Enemy

class Room:
    def __init__(self, room_number=1):
        self.width = random.randint(600, settings.WIDTH)
        self.height = random.randint(400, settings.HEIGHT)
        self.rect = pygame.Rect(
            (settings.WIDTH - self.width) // 2,
            (settings.HEIGHT - self.height) // 2,
            self.width, self.height
        )
        # Obstacles have been removed.
        self.obstacles = []  # (Not used)

        room_area = self.width * self.height
        num_enemies = max(min(room_area // 30000, 9), 4)
        self.enemies = pygame.sprite.Group()
        for _ in range(num_enemies):
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                enemy_x = random.randint(self.rect.left, self.rect.right)
                enemy_y = random.randint(self.rect.top, self.rect.bottom)
                enemy_type = random.choice(["orc", "bat"])
                enemy = Enemy((enemy_x, enemy_y), enemy_type=enemy_type,
                              strength_multiplier=1 + (room_number - 1) * 0.2)
                self.enemies.add(enemy)
                placed = True
                attempts += 1

    def get_safe_spawn_point(self):
        # With no obstacles, return the center of the room.
        return self.rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        # Removed obstacle drawing.
