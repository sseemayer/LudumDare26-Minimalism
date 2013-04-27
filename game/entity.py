import py2d.Math as m

class Entity(object):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        self.mode = mode
        self.position = position
        self.direction = direction


    def __str__(self):
        return "Entity(pos={}, dir={})".format(self.position, self.direction)

    def update(self, time_elapsed):
        pass

    def render(self):
        pass

class PhysicsEntity(Entity):
    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), mass=1, velocity=m.Vector(0,0), max_velocity=1, velocity_decay=1):
        Entity.__init__(self, mode, position, direction)
        self.mass = mass
        self.velocity = velocity
        self.force = m.Vector(0, 0)
        self.acceleration = m.Vector(0, 0)
        self.max_velocity = max_velocity
        self.velocity_decay = velocity_decay

    def __str__(self):
        return "PhysicsEntity(pos={}, dir={}, m={}, f={}, vel={})".format(self.position, self.direction, self.mass, self.force, self.velocity)

    def apply_force(self):
        pass

    def update(self, time_elapsed):
        self.force.x = 0
        self.force.y = 0
        self.acceleration.x = 0
        self.acceleration.y = 0

        self.velocity *= self.velocity_decay

        self.apply_force()

        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration * time_elapsed

        if self.velocity.length > self.max_velocity:
            self.velocity = self.velocity.normalize() * self.max_velocity

        self.position += self.velocity * time_elapsed
        self.direction = self.velocity * 100
