import pygame

# TODO: make all imports like this to call through class (reads way easier)
import constants
import utils

from ui.element import UIElement

class Window:

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.visible = False

        self.text = []
        self.options = []
        self.current_option = 0

        self.selector_left = utils.load_img("ui/selector_left")
        self.selector_right = utils.load_img("ui/selector_right")

    def add_element(self, height, text, font, callback=None):
        rel_pos = (self.rect.x + self.rect.width / 2, height + self.rect.y)

        if callback == None:
            el = UIElement(rel_pos, text.upper(), font)
            self.text.append(el)
        else:
            el = UIElement(rel_pos, text.upper(), font, callback)
            self.options.append(el)
    
    def switch_options(self, dir):
        if not self.visible:
            return

        self.current_option = (self.current_option + dir) % len(self.options)

    def select_option(self):
        if not self.visible:
            return

        self.options[self.current_option].callback()

    def toggle(self):
        self.visible = not self.visible
    
    def draw(self, surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        for el in self.text:
            el.draw(surface)
        for el in self.options:
            el.draw(surface)

        option_rect = self.options[self.current_option].text_rect

        surface.blit(self.selector_left, (option_rect.left - 2 * constants.VIRTUAL_TILE, option_rect.center[1] - constants.VIRTUAL_TILE / 2))
        surface.blit(self.selector_right, (option_rect.right + constants.VIRTUAL_TILE, option_rect.center[1] - constants.VIRTUAL_TILE / 2))