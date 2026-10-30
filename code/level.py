import pygame
from settings import WORLD_MAP, TILESIZE
from tile import Tile
from player import Player, YSortCameraGroup
from support import import_csv_layout
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

        self.ui = UI()

    def create_map(self):
        layout = import_csv_layout('map/world.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile(
                        (x, y),
                        [self.visible_sprites, self.obstacle_sprites]
                    )
                elif col == 'p':
                    self.player = Player(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.create_attack,
                        self.destroy_attack
                    )

    def create_attack(self):
        self.current_attack = Weapon(
            self.player,
            [self.visible_sprites]
        )

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)