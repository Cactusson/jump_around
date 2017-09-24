import pygame as pg
import random

from .. import prepare


class Enemy(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image_stand_left = prepare.GFX['enemies']['stand']
        self.image_stand_right = pg.transform.flip(
            self.image_stand_left, True, False)
        self.images_die = [
            prepare.GFX['enemies']['boom_{}'.format(i)]
            for i in range(7)]
        self.direction = 'RIGHT'
        self.state = 'STAND'
        self.image = self.image_stand_left
        self.rect = self.image.get_rect(topleft=location)

    def die(self):
        prepare.SFX['explosion'].play()
        self.image_index = 0
        self.state = 'DEAD'

    def update_dying(self, frame):
        if self.image_index >= len(self.images_die):
            self.kill()
        else:
            if frame % 4 == 0:
                self.image = self.images_die[self.image_index]
                self.image_index += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, now, frame, dt):
        if self.state == 'DEAD':
            self.update_dying(frame)


class MovingEnemy(Enemy):
    def __init__(self, location, end):
        Enemy.__init__(self, location)
        self.images_walk_left = [
            prepare.GFX['enemies']['walk_{}'.format(i)]
            for i in range(10)]
        self.images_walk_right = [pg.transform.flip(image, True, False)
                                  for image in self.images_walk_left]
        self.image_index = 0
        self.start = location[0]
        self.end = end
        self.speed = 350
        self.x_vel = self.speed
        self.state = 'MOVE'
        self.standing_time = 0.0
        self.standing_delay = 1000

    def update_image(self, frame):
        if self.state == 'STAND':
            self.image_index = 0
            if self.direction == 'RIGHT':
                self.image = self.image_stand_right
            else:
                self.image = self.image_stand_left
        elif self.state == 'MOVE':
            if frame % 4 == 0:
                if self.direction == 'RIGHT':
                    self.image = self.images_walk_right[self.image_index]
                else:
                    self.image = self.images_walk_left[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_walk_right):
                    self.image_index = 0

    def change_position(self, now, dt):
        """
        This function checks if a collision would occur after moving offset
        pixels. If a collision is detected, the position is decremented by one
        pixel and retested. This continues until we find exactly how far we can
        safely move, or we decide we can't move.
        """
        self.rect.x += self.x_vel * dt
        if self.direction == 'RIGHT':
            if self.rect.x >= self.end:
                self.rect.x = self.end
                self.state = 'STAND'
                self.standing_time = now
        elif self.direction == 'LEFT':
            if self.rect.x <= self.start:
                self.rect.x = self.start
                self.state = 'STAND'
                self.standing_time = now

    def change_direction(self):
        if self.direction == 'RIGHT':
            self.direction = 'LEFT'
        elif self.direction == 'LEFT':
            self.direction = 'RIGHT'
        self.x_vel *= -1

    def update(self, now, frame, dt):
        if self.state == 'MOVE':
            self.change_position(now, dt)
            self.update_image(frame)
        elif self.state == 'STAND':
            if now - self.standing_time > self.standing_delay:
                self.change_direction()
                self.state = 'MOVE'
            self.update_image(frame)
        elif self.state == 'DEAD':
            self.update_dying(frame)


