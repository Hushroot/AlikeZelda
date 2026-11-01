import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT
        )
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT
        )
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.game_over_font = pygame.font.Font(UI_FONT, 48)
        self.game_over_overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        self.game_over_overlay.fill((0, 0, 0, 180))

        self.weapon_graphics = []

        self.loot_message = ''
        self.loot_color = TEXT_COLOR
        self.loot_time = 0
        self.loot_duration = 3000

        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []

        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_interaction(self, text, pos):
        text_surf = self.font.render(text, False, TEXT_COLOR)
        text_rect = text_surf.get_rect(midbottom=pos)
        background_rect = text_rect.inflate(20, 12)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, background_rect, 2)

        self.display_surface.blit(text_surf, text_rect)

    def show_loot(self, weapon, rarity, collected):
        name = f'{rarity.title()}{weapon.title()}'

        if collected:
            self.loot_message = f'Found: {name}'
        else:
            self.loot_message = f'{name} - kept your weapon'

        self.loot_color = rarity_data[rarity]['color']
        self.loot_time = pygame.time.get_ticks()

    def draw_loot(self):
        if not self.loot_message:
            return

        if pygame.time.get_ticks() - self.loot_time >= self.loot_duration:
            return

        text_surf = self.font.render(self.loot_message, False, self.loot_color)
        text_rect = text_surf.get_rect(midtop=(
            self.display_surface.get_width() // 2, 70
        ))
        background_rect = text_rect.inflate(24, 16)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)
        pygame.draw.rect(self.display_surface, self.loot_color, background_rect, 2)
        self.display_surface.blit(text_surf, text_rect)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface,  UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(
            self.display_surface,
            UI_BG_COLOR,
            text_rect.inflate(20, 20)
        )
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            UI_BORDER_COLOR,
            text_rect.inflate(20, 20),
            3
        )

    def display(self, player):
        self.show_bar(
            player.health,
            player.stats['health'],
            self.health_bar_rect,
            HEALTH_COLOR
        )
        self.show_bar(
            player.energy,
            player.stats['energy'],
            self.energy_bar_rect,
            ENERGY_COLOR
        )
        self.weapon_overlay(
            player.weapon_index,
            not player.can_switch_weapon
        )
        self.show_exp(player.exp)
        self.magic_overlay(
            player.magic_index,
            not player.can_switch_magic
        )
        self.draw_loot()

    def show_game_over(self):
        self.display_surface.blit(self.game_over_overlay, (0, 0))
        center_x = self.display_surface.get_width() // 2
        center_y = self.display_surface.get_height() // 2

        title = self.game_over_font.render('YOU DIED', False, TEXT_COLOR)
        title_rect = title.get_rect(center=(center_x, center_y - 30))
        self.display_surface.blit(title, title_rect)

        hint = self.font.render(
            'Press R to restart', False, UI_BORDER_COLOR_ACTIVE
        )
        hint_rect = hint.get_rect(center= (center_x, center_y + 35))
        self.display_surface.blit(hint, hint_rect)
