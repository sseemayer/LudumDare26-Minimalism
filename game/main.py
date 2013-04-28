import pygame
from pygame.locals import *

import sys
import collections

import game
import game.constants as c

import game.modes.menu.mode

import py2d.Math as m

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(c.SCREEN_DIMENSIONS.as_tuple())
        pygame.display.set_caption(c.GAME_TITLE)
        pygame.mouse.set_visible(False)

        self.running = True
        self.mode = game.modes.menu.mode.MenuMode(self)

        self.clock = pygame.time.Clock()

        self.mouse_pos = m.Vector(0, 0)

        self.keys = collections.defaultdict(bool)

    def die(self, swim_mode):
        self.mode = game.modes.death.mode.DeathMode(self, swim_mode)

    def loop(self):

        while self.running:

            time_elapsed = self.clock.tick(c.TARGET_FPS)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.keys[event.key] = True

                if event.type == KEYUP:
                    self.keys[event.key] = False

                if event.type == MOUSEMOTION:
                    self.mouse_pos.x = event.pos[0]
                    self.mouse_pos.y = event.pos[1]

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.mode:
                        self.mode.click()

                if event.type == QUIT:
                    self.running = False

            if self.mode:
                self.mode.update(time_elapsed)
                self.mode.render()

            pygame.display.update()

        pygame.quit()
        sys.exit()


def run():
    Game().loop()

