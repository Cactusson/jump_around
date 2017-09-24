import pygame as pg

from .. import tools
from ..components.label import Label
from ..components.button import Button
from ..components.block import Block
from ..components.spikes import SpikeTrap
from ..components.dummy import Dummy
from ..components.background import Background


class Menu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.title = Label(
            'Quicksand-Regular', 90, 'JUMP AROUND', pg.Color('black'),
            center=(self.screen_rect.centerx, 75))
        self.buttons = self.make_buttons()

        self.background = Background(self.screen_rect.width,
                                     self.screen_rect.height)
        self.blocks = self.make_blocks()
        self.spikes = self.make_spikes()
        self.restart_delay = 1500
        self.start()

    def start(self):
        self.frame = 0
        self.dummy = Dummy((50, 400))

    def make_buttons(self):
        """
        There are three buttons in the menu, each has its own call function.
        (their names start with 'button_')
        """
        buttons = pg.sprite.Group()
        play = Button((self.screen_rect.centerx, 175),
                      'PLAY', 'Quicksand-Regular', 50, self.button_play)
        quit = Button((self.screen_rect.centerx, 225),
                      'QUIT', 'Quicksand-Regular', 25, self.button_quit)
        buttons.add(play, quit)
        return buttons

    def button_play(self):
        self.next = 'GAME'
        self.done = True

    def button_quit(self):
        self.quit = True

    def make_blocks(self):
        blocks = [Block((0, 450), 200, 150, True),
                  Block((350, 450), 150, 150, True),
                  Block((650, 450), 150, 150, True),
                  Block((200, 575), 150, 25),
                  Block((500, 575), 150, 25)]
        return pg.sprite.Group(blocks)

    def make_spikes(self):
        spikes_data = [((200, 525), 3),
                       ((500, 525), 3)]
        spikes = [SpikeTrap(*data) for data in spikes_data]
        return pg.sprite.Group(spikes)

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        self.start()

    def cleanup(self):
        self.done = False
        self.dummy = None
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

        for spike_trap in self.spikes:
            spike_trap.draw(self.screen)

        self.dummy.draw(self.screen)

        self.title.draw(self.screen)
        self.buttons.draw(self.screen)

    def update(self, surface, keys, current_time, dt):
        self.frame += 1
        self.current_time = current_time

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

        self.dummy.update(
            self.blocks, self.spikes, self.frame, current_time, dt)
        if self.dummy.state == 'DEAD':
            if current_time - self.dummy.death_time > self.restart_delay:
                self.start()
        self.draw()
