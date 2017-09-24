import pygame as pg

from .. import tools
from ..components.label import Label


class MessageScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        message = 'Get ready to meet The Boss!'
        self.title = Label('Quicksand-Regular', 35, message,
                           pg.Color('white'),
                           center=(self.screen_rect.centerx,
                                   self.screen_rect.centery))
        self.time_waiting = 2500

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

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.title.draw(self.screen)

    def update(self, surface, keys, current_time, dt):
        if current_time - self.start_time > self.time_waiting:
            self.next = 'GAME'
            self.done = True
        else:
            self.draw()
