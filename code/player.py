from os import path

import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.import_player_assets()
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -25)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = 400
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_folder = '../graphics/player/'
        self.animations = {
            'up': [],
            'up_idle': [],
            'up_attack': [],
            'down': [],
            'down_idle': [],
            'down_attack': [],
            'left': [],
            'left_idle': [],
            'left_attack': [],
            'right': [],
            'right_idle': [],
            'right_attack': [],
        }
        for animation_name in self.animations.keys():
            animation_folder = path.join(character_folder, animation_name)
            self.animations[animation_name] = import_folder(animation_folder)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if not self.attacking and keys[pygame.K_SPACE] or keys[pygame.K_j]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        if not self.attacking and keys[pygame.K_LCTRL] or keys[pygame.K_k]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')

    def move(self):
        if self.rect is not None:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.hitbox.move_ip(self.direction.x * self.speed, 0)
            self.collide('horizontal')
            self.hitbox.move_ip(0, self.direction.y * self.speed)
            self.collide('vertical')
            self.rect.center = self.hitbox.center

    def collide(self, direction):
        if self.rect is not None:
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
            elif direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

    def update(self):
        self.cooldowns()
        self.input()
        self.move()
