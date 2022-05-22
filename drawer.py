import pygame as pg
from tile import *
from settings import *

def draw_board():
    for t in Tile.tiles_pile:
        for l in t.locations:
            SCREEN.blit(t.sprite, l['location'])

def draw_debug_info():
    for t in Tile.tiles_pile:
        for l in t.locations:
            for c in t.connections:
                if c['type'] == 'road':
                    color = [0, 0, 255]
                else: color = [255, 0, 0]

                vertex_array = []

                if c['connections'][0]:
                    vertex_array.append(
                    (l['location'][0] + GRID_SCALE / 2,
                     l['location'][1]))
                    pg.draw.circle(SCREEN, color, vertex_array[-1], 5)

                if c['connections'][1]:
                    vertex_array.append(
                    (l['location'][0] + GRID_SCALE,
                     l['location'][1] + GRID_SCALE / 2))
                    pg.draw.circle(SCREEN, color, vertex_array[-1], 5)

                if c['connections'][2]:
                    vertex_array.append(
                    (l['location'][0] + GRID_SCALE / 2,
                     l['location'][1] + GRID_SCALE))
                    pg.draw.circle(SCREEN, color, vertex_array[-1], 5)

                if c['connections'][3]:
                    vertex_array.append(
                    (l['location'][0],
                     l['location'][1] + GRID_SCALE / 2))
                    pg.draw.circle(SCREEN, color, vertex_array[-1], 5)

                if len(vertex_array) > 1:
                    pg.draw.lines(SCREEN, color, False, vertex_array, 2)


