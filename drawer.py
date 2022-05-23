import math

import pygame
import pygame as pg
from settings import *
import game_board

from game_board import *
from settings import *

def draw_board(crop=2):
    for t in Tile.tiles_pile:
        for l in t.placements:
            SCREEN.blit(source=pg.transform.rotate(t.sprite, l['rotation'] * 90).subsurface([
                crop,crop,t.sprite.get_width()-crop*2,t.sprite.get_height()-crop*2]),
                        dest=[l['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0] + crop,
                              l['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1] + crop])

def draw_debug_info():
    for t in Tile.tiles_pile:
        for l in t.placements:
            for c in t.connections:
                if c['type'] == 'road':
                    color = [0, 0, 255]
                else: color = [255, 0, 0]

                vertex_array = []

                if c['connections'][(0 + l['rotation']) % 4]:
                    vertex_array.append(
                    (l['location'][0] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[0],
                     l['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1]))

                if c['connections'][(1 + l['rotation']) % 4]:
                    vertex_array.append(
                    (l['location'][0] * GRID_SCALE + GRID_SCALE - VIEW_PORT_CENTRE[0],
                     l['location'][1] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[1]))

                if c['connections'][(2 + l['rotation']) % 4]:
                    vertex_array.append(
                    (l['location'][0] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[0],
                     l['location'][1] * GRID_SCALE + GRID_SCALE - VIEW_PORT_CENTRE[1]))

                if c['connections'][(3 + l['rotation']) % 4]:
                    vertex_array.append(
                    (l['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0],
                     l['location'][1] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[1]))

                for v in vertex_array:
                    pg.draw.circle(SCREEN, color, v, 5)

                if len(vertex_array) > 1:
                    pg.draw.lines(SCREEN, color, False, vertex_array, 2)

def draw_gui():
    SCREEN.fill([255,255,255], [0, 0, 100, SCREEN.get_rect()[3]])
    SCREEN.blit(pg.transform.scale(game_board.Tile.selected_tile.sprite, [60, 60]), [20, 20])

def draw_tile_highlight(location):
    SCREEN.blit(game_board.Tile.selected_tile.sprite, location)


