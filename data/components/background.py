import pygame as pg

from .. import prepare


class Background(pg.sprite.Sprite):
    def __init__(self, width, height, cave_y=None):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image(width, height, cave_y)
        self.rect = self.image.get_rect(topleft=(0, 0))

    def make_ground(self, width, height):
        bg = prepare.GFX['misc']['bg']
        bg_top = prepare.GFX['misc']['bg_top']
        image = pg.Surface((width, height)).convert()
        for i in range(width // bg.get_width() + 1):
            image.blit(bg, (bg.get_width() * i, height - bg.get_height()))
            for j in range((height - bg.get_height()) //
                           bg_top.get_height() + 1):
                image.blit(
                    bg_top,
                    (bg.get_width() * i,
                     height - bg.get_height() - bg_top.get_height() * (j + 1)))
        return image

    def make_cave(self, width, height):
        cave = prepare.GFX['misc']['cave']
        image = pg.Surface((width, height)).convert()
        for i in range(width // cave.get_width() + 1):
            image.blit(cave, (cave.get_width() * i, 0))
        return image

    def make_image(self, width, height, cave_y=None):
        image = pg.Surface((width, height)).convert()
        if cave_y is not None:
            ground = self.make_ground(width, cave_y)
            cave = self.make_cave(width, height - cave_y)
            image.blit(ground, (0, 0))
            image.blit(cave, (0, cave_y))
        else:
            ground = self.make_ground(width, height)
            image.blit(ground, (0, 0))
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