class Boss(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        # self.normal_image = pg.Surface((150, 150)).convert()
        # self.normal_image.fill(pg.Color('green'))
        self.normal_image = prepare.GFX['enemies']['boss_normal']
        # self.hurt_image = pg.Surface((150, 150)).convert()
        # self.hurt_image.fill(pg.Color('red'))
        self.hurt_image = prepare.GFX['enemies']['boss_hurt']
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=location)
        self.hp = 5
        self.hp_bar = HPBar()
        self.state = 'NORMAL'  # NORMAL, ANGRY, DEAD
        self.angry_time = 1500
        self.cooldown = 2000
        self.cooldown_reduction = 250
        self.shot_timestamp = 0.0
        self.dead_time = 3000
        self.dead_timestamp = 0.0
        self.explosion_cooldown = 250
        self.explosion_timestamp = 0.0
        self.bounce_speed = 200
        self.start_x = self.rect.x
        self.max_bounce_left = self.rect.x - 20
        self.max_bounce_right = self.rect.x + 20
        self.speed = 100
        self.fall_speed = 400
        self.fireballs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()

    def get_angry(self, now):
        self.hp -= 1
        self.hp_bar.update(self.hp)
        self.cooldown -= self.cooldown_reduction
        if self.hp <= 0:
            self.start_falling()
        else:
            self.state = 'ANGRY'
            self.image = self.hurt_image
            self.angry_timestamp = now

    def back_to_normal(self):
        self.state = 'NORMAL'
        self.image = self.normal_image

    def start_falling(self):
        self.state = 'FALL'
        self.image = self.hurt_image
        self.speed = self.fall_speed

    def die(self, now):
        self.dead_timestamp = now
        self.state = 'DYING'

    def shoot_if_loaded(self, now):
        if now - self.shot_timestamp > self.cooldown:
            self.create_fireball()
            self.shot_timestamp = now

    def create_fireball(self):
        self.fireballs.add(Fireball(self.rect.midleft))

    def create_explosion(self, now):
        self.explosion_timestamp = now
        x = random.randint(self.rect.left, self.rect.right - 30)
        y = random.randint(self.rect.top, self.rect.bottom - 50)
        self.explosions.add(Explosion((x, y)))

    def check_bottom(self, obstacles):
        offset = ((0, 1), (0, -1))
        self.rect.move_ip(*offset[0])
        collide = pg.sprite.spritecollide(self, obstacles, False)
        self.rect.move_ip(*offset[1])
        return collide

    def bounce(self, dt):
        self.rect.x += self.bounce_speed * dt
        if (self.bounce_speed < 0 and self.rect.x < self.max_bounce_left or
                self.bounce_speed > 0 and self.rect.x > self.max_bounce_right):
            self.bounce_speed *= -1

    def bounce_back(self, dt):
        self.rect.x += self.bounce_speed * dt
        if (self.bounce_speed < 0 and self.rect.x < self.start_x or
                self.bounce_speed > 0 and self.rect.x > self.start_x):
            self.bounce_speed *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for fireball in self.fireballs:
            fireball.draw(surface)
        for explosion in self.explosions:
            explosion.draw(surface)
        self.hp_bar.draw(surface)

    def update(self, player, blocks, now, frame, dt):
        if self.state == 'DYING':
            if now - self.dead_timestamp > self.dead_time:
                self.state = 'DEAD'
            else:
                if now - self.explosion_cooldown > self.explosion_timestamp:
                    self.create_explosion(now)
        else:
            if self.state == 'FALL':
                if self.check_bottom(blocks):
                    self.die(now)
            else:
                if self.state == 'ANGRY':
                    self.bounce(dt)
                    if now - self.angry_timestamp > self.angry_time:
                        self.back_to_normal()
                else:
                    if self.rect.x != self.start_x:
                        self.bounce_back(dt)
                self.shoot_if_loaded(now)
                if (self.speed < 0 and self.rect.centery <= 100 or
                        self.speed > 0 and self.rect.centery >= 400):
                    self.speed *= -1
            delta = self.speed * dt
            if delta < 0:
                delta += 1
            self.rect.y += delta
            while pg.sprite.spritecollideany(self, pg.sprite.Group(player)):
                self.rect.y += (1 if self.speed < 0 else -1)

        self.fireballs.update(blocks, now, frame, dt)
        self.explosions.update(frame)


class Fireball(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.images = [prepare.GFX['enemies']['fireball_{}'.format(i)]
                       for i in range(1, 6)]
        self.images_die = [prepare.GFX['enemies']['fireball_die_{}'.format(i)]
                           for i in range(1, 7)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(midright=location)
        self.speed = -500
        self.state = 'ALIVE'

    def die(self):
        self.image_index = 0
        self.state = 'DEAD'

    def update_dying(self, frame):
        if self.image_index >= len(self.images_die):
            self.kill()
        else:
            if frame % 4 == 0:
                self.image = self.images_die[self.image_index]
                self.image_index += 1

    def check_left(self, obstacles):
        offset = ((-1, 0), (1, 0))
        self.rect.move_ip(*offset[0])
        collide = pg.sprite.spritecollide(self, obstacles, False)
        self.rect.move_ip(*offset[1])
        return collide

    def update_image(self, frame):
        if frame % 4 == 0:
            self.image = self.images[self.image_index]
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, blocks, now, frame, dt):
        if self.state == 'DEAD':
            self.update_dying(frame)
        elif self.state == 'ALIVE':
            self.update_image(frame)
            if self.check_left(blocks):
                self.die()
            self.rect.x += self.speed * dt


class Explosion(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.images = [
            prepare.GFX['enemies']['boom_{}'.format(i)]
            for i in range(7)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=location)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, frame):
        if self.image == self.images[-1]:
            self.kill()
        elif frame % 4 == 0:
            self.image = self.images[self.images.index(self.image) + 1]


class HPBar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        location = (265, 540)
        hp = 5
        self.image = self.make_image(hp)
        self.rect = self.image.get_rect(topleft=location)

    def make_image(self, hp):
        picture_width = 45
        picture_height = 45
        bar_width = 35 * 5
        bar_height = 35
        frame_width = 2
        width = picture_width + bar_width + frame_width * 2
        height = picture_height + bar_height + frame_width * 2

        image = pg.Surface((width, height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()

        frame = pg.Surface((width, height)).convert()
        frame.set_alpha(0)
        frame = frame.convert_alpha()

        frame_square = pg.Surface((picture_width + frame_width * 2,
                                   picture_height + frame_width * 2))
        frame_square.fill(pg.Color('white'))
        frame.blit(frame_square, (0, 0))

        frame_rect = pg.Surface((bar_width + frame_width,
                                 bar_height + frame_width * 2))
        frame_rect.fill(pg.Color('white'))
        frame.blit(frame_rect, (picture_width + frame_width,
                                picture_height - bar_height))

        image.blit(frame, (0, 0))

        picture = prepare.GFX['enemies']['boss_picture']
        image.blit(picture, (frame_width, frame_width))

        for i in range(5):
            point = pg.Surface((bar_height, bar_height)).convert()
            if i + 1 <= hp:
                point.fill(pg.Color('red'))
            else:
                point.fill(pg.Color('black'))
            image.blit(point, (picture_width + i * bar_height + frame_width,
                               picture_height - bar_height + frame_width))

        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, hp):
        self.image = self.make_image(hp)
