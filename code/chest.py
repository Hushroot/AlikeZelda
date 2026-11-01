import pygame
from settings import TILESIZE

class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.closed_image = pygame.Surface((48, 40), pygame.SRCALPHA)

        pygame.draw.rect(self.closed_image, '#7a4828', (0, 8, 48, 32))
        pygame.draw.rect(self.closed_image, '#d9ad55', (0, 8, 48, 32), 3)
        pygame.draw.rect(self.closed_image, '#d9ad55', (0, 18, 48, 4))
        pygame.draw.rect(self.closed_image, '#d9ad55', (21, 15, 6, 12))

        self.open_image = self.closed_image.copy()
        pygame.draw.rect(self.open_image, '#211b16', (4, 8, 40, 16))
        pygame.draw.rect(self.open_image, '#d9ad55', (0, 0, 48, 8))

        self.image = self.closed_image
        self.rect = self.image.get_rect(midbottom=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE
        ))

        self.hitbox = self.rect.inflate(0, -12)
        self.opened = False

    def get_interaction_text(self):
        if self.opened:
            return ''

        return 'Press F to open'

    def open(self):
        if self.opened:
            return False

        self.opened = True
        self.image = self.open_image
        return True