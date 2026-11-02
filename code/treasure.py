import pygame
from settings import TILESIZE

class BuriedTreasure(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.state = 'hidden'

        self.hidden_image = pygame.Surface((32, 24), pygame.SRCALPHA)
        self.marked_image = self.hidden_image.copy()
        pygame.draw.line(self.marked_image, '#e59945', (6, 4), (26, 20), 4)
        pygame.draw.line(self.marked_image, '#e59945', (26, 4), (6, 20), 4)

        self.open_image = self.hidden_image.copy()
        pygame.draw.ellipse(self.open_image, '#37281d', (2, 8, 28, 14))
        pygame.draw.ellipse(self.open_image, '#795235', (2, 8, 28, 14), 2)

        self.image = self.hidden_image
        self.rect = self.image.get_rect(center=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE // 2
        ))
        self.hitbox = self.rect.copy()

    def get_interaction_text(self):
        if self.state == 'marked':
            return 'Press F to dig for treasure'
        return ''

    def reveal(self):
        if self.state == 'hidden':
            self.state = 'marked'
            self.image = self.marked_image

    def open(self):
        if self.state != 'marked':
            return False

        self.state = 'opened'
        self.image = self.open_image
        return True

class TreasureClue(pygame.sprite.Sprite):
    def __init__(self, pos, groups, treasure, hint):
        super().__init__(groups)
        self.treasure = treasure
        self.hint = hint
        self.collected = False

        self.image = pygame.Surface((24, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, '#b48a52', (1, 1, 22, 26))
        pygame.draw.rect(self.image, '#ead4a0', (3, 3, 18, 22))

        for y in (8, 13, 18):
            pygame.draw.line(self.image, '#715132', (7, y), (17, y), 2)

        self.rect = self.image.get_rect(center=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE // 2
        ))
        self.hitbox = self.rect.copy()

    def get_interaction_text(self):
        return '' if self.collected else 'Press F to read clue'

    def read(self):
        if self.collected:
            return False

        self.collected = True
        self.treasure.reveal()
        self.kill()
        return True
