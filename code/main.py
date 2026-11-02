import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):

        # general setup

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('AlikeZelda')
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.started = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not self.started:
                        if event.key == pygame.K_RETURN:
                            self.started = True
                    elif self.level.game_over or self.level.game_won:
                        if event.key == pygame.K_r:
                            self.level = Level()
                    elif event.key == pygame.K_TAB:
                        self.level.toggle_map()
                    elif event.key == pygame.K_m:
                        self.level.toggle_menu()
                    elif event.key == pygame.K_f:
                        self.level.interact()

            self.screen.fill('black')

            if self.started:
                self.level.run()
            else:
                self.level.visible_sprites.custom_draw(self.level.player)
                self.level.ui.show_title()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
