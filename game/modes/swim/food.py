import pygame
import game
import game.util as u
import game.constants as c

import py2d.Math as m
import math
import random

import fish


sprite = pygame.image.load("data/images/plankton.png")

class Food(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), nutrition_value=None):
        super(Food, self).__init__(mode, position, direction)

        if nutrition_value == None:
            nutrition_value = random.gammavariate(c.FOOD_NUTRITION_VALUE, c.FOOD_NUTRITION_VALUE_VAR)

        self.nutrition_value = nutrition_value
        self.angle = random.uniform(0, 360)

    def apply_force(self):
        pass

    def update(self, time_elapsed):
        pass

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        spr_zoom = pygame.transform.rotozoom(sprite, self.angle, 0.3 * math.sqrt(self.nutrition_value))
        spr_dim = m.Vector(spr_zoom.get_width(), spr_zoom.get_height())


        scr.blit(spr_zoom, (self.position - cam - spr_dim / 2).as_tuple())

        #u.draw_cross(scr, self.position - cam, color=(255, 255, 0), radius = math.sqrt(self.nutrition_value))
