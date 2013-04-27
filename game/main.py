import pygame
from pygame.locals import *

import sys

import game.constants as c
import game.modes.swim as swim

import py2d.Math as m

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(c.SCREEN_DIMENSIONS.as_tuple())
        pygame.display.set_caption(c.GAME_TITLE)

        self.running = True
        self.mode = swim.SwimMode(self)
        self.clock = pygame.time.Clock()

        self.mouse_pos = m.Vector(0, 0)

    def loop(self):

        while self.running:

            time_elapsed = self.clock.tick(c.TARGET_FPS)

            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    self.mouse_pos.x = event.pos[0]
                    self.mouse_pos.y = event.pos[1]

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

