import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m
import math
import random


class Trawl(game.Entity):

    killzone = m.Polygon.from_tuples([
        (-210, -1340),
        (-120, -1380),
        (-120, 1380),
        (-210, 1340),
        (-230, 1020),
        (-250, 0),
        (-230, -1020)
    ])

    sprite = None

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(1, 0)):
        super(Trawl, self).__init__(mode, position, direction.normalize())

        if not Trawl.sprite:
            Trawl.sprite = pygame.image.load("data/images/trawl.png").convert_alpha()

        self.angle = math.atan2(self.direction.y, self.direction.x)
        print(self.angle)

        self.sprite = pygame.transform.rotozoom(Trawl.sprite, -self.angle / math.pi * 180, 1)
        self.sprite_size = m.Vector(self.sprite.get_width(), self.sprite.get_height())

        self.transform = m.Transform.rotate(self.angle)

    def apply_force(self):
        pass

    def update(self, time_elapsed):
        self.position += self.direction * c.TRAWL_SPEED * time_elapsed

        kill_zone = self.transform * Trawl.killzone

        for p in self.mode.predators:
            if kill_zone.contains_point(p.position - self.position):
                self.mode.game.audio.play("hurt")
                self.mode.predators.remove(p)

        for f in self.mode.foods:
            if kill_zone.contains_point(f.position - self.position):
                self.mode.game.audio.play("eat")
                self.mode.foods.remove(f)

        for f in self.mode.swarm.fishes:
            if kill_zone.contains_point(f.position - self.position) and f.food >= c.TRAWL_SIZE_THRESHOLD and self.mode.swarm.swarm_mode != 1:
                self.mode.game.audio.play("hurt")
                self.mode.swarm.fishes.remove(f)

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        scr.blit(self.sprite, (self.position - cam - self.sprite_size / 2).as_tuple())

        #kz_points = [ self.transform * p + self.position - cam for p in Trawl.killzone.points ]
        #pygame.draw.polygon(scr, (255,0,0), [p.as_tuple() for p in kz_points])
