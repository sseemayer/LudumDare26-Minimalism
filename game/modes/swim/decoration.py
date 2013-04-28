import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m
import math
import random



class Decoration(game.Entity):

    sprites = None

    def __init__(self, mode, which, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Decoration, self).__init__(mode, position, direction)

        if not Decoration.sprites:
            Decoration.sprites = [ pygame.image.load("data/images/depth_{}.png".format(i)).convert_alpha() for i in range(7) ]
            for s in Decoration.sprites:
                s.fill((0,0,50), special_flags=BLEND_MULT)


        self.which = which % len(Decoration.sprites)

    def apply_force(self):
        pass

    def update(self, time_elapsed):
        pass

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        spr_zoom = Decoration.sprites[self.which]

        spr_dim = m.Vector(spr_zoom.get_width(), spr_zoom.get_height())

        scr.blit(spr_zoom, (self.position - cam - spr_dim / 2).as_tuple())

        #u.draw_cross(scr, self.position - cam, color=(255, 255, 0), radius = math.sqrt(self.nutrition_value))



