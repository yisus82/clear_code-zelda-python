import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(position[0], position[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -10)
