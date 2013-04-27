import game
import game.util as u
import game.constants as c

import py2d.Math as m

import fish

class Swarm(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), initial_fishes=10, fish_radius=100):
        super(Swarm, self).__init__(mode, position, direction, max_velocity=c.SWARM_MAX_VELOCITY, velocity_decay=c.SWARM_VELOCITY_DECAY)

        self.target_position = position


        self.fishes = [fish.Fish(self, u.random_dir() * fish_radius, u.random_dir()) for _ in range(initial_fishes)]

    def apply_force(self):
        self.acceleration += (self.target_position - self.position).clamp() * c.SWARM_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)
        self.direction = self.velocity * 100

        for f in self.fishes:
            f.target_position = self.position
            f.update(time_elapsed)

    def render(self):
        scr = self.mode.game.screen
        u.draw_pos_dir(scr, self)

        for f in self.fishes:
            f.render()
