import py2d.Math as m


class Entity(object):

    def __init__(self, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        self.position = position
        self.direction = direction


    def __str__(self):
        return "Entity(pos={}, dir={})".format(self.position, self.direction)


    def render(self, debug=False):
        if debug:
            # TODO draw little cross
            pass
