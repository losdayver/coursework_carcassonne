import math
import pygame as pg
from game_board import *
from settings import *

def draw_board(crop=2):
    '''
    Функция выводит игровую доску на экран

    :param crop: Обрезка тайлов по краям
    '''

    for t in Tile.tiles_pile:
        for p in t.placements:
            SCREEN.blit(source=pg.transform.rotate(t.sprite, p['rotation'] * 90).subsurface([
                crop,crop,t.sprite.get_width()-crop*2,t.sprite.get_height()-crop*2]),
                        dest=[p['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0] + crop,
                              p['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1] + crop])

def draw_debug_info():
    '''
    Выводит информацию для разработчика
    '''

    for t in Tile.tiles_pile:
        for l in t.placements:
            for i, c in enumerate(t.connections):

                text = SMALL_FONT.render(f"{l['enclosed_connections']}", True, [0,0,0])
                x = l['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0]
                y = l['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1]
                SCREEN.blit(text, (x, y + 5))

                if c['type'] == 'road':
                    color = [0, 0, 255]
                else: color = [255, 0, 0]

                vertex_array = []

                if c['connections'][(0 + l['rotation']) % 4]:
                    x = l['location'][0] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[0]
                    y = l['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1]
                    vertex_array.append((x, y))
                    text = DEBUG_FONT.render(f"{l['connection_ids'][i]}", True, color)
                    SCREEN.blit(text, (x, y+5))

                if c['connections'][(1 + l['rotation']) % 4]:
                    x = l['location'][0] * GRID_SCALE + GRID_SCALE - VIEW_PORT_CENTRE[0]
                    y = l['location'][1] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[1]
                    vertex_array.append((x, y))
                    text = DEBUG_FONT.render(f"{l['connection_ids'][i]}", True, color)
                    SCREEN.blit(text, (x-20, y))

                if c['connections'][(2 + l['rotation']) % 4]:
                    x = l['location'][0] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[0]
                    y = l['location'][1] * GRID_SCALE + GRID_SCALE - VIEW_PORT_CENTRE[1]
                    vertex_array.append((x, y))
                    text = DEBUG_FONT.render(f"{l['connection_ids'][i]}", True, color)
                    SCREEN.blit(text, (x, y-20))

                if c['connections'][(3 + l['rotation']) % 4]:
                    x = l['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0]
                    y = l['location'][1] * GRID_SCALE + GRID_SCALE / 2 - VIEW_PORT_CENTRE[1]
                    vertex_array.append((x, y))
                    text = DEBUG_FONT.render(f"{l['connection_ids'][i]}", True, color)
                    SCREEN.blit(text, (x+5, y))

                for i, v in enumerate(vertex_array):
                    pg.draw.circle(SCREEN, color, v, 5)

                if len(vertex_array) > 1:
                    pg.draw.lines(SCREEN, color, False, vertex_array, 2)

    for i, s in enumerate(Tile.structure_score):
        text = text = DEBUG_FONT.render(f"{s} : {Tile.structure_score[s]}", True, [0,0,0])
        SCREEN.blit(text, (pg.display.get_window_size()[0] - text.get_width(), i * 20))

def draw_gui():
    SCREEN.blit(pg.transform.scale(Tile.selected_tile.sprite, [60, 60]), [20, 20])

    text = REGULAR_FONT.render(f'Плиток осталось: {Tile.total_amount}', True, [0, 0, 0])
    SCREEN.blit(text, [100, 50])

    for i, p in enumerate(Player.current_players):

        SCREEN.blit(p.sprite, [10, 100+i*40])
        text = REGULAR_FONT.render(f'{p.name} Счет: {p.score} Осталось миплов: {p.meeples_left}', True, [0,0,0])
        if Player.turn == i:
            SCREEN.blit(HAND_SIGN_SPRITE, [text.get_width() + 60, 120 + i * 40])
        SCREEN.blit(text, [50, 120+i*40])

def draw_tile_highlight(location):
    highlight_sprite = pg.transform.rotate(Tile.selected_tile.sprite, Tile.selected_tile_rotation * 90)
    highlight_sprite.fill([0,40,100], special_flags=pg.BLEND_ADD)
    SCREEN.blit(highlight_sprite, location, special_flags=pg.BLEND_MULT)

meeple_highlight_location = [0, 0]
meeple_highlight_margin = 20
# Возвращает результирующую ориентацию поставновки мипла
def draw_meeple_highlight():
    global meeple_highlight_location
    global meeple_highlight_margin

    mouse_location = pg.mouse.get_pos()

    meeple_orientation = None

    last_tile_location = [0, 0]
    last_tile_location[0] = Tile.last_placed_tile.placements[-1]['location'][0] * GRID_SCALE
    last_tile_location[1] = Tile.last_placed_tile.placements[-1]['location'][1] * GRID_SCALE

    offset = [GRID_SCALE // 2 - MEEPLE_SPRITE.get_width() // 2, GRID_SCALE // 2 - MEEPLE_SPRITE.get_height() // 2]

    if last_tile_location[0] < pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0] < last_tile_location[0] + GRID_SCALE and \
        last_tile_location[1] < pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1] < last_tile_location[1] + GRID_SCALE:

            if last_tile_location[0] + meeple_highlight_margin < pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0] < last_tile_location[0] + GRID_SCALE - meeple_highlight_margin:
                if pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1] < last_tile_location[1] + meeple_highlight_margin:
                    offset = [GRID_SCALE // 2 - MEEPLE_SPRITE.get_width() // 2, 0]
                    meeple_orientation = 'up'
                elif last_tile_location[1] + GRID_SCALE - meeple_highlight_margin < pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]:
                    offset = [GRID_SCALE // 2 - MEEPLE_SPRITE.get_width() // 2, GRID_SCALE - MEEPLE_SPRITE.get_height()]
                    meeple_orientation = 'down'
                else: meeple_orientation = 'centre'

                meeple_highlight_location = [last_tile_location[0] + offset[0] - VIEW_PORT_CENTRE[0],
                                             last_tile_location[1] + offset[1] - VIEW_PORT_CENTRE[1]]

            elif last_tile_location[1] + meeple_highlight_margin < pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1] < last_tile_location[1] + GRID_SCALE - meeple_highlight_margin:
                if pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0] < last_tile_location[0] + meeple_highlight_margin:
                    offset = [0, GRID_SCALE // 2 - MEEPLE_SPRITE.get_height() // 2]
                    meeple_orientation = 'left'
                elif last_tile_location[0] + GRID_SCALE - meeple_highlight_margin < pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]:
                    offset = [GRID_SCALE - MEEPLE_SPRITE.get_height(), GRID_SCALE // 2 - MEEPLE_SPRITE.get_height() // 2]
                    meeple_orientation = 'right'
                else:
                    meeple_orientation = 'centre'

                meeple_highlight_location = [last_tile_location[0] + offset[0] - VIEW_PORT_CENTRE[0],
                                             last_tile_location[1] + offset[1] - VIEW_PORT_CENTRE[1]]

            SCREEN.blit(Player.current_players[Player.turn].sprite, meeple_highlight_location)

            meeple_highlight_location[0] += VIEW_PORT_CENTRE[0]
            meeple_highlight_location[1] += VIEW_PORT_CENTRE[1]

    return (meeple_highlight_location, meeple_orientation)

highlight_last_tile_margin = 1
def highlight_last_tile(turn):
    SCREEN.fill(Player.current_players[turn].color,
                [Tile.last_placed_tile.placements[-1]['location'][0] * GRID_SCALE - VIEW_PORT_CENTRE[0] - highlight_last_tile_margin,
                 Tile.last_placed_tile.placements[-1]['location'][1] * GRID_SCALE - VIEW_PORT_CENTRE[1] - highlight_last_tile_margin,
                 GRID_SCALE + highlight_last_tile_margin*2, GRID_SCALE + highlight_last_tile_margin*2])

def draw_all_meeples():
    for plr in Player.current_players:
        for coords in plr.meeples_coords:
            SCREEN.blit(plr.sprite, (coords[0] - VIEW_PORT_CENTRE[0], coords[1] - VIEW_PORT_CENTRE[1]))



