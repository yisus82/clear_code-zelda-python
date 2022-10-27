from os import path

import pygame
from settings import SPELLS, WEAPONS
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack,
                 create_spell, destroy_spell):
        super().__init__(groups)
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -25)
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = 400
        self.obstacle_sprites = obstacle_sprites
        self.weapon_index = 0
        self.weapon = WEAPONS[[*WEAPONS][self.weapon_index]]
        self.switching_weapon = False
        self.weapon_switch_time = 0
        self.weapon_switch_cooldown = 200
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.spell_index = 0
        self.spell = SPELLS[[*SPELLS][self.spell_index]]
        self.switching_spell = False
        self.spell_switch_time = 0
        self.spell_switch_cooldown = 200
        self.create_spell = create_spell
        self.destroy_spell = destroy_spell
        self.initial_stats = {
            'health': 100,
            'mana': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5,
        }
        self.current_stats = {
            'health': self.initial_stats['health'],
            'mana': self.initial_stats['mana'],
            'speed': self.initial_stats['speed'],
            'attack': self.initial_stats['attack'],
            'magic': self.initial_stats['magic'],
            'exp': 0,
        }

    def import_player_assets(self):
        character_folder = path.join('..', 'graphics', 'player')
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
        if not self.attacking:
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
            if keys[pygame.K_SPACE] or keys[pygame.K_j]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.create_attack()
            elif keys[pygame.K_LCTRL] or keys[pygame.K_k]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.create_spell()
            elif not self.switching_weapon and (keys[pygame.K_LALT] or keys[pygame.K_u]):
                self.switching_weapon = True
                self.weapon_switch_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.change_weapon()
            elif not self.switching_spell and (keys[pygame.K_LSHIFT] or keys[pygame.K_i]):
                self.switching_spell = True
                self.spell_switch_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.change_spell()

    def move(self):
        if self.rect is not None:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.hitbox.move_ip(self.direction.x *
                                self.current_stats['speed'], 0)
            self.collide('horizontal')
            self.hitbox.move_ip(0, self.direction.y *
                                self.current_stats['speed'])
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

    def change_weapon(self):
        self.weapon_index = (self.weapon_index + 1) % len(WEAPONS)
        self.weapon = WEAPONS[[*WEAPONS][self.weapon_index]]

    def change_spell(self):
        self.spell_index = (self.spell_index + 1) % len(SPELLS)
        self.spell = SPELLS[[*SPELLS][self.spell_index]]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            self.destroy_attack()
            self.destroy_spell()
        if self.switching_weapon and current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
            self.switching_weapon = False
        if self.switching_spell and current_time - self.spell_switch_time >= self.spell_switch_cooldown:
            self.switching_spell = False

    def update_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'
        elif self.direction.x == 1 and self.direction.y == 0:
            self.status = 'right'
        elif self.direction.x == -1 and self.direction.y == 0:
            self.status = 'left'
        elif self.direction.y > 0:
            self.status = 'down'
        elif self.direction.y < 0:
            self.status = 'up'
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        self.image = animation[int(self.frame_index % len(animation))]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.cooldowns()
        self.input()
        self.update_status()
        self.animate()
        self.move()
