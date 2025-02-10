# game.py
import pygame
import settings
from room import Room
from player import Player
from ui import draw_health_bar, draw_text, pause_menu
from pygame.math import Vector2
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.current_room_number = 1
        self.current_room = Room(room_number=self.current_room_number)
        spawn_point = self.current_room.get_safe_spawn_point()
        self.player = Player(spawn_point)
        self.projectiles = pygame.sprite.Group()
        self.score = 0
        self.rooms_cleared = 0
        self.running = True
        self.attack_charge_start = None
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)

    def get_effective_damage(self):
        if self.current_room_number >= 6:
            return self.player.damage / 3
        elif self.current_room_number >= 3:
            return self.player.damage / 2
        else:
            return self.player.damage

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)
            current_time = pygame.time.get_ticks()
            self.handle_events(current_time)
            # Update the player without any obstacle collision.
            keys_pressed = pygame.key.get_pressed()
            self.player.update(keys_pressed)
            self.projectiles.update()

            for enemy in list(self.current_room.enemies):
                enemy.update(self.player, current_time)
                for proj in self.projectiles:
                    if enemy.rect.colliderect(proj.rect):
                        enemy.take_damage(proj.damage)
                        proj.kill()
                if enemy.state == "death" and enemy.death_animation_done:
                    enemy.kill()
                    self.score += 50

            if len(self.current_room.enemies) == 0:
                self.rooms_cleared += 1
                self.player.damage += 5
                self.player.max_health += 10
                self.player.health = self.player.max_health
                self.current_room_number += 1
                self.current_room = Room(room_number=self.current_room_number)
            
            self.draw()
            pygame.display.flip()
            if self.player.health <= 0:
                self.running = False

    def handle_events(self, current_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_p:
                    self.pause_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.attack_charge_start = current_time
                elif event.button == 3:
                    effective_damage = self.get_effective_damage()
                    self.player.attack(current_time, pygame.mouse.get_pos(), self.projectiles,
                                       attack_type="ranged", effective_damage=effective_damage)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.attack_charge_start is not None:
                        charge_duration = current_time - self.attack_charge_start
                        if charge_duration >= 500:
                            result = self.player.attack(current_time, pygame.mouse.get_pos(), self.projectiles,
                                                        attack_type="charged")
                        else:
                            result = self.player.attack(current_time, pygame.mouse.get_pos(), self.projectiles,
                                                        attack_type="melee")
                        if result is not None and result[0] == "melee":
                            center, radius = result[1]
                            effective_damage = self.get_effective_damage()
                            for enemy in self.current_room.enemies:
                                if (enemy.pos - center).length() <= radius:
                                    if self.player.facing == "right" and enemy.pos.x >= center.x:
                                        enemy.take_damage(effective_damage)
                                    elif self.player.facing == "left" and enemy.pos.x <= center.x:
                                        enemy.take_damage(effective_damage)
                        self.attack_charge_start = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.current_room.draw(self.screen)
        self.current_room.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.projectiles.draw(self.screen)
        draw_health_bar(self.screen, 10, 10, self.player.health, self.player.max_health)
        draw_text(self.screen, f"Score: {self.score}", 20, (255, 255, 255), (10, 30))
        draw_text(self.screen, f"Room: {self.current_room_number}", 20, (255, 255, 255), (10, 50))

    def pause_game(self):
        paused = True
        pause_menu(self.screen)
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            pygame.display.flip()
            self.clock.tick(settings.FPS)
