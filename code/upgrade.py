import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def create_items(self):
        self.item_list = []

        for index in range(self.attribute_nr):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = index * increment + (increment - self.width) // 2
            top = self.display_surface.get_size()[1] * 0.1

            item = Item(
                left, top, self.width, self.height, index, self.font
            )
            self.item_list.append(item)

    def display(self):
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(
                self.display_surface,
                self.selection_index,
                name,
                value,
                max_value,
                cost
            )

class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect( midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        cost_surf = self.font.render(str(int(cost)), False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height

        value_rect = pygame.Rect(
            top[0] - 15,
            bottom[1] - relative_number,
            30,
            10
        )

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def display(self, surface, selection_num, name, value, max_value, cost):
        selected = self.index == selection_num
        color = UPGRADE_BG_COLOR_SELECTED if selected else UI_BG_COLOR

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, selected)
        self.display_bar(surface, value, max_value, selected)