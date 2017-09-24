import pygame as pg

from .. import prepare


class Jumper(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['misc']['spring']
        self.rect = self.image.get_rect(topleft=location)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
