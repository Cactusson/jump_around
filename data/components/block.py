import pygame as pg

from .. import prepare


class Block(pg.sprite.Sprite):
    def __init__(self, location, width, height, green=False):
        pg.sprite.Sprite.__init__(self)
        self.brown_tile = prepare.GFX['ground']['dirt']
        self.green_tile = prepare.GFX['ground']['grass_big']
        self.green_tile_small = prepare.GFX['ground']['grass_small']
        if green:
            image = pg.Surface((width, height)).convert()
            green_part = self.make_green_image(width)
            brown_part = self.make_brown_image(width, height - 50)
            image.blit(green_part, (0, 0))
            image.blit(brown_part, (0, 50))
            self.image = image
        else:
            self.image = self.make_brown_image(width, height)
        self.rect = self.image.get_rect(topleft=location)

    def make_green_image(self, width):
        height = 50
        surface = pg.Surface((width, height)).convert()
        for i in range(0, width, 50):
            surface.blit(self.green_tile, (i, 0))
        if width % 50 != 0:
            surface.blit(self.green_tile_small, (width - 25, 0))
        return surface

    def make_brown_image(self, width, height):
        surface = pg.Surface((width, height)).convert()
        for i in range(0, width, 25):
            for j in range(0, height, 25):
                surface.blit(self.brown_tile, (i, j))
        return surface

    def draw(self, surface):
        surface.blit(self.image, self.rect)
