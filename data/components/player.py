import pygame as pg

from .. import prepare


class Player(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)

        self.image_stand_left = prepare.GFX['player']['player_stand']
        self.image_stand_right = pg.transform.flip(
            self.image_stand_left, True, False)
        self.image_index = 0
        self.direction = 'right'

        self.images_appear_left = [
            prepare.GFX['player']['appear_{}'.format(i)]
            for i in range(10)]
        self.images_appear_right = [pg.transform.flip(image, True, False)
                                    for image in self.images_appear_left]

        self.images_walk_left = [
            prepare.GFX['player']['player_walk_{}'.format(i)]
            for i in range(8)]
        self.images_walk_right = [pg.transform.flip(image, True, False)
                                  for image in self.images_walk_left]

        self.images_die_left = [
            prepare.GFX['player']['dead_{}'.format(i)] for i in range(8)]
        self.images_die_right = [pg.transform.flip(image, True, False)
                                 for image in self.images_die_left]

        self.image = self.images_appear_right[0]
        self.rect = self.image.get_rect(topleft=location)

        self.x_vel = self.y_vel = 0
        self.grav = 50
        self.speed = 550
        self.jump_power = -1250
        self.jump_after_hit_enemy_power = -800
        self.jump_on_jumper_power = -2000
        self.jump_cut_magnitude = -500

        # GROUND / JUMP /  JUMP_HIT / FALL
        self.state_y = 'GROUND'
        # APPEAR / ALIVE / DEAD
        self.state_life = 'APPEAR'

    def check_keys(self, keys):
        self.x_vel = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.x_vel = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x_vel = self.speed
        if (keys[pg.K_UP] or keys[pg.K_w]) and self.state_y == 'GROUND':
            self.jump()
        if not (keys[pg.K_UP] or keys[pg.K_w]) and self.state_y == 'JUMP':
            self.jump_cut()
        # if keys[pg.K_SPACE]:
        #     print(self.state_y)

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

        elif self.state_y == 'JUMP' or self.state_y == 'JUMP_HIT':
            if (self.check_collisions('top', obstacles) or
                    self.y_vel > 0):
                self.state_y = 'FALL'
                if self.y_vel < 0:
                    self.y_vel = 0
            else:
                self.change_position((0, self.y_vel), 1, obstacles, dt)

        if self.x_vel:
            self.change_position((self.x_vel, 0), 0, obstacles, dt)

    def check_spikes(self, spikes, now):
        if self.state_life == 'ALIVE':
            if self.check_collisions('bottom', spikes):
                self.die(now)

    def check_enemies(self, enemies, now):
        if (self.check_collisions('left', enemies) or
                self.check_collisions('right', enemies) or
                self.check_collisions('top', enemies)):
            self.die(now)

        if self.state_y == 'GROUND':
            if self.check_collisions('bottom', enemies):
                killed_enemies = self.check_collisions(
                    'bottom', enemies)
                self.kill_enemies(killed_enemies)

    def kill_enemies(self, enemies):
        for enemy in enemies:
            enemy.die()
        self.jump_after_hit_enemy()

    def check_boss(self, boss, now):
        boss_group = pg.sprite.Group(boss)
        if (self.check_collisions('left', boss_group) or
                self.check_collisions('right', boss_group) or
                self.check_collisions('top', boss_group)):
            self.die(now)

        if self.state_y == 'GROUND':
            if self.check_collisions('bottom', boss_group):
                if boss.state == 'NORMAL':
                    boss.get_angry(now)
                    self.jump_after_hit_enemy()
                elif boss.state == 'ANGRY':
                    self.die(now)

    def check_fireballs(self, fireballs, now):
        if (self.check_collisions('left', fireballs) or
                self.check_collisions('right', fireballs) or
                self.check_collisions('top', fireballs) or
                self.check_collisions('bottom', fireballs)):
            fireballs_collided = pg.sprite.Group()
            fireballs_collided.add(self.check_collisions('left', fireballs))
            fireballs_collided.add(self.check_collisions('right', fireballs))
            fireballs_collided.add(self.check_collisions('top', fireballs))
            fireballs_collided.add(self.check_collisions('bottom', fireballs))
            for fireball in fireballs_collided:
                fireball.die()
            self.die(now)

    def check_jumpers(self, jumpers):
        if self.state_y == 'GROUND':
            if self.check_collisions('bottom', jumpers):
                self.jump_on_jumper()

    def check_position_to_boss(self, boss):
        if self.state_y == 'FALL' and boss.speed > 0:
            if self.check_collisions('bottom', pg.sprite.Group(boss)):
                self.state_y = 'GROUND'

    def update_image(self, frame):
        if self.state_life == 'APPEAR':
            if frame % 4 == 0:
                if self.direction == 'right':
                    self.image = self.images_appear_right[self.image_index]
                else:
                    self.image = self.images_appear_left[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_appear_right):
                    self.state_life = 'ALIVE'
                    self.image_index = 0
        elif self.state_life == 'DEAD':
            if frame % 4 == 0:
                if self.direction == 'right':
                    self.image = self.images_die_right[self.image_index]
                else:
                    self.image = self.images_die_left[self.image_index]
                self.image_index += 1
                if self.image_index >= len(self.images_die_right):
                    self.image_index = len(self.images_die_right) - 1
        elif self.state_life == 'ALIVE':
            if self.x_vel == 0:
                self.image_index = 0
                if self.direction == 'right':
                    self.image = self.image_stand_right
                else:
                    self.image = self.image_stand_left
            else:
                if self.x_vel > 0:
                    self.direction = 'right'
                else:
                    self.direction = 'left'
                if frame % 4 == 0:
                    if self.direction == 'right':
                        self.image = self.images_walk_right[self.image_index]
                    else:
                        self.image = self.images_walk_left[self.image_index]
                    self.image_index += 1
                    if self.image_index >= len(self.images_walk_right):
                        self.image_index = 0

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

    def jump(self):
        """
        Called when the user presses the jump key.
        """
        self.state_y = 'JUMP'
        self.y_vel = self.jump_power

    def jump_after_hit_enemy(self):
        self.state_y = 'JUMP_HIT'
        self.y_vel = self.jump_after_hit_enemy_power

    def jump_on_jumper(self):
        self.state_y = 'JUMP_HIT'
        self.y_vel = self.jump_on_jumper_power

    def jump_cut(self):
        """
        Called if player releases the jump key before maximum height.
        """
        if self.y_vel < self.jump_cut_magnitude:
            self.y_vel = self.jump_cut_magnitude

    def die(self, now):
        self.x_vel = 0
        self.state_life = 'DEAD'
        self.death_time = now
        self.image_index = 0

    def update(self, blocks, spikes, enemies, boss,
               jumpers, keys, now, frame, dt):
        """
        Every frame we check keys, update player's position accordingly to
        its velocity and make a gravity update.
        """
        alive_enemies = pg.sprite.Group()
        for enemy in enemies:
            if enemy.state is not 'DEAD':
                alive_enemies.add(enemy)
        obstacles = pg.sprite.Group(blocks, spikes, alive_enemies, jumpers)
        if boss:
            obstacles.add(boss)
            obstacles.add(boss.fireballs)
        if self.state_life == 'ALIVE':
            self.check_keys(keys)
        self.update_position(obstacles, dt)
        if boss:
            self.check_position_to_boss(boss)
        self.update_image(frame)
        if self.state_life == 'ALIVE':
            self.check_spikes(spikes, now)
            self.check_enemies(alive_enemies, now)
            if boss:
                self.check_boss(boss, now)
                self.check_fireballs(boss.fireballs, now)
            self.check_jumpers(jumpers)
        self.gravity_update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
