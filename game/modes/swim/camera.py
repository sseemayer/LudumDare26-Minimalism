import game
import game.util as u
import game.constants as c

import py2d.Math as m

import fish

class Camera(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Camera, self).__init__(mode, position, direction, max_velocity=c.CAMERA_MAX_VELOCITY, velocity_decay=c.CAMERA_VELOCITY_DECAY)

        self.offset = c.SCREEN_DIMENSIONS / 2

    def apply_force(self):
        delta_pos = self.mode.swarm.position - self.position - self.offset

        if delta_pos.length >= c.CAMERA_MIN_DISTANCE:
            delta_pos *= delta_pos.length / c.CAMERA_MIN_DISTANCE
            self.acceleration += (delta_pos).clamp() * c.CAMERA_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)

    def render(self):
        u.draw_text(self.mode.game.screen, m.Vector(80, 0), "Camera: {}".format(self.position))
        u.draw_text(self.mode.game.screen, m.Vector(80, 20), "MouseW: {}".format(self.mode.mouse_pos_world))
        u.draw_text(self.mode.game.screen, m.Vector(80, 40), "MouseS: {}".format(self.mode.game.mouse_pos))

        u.draw_cross(self.mode.game.screen, self.mode.mouse_pos_world - self.position)

        pass
