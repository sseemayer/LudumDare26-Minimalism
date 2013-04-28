import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m

import fish

class Swarm(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), initial_fishes=c.START_FISHES, fish_radius=100):
        super(Swarm, self).__init__(mode, position, direction, max_velocity=c.SWARM_MAX_VELOCITY, velocity_decay=c.SWARM_VELOCITY_DECAY)

        self.target_position = position
        self.last_pos = position

        self.fishes = [fish.Fish(self, position +  u.random_dir() * fish_radius, u.random_dir()) for _ in range(initial_fishes)]

        self.swarm_mode = 0
        self.maneuver_energy = c.SWARM_MANEUVER_ENERGY_MAX

    def apply_force(self):
        self.acceleration += (self.target_position - self.position).clamp() * c.SWARM_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)


        if len(self.fishes) < c.SWARM_MANEUVER_MIN_FISHES:
            self.swarm_mode = 0


        if self.swarm_mode == 0:
            self.maneuver_energy += c.SWARM_MANEUVER_ENERGY_REFRESH * time_elapsed
            if self.maneuver_energy > c.SWARM_MANEUVER_ENERGY_MAX:
                self.maneuver_energy = c.SWARM_MANEUVER_ENERGY_MAX

        else:
            self.maneuver_energy -= c.SWARM_MANEUVER_ENERGY_DRAIN * time_elapsed

        if self.maneuver_energy <= 0:
            self.maneuver_energy = 0
            self.swarm_mode = 0



        self.direction = self.velocity * 100

        self.mode.distance_travelled += (self.last_pos - self.position).length
        self.last_pos = self.position

        for f in self.fishes:
            f.update(time_elapsed)

    def valid_position(self):

        secX, secY = self.mode.get_sector(self)
        if not game.world.depth((secX, secY)):
            return False
        return True

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position
        u.draw_pos_dir(scr, self.position - cam, self.direction)


        if self.maneuver_energy != c.SWARM_MANEUVER_ENERGY_MAX:
            #pygame.draw.rect(scr, (0, 0, 0), pygame.Rect((10, c.SCREEN_DIMENSIONS.y - 20), (c.SCREEN_DIMENSIONS.x - 20, 10)))
            pygame.draw.rect(scr, (255, 255, 255), pygame.Rect((10, c.SCREEN_DIMENSIONS.y - 20), (c.SCREEN_DIMENSIONS.x - 20, 10)), 1)
            pygame.draw.rect(scr, (255, 255, 255), pygame.Rect((10, c.SCREEN_DIMENSIONS.y - 20), ( (c.SCREEN_DIMENSIONS.x - 20) * (self.maneuver_energy / c.SWARM_MANEUVER_ENERGY_MAX) , 10)))

        for f in self.fishes:
            f.render()
