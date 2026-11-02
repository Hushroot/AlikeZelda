import pygame
from settings import *
from chest import Chest
from exit_gate import ExitGate
from treasure import BuriedTreasure, TreasureClue

class WorldMap:
    def __init__(self, layout):
        self.layout = layout
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.explored = set()
        self.last_tile = None
        self.reveal_radius = 5

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, 18)
        self.small_font = pygame.font.Font(UI_FONT, 14)

        self.tile_size = min(16, (self.display_surface.get_width() - 120) // self.cols,
        (self.display_surface.get_height() - 220) // self.rows)

        self.surface = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size))
        self.rect = self.surface.get_rect(center=self.display_surface.get_rect().center)
        self.panel_rect = self.rect.inflate(48, 176)

        self.overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.colors = {
            'x': '#777681', 'd': '#946439', 'p': '#946439',
            's': '#946439', 'c': '#946439', 'r': '#a77b52',
            'g': '#946439', 't': '#21472d', 'h': '#a77b52',
            'f': '#a77b52', 'b': '#2d5734', 'v': '#70974c'
        }

    def reveal(self, pos):
        col = int(pos[0] // TILESIZE)
        row = int(pos[1] // TILESIZE)

        if self.last_tile == (col, row):
            return

        self.last_tile = (col, row)
        radius = self.reveal_radius

        for y in range(max(0, row - radius), min(self.rows, row + radius + 1)):
            for x in range(max(0, col - radius), min(self.cols, col + radius + 1)):
                if (x - col) ** 2 + (y - row) ** 2 <= radius ** 2:
                    self.explored.add((x, y))

    def map_pos(self, pos):
        return (int(pos[0] / TILESIZE * self.tile_size), int(pos[1] / TILESIZE * self.tile_size))

    def display(self, player, interactions):
        self.surface.fill('#080b10')

        for row_index, row in enumerate(self.layout):
            for col_index, col in enumerate(row):
                color = '#10131b'

                if (col_index, row_index) in self.explored:
                    color = self.colors.get(col, '#3b6e36')

                pygame.draw.rect(self.surface, color, (
                    col_index * self.tile_size,
                    row_index * self.tile_size,
                    self.tile_size - 1,
                    self.tile_size - 1
                ))

        for sprite in interactions:
            col = sprite.hitbox.centerx // TILESIZE
            row = sprite.hitbox.centery // TILESIZE

            if isinstance(sprite, BuriedTreasure):
                if sprite.state == 'hidden':
                    continue

                color = '#888888' if sprite.state == 'opened' else '#e59945'
                x, y = self.map_pos(sprite.hitbox.center)

                pygame.draw.line(
                    self.surface, color, (x - 4, y - 4), (x + 4, y + 4), 2
                )
                pygame.draw.line(
                    self.surface, color, (x + 4, y - 4), (x - 4, y + 4), 2
                )
                continue

            if (col, row) not in self.explored:
                continue

            width = 0

            if isinstance(sprite, Chest):
                color = '#bb66ff' if sprite.cursed else '#e6c36a'

                if sprite.state == 'opened':
                    color = '#888888'
                    width = 1
            elif isinstance(sprite, TreasureClue):
                color = '#ead4a0'
            elif isinstance(sprite, ExitGate):
                color = '#7ee0bf'
            else:
                continue

            marker = pygame.Rect(0, 0, 6, 6)
            marker.center = self.map_pos(sprite.hitbox.center)

            pygame.draw.rect(self.surface, color, marker, width)

        pygame.draw.circle(
            self.surface,
            'white',
            self.map_pos(player.hitbox.center),
            4
        )

        self.display_surface.blit(self.overlay, (0, 0))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.panel_rect)
        pygame.draw.rect(self.display_surface, '#bb66ff', self.panel_rect, 2)
        self.display_surface.blit(self.surface, self.rect)

        labels = [
            (self.font, 'World Map', self.panel_rect.top + 26, TEXT_COLOR),
            (self.small_font, 'White: You   Gold: Chest   Purple: Cursed   Teal: Exit', self.rect.bottom + 20, TEXT_COLOR),
            (self.small_font, 'Paper: Clue   Orange X: Treasure   Gray: Opened', self.rect.bottom + 42, TEXT_COLOR),
            (self.font, 'TAB: Close map', self.panel_rect.bottom - 18, UI_BORDER_COLOR_ACTIVE)
        ]

        for font, text, y, color in labels:
            text_surf = font.render(text, False, color)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, y))

            self.display_surface.blit(text_surf, text_rect)
