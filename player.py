# player.py
import pygame
from pygame.math import Vector2
import settings
from animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load soldier animations (each frame 100x100).
        self.animations = {
            "walk": Animation(
                pygame.image.load("assets/images/Soldier-Walk.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=8, frame_rate=100, loop=True
            ),
            "attack01": Animation(
                pygame.image.load("assets/images/Soldier-Attack01.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=6, frame_rate=80, loop=False
            ),
            "attack02": Animation(
                pygame.image.load("assets/images/Soldier-Attack02.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=6, frame_rate=80, loop=False
            ),
            "attack03": Animation(
                pygame.image.load("assets/images/Soldier-Attack03.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=9, frame_rate=80, loop=False
            ),
            "death": Animation(
                pygame.image.load("assets/images/Soldier-Death.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=4, frame_rate=150, loop=False
            ),
            "hurt": Animation(
                pygame.image.load("assets/images/Soldier-Hurt.png").convert_alpha(),
                frame_width=100, frame_height=100, num_frames=4, frame_rate=150, loop=False
            )
        }
        self.state = "walk"
        self.current_animation = self.animations[self.state]
        self.image = self.current_animation.get_current_frame()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 3
        self.health = 100
        self.max_health = 100
        self.damage = 40
        self.attack_speed = 0.5  # seconds between attacks
        self.last_attack_time = 0
        self.attacking = False
        self.facing = "right"
        self.old_pos = self.pos.copy()
        self.invulnerable_until = 0

    def update(self, keys_pressed):
        current_time = pygame.time.get_ticks()
        if self.state == "hurt" and (current_time >= self.invulnerable_until or self.current_animation.finished):
            self.state = "walk"
            self.current_animation = self.animations["walk"]
            self.current_animation.reset()

        self.old_pos = self.pos.copy()
        self.vel = Vector2(0, 0)
        if keys_pressed[pygame.K_w]:
            self.vel.y = -self.speed
        if keys_pressed[pygame.K_s]:
            self.vel.y = self.speed
        if keys_pressed[pygame.K_a]:
            self.vel.x = -self.speed
            self.facing = "left"
        if keys_pressed[pygame.K_d]:
            self.vel.x = self.speed
            self.facing = "right"

        if not self.attacking:
            self.state = "walk"

        if self.current_animation != self.animations[self.state]:
            self.current_animation = self.animations[self.state]
            self.current_animation.reset()

        self.current_animation.update()
        self.image = self.current_animation.get_current_frame()
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        # Simple movement without collision detection.
        self.pos += self.vel
        self.pos.x = max(0, min(settings.WIDTH, self.pos.x))
        self.pos.y = max(0, min(settings.HEIGHT, self.pos.y))
        self.rect.center = self.pos

        if self.state in ["attack01", "attack02", "attack03"] and self.current_animation.finished:
            self.attacking = False
            self.state = "walk"
            self.current_animation = self.animations["walk"]
            self.current_animation.reset()

    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()
        if current_time < self.invulnerable_until:
            return

        self.health -= damage
        if self.health > 0:
            self.invulnerable_until = current_time + 500
            self.state = "hurt"
            self.current_animation = self.animations["hurt"]
            self.current_animation.reset()
        else:
            self.state = "death"
            self.current_animation = self.animations["death"]
            self.current_animation.reset()

    def attack(self, current_time, target_pos, projectile_group, attack_type="melee", effective_damage=None):
        if self.state == "hurt":
            self.state = "walk"
            self.current_animation = self.animations["walk"]
            self.current_animation.reset()

        if current_time - self.last_attack_time < self.attack_speed * 1000:
            return None

        self.last_attack_time = current_time
        self.attacking = True

        if attack_type == "ranged":
            self.state = "attack03"
        else:
            self.state = "attack02"
        self.current_animation = self.animations[self.state]
        self.current_animation.reset()

        from pygame.math import Vector2
        direction = Vector2(target_pos) - self.pos
        if direction.length() != 0:
            direction = direction.normalize()

        if attack_type == "ranged":
            from projectile import Projectile
            if effective_damage is None:
                effective_damage = self.damage
            proj = Projectile(self.pos, direction, effective_damage)
            projectile_group.add(proj)
            return ("attack", proj)
        else:
            # Adjusted melee attack radius.
            attack_radius = int(40 * settings.SCALE)
            return ("melee", (self.pos.copy(), attack_radius))
