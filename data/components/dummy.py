import pygame as pg

from .. import prepare


class Dummy(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)

        self.images_appear = [
                pg.transform.flip(image, True, False)
                for image in [prepare.GFX['player']['appear_{}'.format(i)]
                              for i in range(10)]]
        self.images_walk = [
                pg.transform.flip(image, True, False)
                for image in [prepare.GFX['player']['player_walk_{}'.format(i)]
                              for i in range(8)]]
        self.images_die = [
                pg.transform.flip(image, True, False)
                for image in [prepare.GFX['player']['dead_{}'.format(i)]
                              for i in range(8)]]
        self.image_index = 0

        self.image = self.images_appear[0]
        self.rect = self.image.get_rect(topleft=location)
        self.state = 'APPEAR'
        self.state_y = 'GROUND'
        self.x_vel = 0
        self.y_vel = 0
        self.grav = 50
        self.death_time = 0.0

        self.triggers = [(200, self.set_vel, 350, -800),
                         (500, self.set_vel, 300, -600), ]

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel
        if self.y_vel < 0:
            self.state_y = 'JUMP'

    def awake(self):
        self.state = 'ALIVE'
        self.x_vel = 300

    def update_position(self, obstacles, dt):
        """
        Update player's position and correct it if it's collided with
        obstacles.
        """
        if self.state_y == 'GROUND':
            if not self.check_collisions('bottom', obstacles):
                self.state_y = 'FALL'

        elif self.state_y == 'FALL':
            if self.check_collisions('bottom', obstacles):
                self.state_y = 'GROUND'
            else:
                self.change_position((0, self.y_vel), 1, obstacles, dt)

        elif self.state_y == 'JUMP':
            if self.y_vel > 0:
                self.state_y = 'FALL'
            else:
                self.change_position((0, self.y_vel), 1, obstacles, dt)

        if self.x_vel:
            self.change_position((self.x_vel, 0), 0, obstacles, dt)

    def change_position(self, offset, index, obstacles, dt):
        """
        This function checks if a collision would occur after moving offset
        pixels. If a collision is detected, the position is decremented by one
        pixel and retested. This continues until we find exactly how far we can
        safely move, or we decide we can't move.
        """
        self.rect[index] += offset[index] * dt
        while pg.sprite.spritecollideany(self, obstacles):
            self.rect[index] += (1 if offset[index] < 0 else -1)

    def check_collisions(self, side, obstacles):
        offset = {'left': ((-1, 0), (1, 0)),
                  'right': ((1, 0), (-1, 0)),
                  'top': ((0, -1), (0, 1)),
                  'bottom': ((0, 1), (0, -1))}[side]
        self.rect.move_ip(*offset[0])
        collide = pg.sprite.spritecollide(self, obstacles, False)
        self.rect.move_ip(*offset[1])
        return collide

    def gravity_update(self):
        """
        If player is in the air, add a little to their y_vel so they
        are pulled back to the ground.
        """
        if (self.state_y == 'JUMP' or
                self.state_y == 'JUMP_HIT' or
                self.state_y == 'FALL'):
            self.y_vel += self.grav
        else:
            self.y_vel = 0

    def check_spikes(self, spikes, now):
        if self.check_collisions('bottom', spikes):
            self.die(now)

    def die(self, now):
        self.x_vel = 0
        self.state = 'DEAD'
        self.death_time = now
        self.image_index = 0

    def update_image(self, frame):
        if self.state == 'APPEAR':
            if frame % 4 == 0:
                self.image = self.images_appear[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_appear):
                    self.image_index = 0
                    self.awake()
        elif self.state == 'ALIVE':
            if frame % 4 == 0:
                self.image = self.images_walk[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_walk):
                    self.image_index = 0
        elif self.state == 'DEAD':
            if frame % 4 == 0:
                self.image = self.images_die[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_die):
                    self.image_index = len(self.images_die) - 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, blocks, spikes, frame, now, dt):
        obstacles = pg.sprite.Group(blocks, spikes)
        self.update_position(obstacles, dt)
        self.update_image(frame)
        if self.state == 'ALIVE':
            self.check_spikes(spikes, now)
        self.gravity_update()
        for trigger in self.triggers:
            point, event, x_vel, y_vel = trigger
            if self.rect.right >= point:
                event(x_vel, y_vel)
                self.triggers.remove(trigger)
