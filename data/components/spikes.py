import pygame as pg

from .. import prepare


class SpikeTrap(pg.sprite.Sprite):
    def __init__(self, location, amount):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image(amount)
        self.rect = self.image.get_rect(topleft=location)

    def make_image(self, amount):
        """
        Not absolutely sure why this works as intended
        (joining images with transparent backgrounds).
        """
        picture = prepare.GFX['misc']['spikes']
        image = pg.Surface((50 * amount, 50)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        for i in range(amount):
            image.blit(picture, (50 * i, 0))
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
