import pygame as pg

from .. import prepare, tools
from ..components.block import Block
from ..components.spikes import SpikeTrap
from ..components.enemies import Enemy, MovingEnemy, Boss
from ..components.jumper import Jumper
from ..components.player import Player
from ..components.finish import Finish
from ..components.background import Background
from ..components.data import levels


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.cover = pg.Surface(self.screen_rect.size).convert()
        self.viewport = self.screen_rect
        self.viewport_speed = 2000
        self.keys = pg.key.get_pressed()
        self.restart_delay = 1500
        self.alpha_step = 7
        self.blocks = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.jumpers = pg.sprite.Group()
        self.boss = None

    def next_level(self):
        if self.level_number < self.total_levels - 1:
            self.level_number += 1
            if self.level_number == 5:
                self.next = 'MESSAGE_SCREEN'
                self.done = True
            else:
                self.start_level()
        else:
            self.next = 'GAMEOVER'
            self.done = True

    def start_level(self):
        """
        Called in the beginning and on every restart.
        """
        self.state = 'START'  # START, PLAY, RESTART, FINISH
        self.cover_alpha = 256
        level = levels[self.level_number]
        self.level = pg.Surface((level['width'], level['height'])).convert()
        self.level_rect = self.level.get_rect()
        if 'cave_y' in level:
            cave_y = level['cave_y']
        else:
            cave_y = None
        self.background = Background(level['width'], level['height'], cave_y)
        self.blocks = self.make_blocks(level['blocks'])
        self.spikes.empty()
        self.enemies.empty()
        self.jumpers.empty()
        self.boss = None
        if 'spikes' in level:
            self.spikes = self.make_spikes(level['spikes'])
        if 'enemies' in level:
            self.enemies = self.make_enemies(level['enemies'],
                                             level['moving_enemies'])
        if 'jumpers' in level:
            self.jumpers = self.make_jumpers(level['jumpers'])
        if 'boss' in level:
            self.boss = Boss(level['boss'])
        self.player = Player(level['start_location'])
        if 'finish_location' in level:
            self.finish = Finish(level['finish_location'])
        else:
            self.finish = None
        self.update_viewport()
        self.viewport_center = self.viewport.center

    def recreate_level(self):
        self.player.kill()
        level = levels[self.level_number]
        start_location = levels[self.level_number]['start_location']
        self.player = Player(start_location)
        if 'enemies' in level:
            self.enemies.empty()
            enemies_data = levels[self.level_number]['enemies']
            moving_enemies_data = levels[self.level_number]['moving_enemies']
            self.enemies = self.make_enemies(enemies_data, moving_enemies_data)
        if 'boss' in level:
            self.boss = Boss(level['boss'])

    def make_blocks(self, blocks_data):
        blocks = [Block(*data) for data in blocks_data]
        return pg.sprite.Group(blocks)

    def make_spikes(self, spikes_data):
        spikes = [SpikeTrap(*data) for data in spikes_data]
        return pg.sprite.Group(spikes)

    def make_enemies(self, enemies_data, moving_enemies_data):
        enemies = [Enemy(data) for data in enemies_data]
        moving_enemies = [MovingEnemy(*data) for data in moving_enemies_data]
        return pg.sprite.Group(enemies, moving_enemies)

    def make_jumpers(self, jumpers_data):
        jumpers = [Jumper(data) for data in jumpers_data]
        return pg.sprite.Group(jumpers)

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        if self.previous == 'MENU':
            self.level_number = 0
            self.music_track = prepare.MUSIC['Fretless']
        elif self.previous == 'MESSAGE_SCREEN':
            self.level_number = 5
            self.music_track = prepare.MUSIC['Baba Yaga']
        self.total_levels = len(levels)
        self.start_level()
        self.frame = 0
        self.play_music(self.music_track)

    def cleanup(self):
        self.stop_music()
        self.done = False
        return self.persist

    def play_music(self, track):
        pg.mixer.music.load(track)
        pg.mixer.music.play()

    def stop_music(self):
        pg.mixer.music.stop()

    def update_viewport(self, start=False):
        """
        The viewport will stay centered on the player unless the player
        approaches the edge of the map.
        """
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def viewport_start_moving_back(self):
        if self.viewport.centerx < self.viewport_center[0]:
            self.viewport_dx = self.viewport_speed
        elif self.viewport.centerx > self.viewport_center[0]:
            self.viewport_dx = -self.viewport_speed
        else:
            self.viewport_dx = 0

        if self.viewport.centery < self.viewport_center[1]:
            self.viewport_dy = self.viewport_speed
        elif self.viewport.centery > self.viewport_center[1]:
            self.viewport_dy = -self.viewport_speed
        else:
            self.viewport_dy = 0

    def move_viewport(self, dt):
        if (abs(self.viewport_center[0] - self.viewport.centerx) <
                abs(self.viewport_center[1] - self.viewport.centery)):
            dx = self.viewport_dx // 2
            dy = self.viewport_dy
        else:
            dx = self.viewport_dx
            dy = self.viewport_dy // 2

        self.viewport.centerx += dx * dt
        if self.viewport_dx > 0:
            if self.viewport.centerx >= self.viewport_center[0]:
                self.viewport_dx = 0
        elif self.viewport_dx < 0:
            if self.viewport.centerx <= self.viewport_center[0]:
                self.viewport_dx = 0

        self.viewport.centery += dy * dt
        if self.viewport_dy > 0:
            if self.viewport.centery >= self.viewport_center[1]:
                self.viewport_dy = 0
        elif self.viewport_dy < 0:
            if self.viewport.centery <= self.viewport_center[1]:
                self.viewport_dy = 0

        self.viewport.clamp_ip(self.level_rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_RETURN:
                self.start_level()
            elif event.key == pg.K_SPACE:
                self.player.die(self.current_time)
            elif event.key == pg.K_h:
                if self.boss:
                    self.boss.create_fireball()
                print(self.player.state_life, self.player.state_y)

    def draw(self):
        # self.level.fill(prepare.BG_COLOR, self.viewport)
        self.level.blit(
            self.background.image, self.viewport.topleft, self.viewport)

        for block in self.blocks:
            if block.rect.colliderect(self.viewport):
                block.draw(self.level)

        for spike_trap in self.spikes:
            if spike_trap.rect.colliderect(self.viewport):
                spike_trap.draw(self.level)

        for enemy in self.enemies:
            if enemy.rect.colliderect(self.viewport):
                enemy.draw(self.level)

        if self.boss:
            self.boss.draw(self.level)

        for jumper in self.jumpers:
            if jumper.rect.colliderect(self.viewport):
                jumper.draw(self.level)

        if self.finish:
            if self.finish.rect.colliderect(self.viewport):
                self.finish.draw(self.level)

        self.player.draw(self.level)

        self.screen.blit(self.level, (0, 0), self.viewport)

        if self.state == 'START' or self.state == 'FINISH':
            self.screen.blit(self.cover, (0, 0))

    def update(self, surface, keys, current_time, dt):
        self.frame += 1
        self.current_time = current_time
        self.keys = keys

        if not pg.mixer.music.get_busy():
            self.play_music(self.music_track)

        if self.state == 'START':
            if self.cover_alpha == 0:
                self.state = 'PLAY'
            else:
                self.cover_alpha = max(self.cover_alpha - self.alpha_step, 0)
                self.cover.set_alpha(self.cover_alpha)

        elif self.state == 'PLAY':
            if self.player.state_life == 'DEAD':
                self.state = 'RESTART_DELAY'
            elif self.finish:
                if self.player.rect.colliderect(self.finish):
                    self.state = 'FINISH'
            elif self.boss:
                if self.boss.state == 'DEAD':
                    self.state = 'FINISH'
            if self.state == 'PLAY':
                self.player.update(
                    self.blocks, self.spikes, self.enemies, self.boss,
                    self.jumpers, keys, current_time, self.frame, dt)
                self.enemies.update(current_time, self.frame, dt)
                if self.boss:
                    self.boss.update(self.player, self.blocks, current_time,
                                     self.frame, dt)
                self.update_viewport()

        elif self.state == 'RESTART_DELAY':
            if current_time - self.player.death_time > self.restart_delay:
                self.viewport_start_moving_back()
                self.state = 'RESTART'
            else:
                self.player.update(
                    self.blocks, self.spikes, self.enemies, self.boss,
                    self.jumpers, keys, current_time, self.frame, dt)
                self.enemies.update(current_time, self.frame, dt)
                if self.boss:
                    self.boss.update(self.player, self.blocks, current_time,
                                     self.frame, dt)
                self.update_viewport()

        elif self.state == 'RESTART':
            # if self.viewport.collidepoint(self.viewport_center):
            if self.viewport_dx == 0 and self.viewport_dy == 0:
                self.state = 'PLAY'
                self.recreate_level()
            else:
                self.move_viewport(dt)

        elif self.state == 'FINISH':
            if self.cover_alpha == 256:
                self.next_level()
            else:
                self.cover_alpha = min(self.cover_alpha + self.alpha_step, 256)
                self.cover.set_alpha(self.cover_alpha)

        self.draw()
