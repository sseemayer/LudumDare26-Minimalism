import pygame

import game
import game.util as u
import game.constants as c

import py2d.Math as m

import fish

class Camera(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Camera, self).__init__(mode, position, direction, max_velocity=c.CAMERA_MAX_VELOCITY, velocity_decay=c.CAMERA_VELOCITY_DECAY)

        self.offset = c.SCREEN_DIMENSIONS / 2
        self.cursor = pygame.image.load("data/images/cursor.png")
        self.cursor_size = m.Vector(self.cursor.get_width(), self.cursor.get_height())

    def apply_force(self):
        delta_pos = self.mode.swarm.position - self.position - self.offset

        if delta_pos.length >= c.CAMERA_MIN_DISTANCE:
            delta_pos *= delta_pos.length / c.CAMERA_MIN_DISTANCE
            self.acceleration += (delta_pos).clamp() * c.CAMERA_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)

    def render(self):
        scr = self.mode.game.screen
        #u.draw_text(self.mode.game.screen, m.Vector(80, 0), "Camera: {}".format(self.position))
        #u.draw_text(self.mode.game.screen, m.Vector(80, 20), "Active: {}".format(self.mode.active_sectors))
        #u.draw_text(self.mode.game.screen, m.Vector(80, 40), "Sector: {} {}".format(self.mode.sector_x, self.mode.sector_y))


        scr.blit(self.cursor, (self.mode.mouse_pos_world - self.position - self.cursor_size / 2).as_tuple())

        pass
