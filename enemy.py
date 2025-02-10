# enemy.py
import pygame
from pygame.math import Vector2
import settings
from animation import Animation

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type="orc", strength_multiplier=1.0):
        super().__init__()
        self.enemy_type = enemy_type
        self.strength_multiplier = strength_multiplier
        self.death_animation_done = False  # Flag to track death animation completion

        if enemy_type == "orc":
            self.animations = {
                "walk": Animation(
                    pygame.image.load("assets/images/Orc-Walk.png").convert_alpha(),
                    frame_width=100, frame_height=100, num_frames=8, frame_rate=100, loop=True
                ),
                "attack": Animation(
                    pygame.image.load("assets/images/Orc-Attack01.png").convert_alpha(),
                    frame_width=100, frame_height=100, num_frames=6, frame_rate=80, loop=False
                ),
                "death": Animation(
                    pygame.image.load("assets/images/Orc-Death.png").convert_alpha(),
                    frame_width=100, frame_height=100, num_frames=4, frame_rate=150, loop=False
                ),
                "hurt": Animation(
                    pygame.image.load("assets/images/Orc-Hurt.png").convert_alpha(),
                    frame_width=100, frame_height=100, num_frames=4, frame_rate=150, loop=False
                )
            }
            self.state = "walk"
            self.current_animation = self.animations[self.state]
            self.image = self.current_animation.get_current_frame()
            self.speed = 1.5 * strength_multiplier
            self.health = 100 * strength_multiplier
            self.damage = 10 * strength_multiplier
        elif enemy_type == "bat":
            self.animations = {
                "walk": Animation(
                    pygame.image.load("assets/images/Bat-Run.png").convert_alpha(),
                    frame_width=64, frame_height=64, num_frames=8, frame_rate=100, loop=True
                ),
                "attack": Animation(
                    pygame.image.load("assets/images/Bat-Attack1.png").convert_alpha(),
                    frame_width=64, frame_height=64, num_frames=8, frame_rate=100, loop=False
                ),
                "death": Animation(
                    pygame.image.load("assets/images/Bat-Die.png").convert_alpha(),
                    frame_width=64, frame_height=64, num_frames=12, frame_rate=80, loop=False
                ),
                "hurt": Animation(
                    pygame.image.load("assets/images/Bat-Hurt.png").convert_alpha(),
                    frame_width=64, frame_height=64, num_frames=5, frame_rate=100, loop=False
                )
            }
            self.state = "walk"
            self.current_animation = self.animations[self.state]
            self.image = self.current_animation.get_current_frame()
            self.speed = 3 * strength_multiplier
            self.health = 50 * strength_multiplier
            self.damage = 5 * strength_multiplier

        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.attack_cooldown = 2000  # milliseconds
        self.last_attack_time = 0
        self.attacking = False

    def take_damage(self, damage):
        # Prevent taking damage if already in death state.
        if self.state == "death":
            return

        self.health -= damage
        if self.health > 0:
            self.state = "hurt"
            self.current_animation = self.animations["hurt"]
            self.current_animation.reset()
        else:
            self.state = "death"
            self.death_animation_done = False
            self.current_animation = self.animations["death"]
            self.current_animation.reset()

    def update(self, player, current_time):
        # Handle hurt state: update the hurt animation, and when finished, resume walking.
        if self.state == "hurt":
            self.current_animation.update()
            self.image = self.current_animation.get_current_frame()
            if self.current_animation.finished:
                self.state = "walk"
                self.current_animation = self.animations["walk"]
                self.current_animation.reset()
            return

        # Handle death state: update death animation and mark as done when finished.
        if self.state == "death":
            self.current_animation.update()
            self.image = self.current_animation.get_current_frame()
            if self.current_animation.finished:
                self.death_animation_done = True
            return

        # Normal behavior (walking, attacking)
        # Move toward the player.
        direction = player.pos - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.pos += direction * self.speed
        self.rect.center = self.pos

        # Check if within attack range (scaled).
        if (player.pos - self.pos).length() < int(50 * settings.SCALE) and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            self.attacking = True
            self.state = "attack"
            self.current_animation = self.animations["attack"]
            self.current_animation.reset()

        # If attack animation has finished, deal damage and reset state.
        if self.attacking and self.current_animation.finished:
            if (player.pos - self.pos).length() < int(50 * settings.SCALE):
                player.take_damage(self.damage)
            self.attacking = False
            self.state = "walk"
            self.current_animation = self.animations["walk"]
            self.current_animation.reset()

        self.current_animation.update()
        self.image = self.current_animation.get_current_frame()
