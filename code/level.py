import pygame
from player import Player
from settings import *
from tile import Tile


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE
                if column == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif column == 'p':
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(self.display)
