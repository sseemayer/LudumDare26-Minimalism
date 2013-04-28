import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m
import math
import random

import fish



class Food(game.PhysicsEntity):

    sprites = None

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), nutrition_value=None):
        super(Food, self).__init__(mode, position, direction)

        if not Food.sprites:
            Food.sprites = [pygame.image.load("data/images/plankton_{}.png".format(i)).convert_alpha() for i in range(2)]

        if nutrition_value == None:
            nutrition_value = random.gammavariate(c.FOOD_NUTRITION_VALUE, c.FOOD_NUTRITION_VALUE_VAR)

        self.color = u.random_hue(h_min=80, h_max=270)
        self.nutrition_value = nutrition_value
        self.angle = random.uniform(0, 360)
        self.which = random.choice(range(len(Food.sprites)))

    def apply_force(self):
        pass

    def update(self, time_elapsed):
        pass

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        spr_zoom = pygame.transform.rotozoom(Food.sprites[self.which], self.angle, 0.3 * math.sqrt(self.nutrition_value))
        spr_zoom.fill(self.color, special_flags=BLEND_MULT)

        spr_dim = m.Vector(spr_zoom.get_width(), spr_zoom.get_height())



        scr.blit(spr_zoom, (self.position - cam - spr_dim / 2).as_tuple())

        #u.draw_cross(scr, self.position - cam, color=(255, 255, 0), radius = math.sqrt(self.nutrition_value))
