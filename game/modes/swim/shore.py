import pygame

import game
import game.constants as c
import py2d.Math as m

class Shore(game.Entity):

    def __init__(self, mode, position, color):
        super(Shore, self).__init__(mode, position, m.Vector(0, 0))
        self.color = color

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        pygame.draw.rect(scr, self.color, ((self.position - cam).as_tuple(), c.SECTOR_SIZE.as_tuple()))

