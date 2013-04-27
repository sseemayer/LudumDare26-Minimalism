import game
import game.util as u
import game.constants as c

import py2d.Math as m

class Fish(game.PhysicsEntity):

    def __init__(self, swarm, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Swarm, self).__init__(swarm.mode, position, direction, max_velocity=c.SWARM_MAX_VELOCITY, velocity_decay=c.SWARM_VELOCITY_DECAY)

        self.swarm = swarm
        self.target_position = position

    def apply_force(self):
        self.acceleration += (self.target_position - self.position).clamp() * c.SWARM_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)

    def render(self):
        scr = self.mode.game.screen
        u.draw_pos_dir(scr, self, color=(0, 255, 0), radius=2)

