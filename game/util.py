import pygame
import py2d.Math as m

import game.entity
import random
import math

V_11 = m.Vector(1, 1)

pygame.font.init()
DEBUG_FONT = pygame.font.Font( pygame.font.get_default_font(), 12)

def random_dir(min_radius = 0.1, max_radius = 1, min_angle = 0, max_angle = 2 * math.pi):

    radius = random.uniform(min_radius, max_radius)
    angle = random.uniform(min_angle, max_angle)

    return m.Vector(math.cos(angle) * radius, math.sin(angle) * radius)

def angle_steer(current, target):
    left = (target - current + math.pi * 2) % (math.pi * 2)
    right = (current - target + math.pi * 2) % (math.pi * 2)

    if left < right:
        return left
    else:
        return -right

def draw_line(surface, x0, x1, color=(255, 0, 0)):
    pygame.draw.line(
        surface,
        color,
        x0.as_tuple(),
        x1.as_tuple(),
    )


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

    pygame.draw.ellipse(
        surface,
        color,
        ( (pos - V_11 * radius).as_tuple(), (radius * 2, radius * 2) )
    )

    pygame.draw.line(
        surface,
        color,
        pos.as_tuple(),
        (pos + direction).as_tuple()
    )


def draw_text(surface, pos, text, color=(255,0,0)):
    txt = DEBUG_FONT.render(text, True, color)
    surface.blit(txt, pos.as_tuple())
