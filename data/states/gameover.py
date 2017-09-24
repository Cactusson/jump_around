import pygame as pg

from .. import tools
from ..components.label import Label
from ..components.button import Button
from ..components.block import Block
from ..components.background import Background


class GameOver(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.title = Label('Quicksand-Regular', 75, "That's it",
                           pg.Color('black'),
                           center=(self.screen_rect.centerx, 125))
        self.buttons = self.make_buttons()
        self.background = Background(self.screen_rect.width,
                                     self.screen_rect.height)
        self.blocks = self.make_blocks()

    def make_buttons(self):
        buttons = pg.sprite.Group()
        ok = Button((self.screen_rect.centerx, 225),
                    'OK', 'Quicksand-Regular', 25, self.button_ok)
        buttons.add(ok)
        return buttons

    def button_ok(self):
        self.next = 'MENU'
        self.done = True

    def make_blocks(self):
        blocks = [Block((0, 475), 800, 125, True)]
        return pg.sprite.Group(blocks)

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click()

    def draw(self):
        self.screen.blit(self.background.image, (0, 0))

        for block in self.blocks:
            block.draw(self.screen)

        self.title.draw(self.screen)
        self.buttons.draw(self.screen)

    def update(self, surface, keys, current_time, dt):
        self.current_time = current_time

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

        self.draw()
