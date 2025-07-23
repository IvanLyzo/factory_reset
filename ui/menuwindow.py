import pygame
from collections.abc import Callable

import constants
import utils

from ui.window import Window
from ui.element import UIElement


class MenuWindow(Window):

    def __init__(self, offset: int, parent: Window | None = None, custom_pos: pygame.Rect | None = None):
        super().__init__(offset, parent, custom_pos)

        self.text: list[UIElement] = []

        # list of selectable options (with callbacks)
        self.options: list[UIElement] = []
        self.current_option: int = 0

        # selector arrows used to highlight selected option
        self.selector_left: pygame.Surface = utils.load_img("ui/selector_left")
        self.selector_right: pygame.Surface = utils.load_img("ui/selector_right")

    def add_element(self, height: int, text: str, font: pygame.font.Font, callback: Callable[[], None] | None = None):
        rel_pos: tuple[int, int] = (int(self.rect.x + self.rect.width / 2), height + self.rect.y)

        # if no callback provided, this is a non-selectable label
        if callback is None:
            el = UIElement(rel_pos, text.upper(), font)
            self.text.append(el)
        else:
            el = UIElement(rel_pos, text.upper(), font, callback)
            self.options.append(el)
    
    def switch_options(self, dir: int):
        # wrap around when moving past first/last option
        self.current_option = (self.current_option + dir) % len(self.options)

    def select_option(self):
        # call the selected option's callback
        self.options[self.current_option].callback()

    def toggle(self):
        self.active = not self.active
    
    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return

        # move up or down the options list
        if event.key == pygame.K_UP:
            self.switch_options(-1)
        if event.key == pygame.K_DOWN:
            self.switch_options(1)

        # confirm current selection
        if event.key == pygame.K_RETURN:
            self.select_option()
    
    def draw(self, surface: pygame.Surface):
        if not self.active:
            return

        # draw menu background
        pygame.draw.rect(surface, (50, 50, 50), self.rect)

        # draw border if window isn't full screen
        if self.rect.width < constants.VIRTUAL_WIDTH or self.rect.height < constants.VIRTUAL_HEIGHT:
            pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        # draw static text elements
        for el in self.text:
            el.draw(surface)

        # draw selectable options
        for el in self.options:
            el.draw(surface)

        # draw selector arrows around current selection
        if len(self.options) > 0:
            option_rect: pygame.Rect = self.options[self.current_option].text_rect

            surface.blit(self.selector_left, (option_rect.left - 2 * constants.VIRTUAL_TILE, option_rect.center[1] - constants.VIRTUAL_TILE / 2))
            surface.blit(self.selector_right, (option_rect.right + constants.VIRTUAL_TILE, option_rect.center[1] - constants.VIRTUAL_TILE / 2))