import pygame
import py2d.Math as m

import game.entity

def draw_cross(surface, pos, color=(255, 0, 0), radius=3):
    pygame.draw.line(
        surface,
        color,
        (pos - m.VECTOR_X * radius).as_tuple(),
        (pos + m.VECTOR_X * radius).as_tuple(),
    )

    pygame.draw.line(
        surface,
        color,
        (pos - m.VECTOR_Y * radius).as_tuple(),
        (pos + m.VECTOR_Y * radius).as_tuple(),
    )


def draw_pos_dir(surface, pos, direction=None, color=(255, 0, 0), radius=3):

    if not direction and isinstance(pos, game.entity.Entity):
        # pos is an Entity, take position and direction from that
        direction = pos.direction
        pos = pos.position

    pygame.draw.circle(
        surface,
        color,
        pos.as_tuple(),
        radius
    )

    pygame.draw.line(
        surface,
        color,
        pos.as_tuple(),
        (pos + direction).as_tuple()
    )
