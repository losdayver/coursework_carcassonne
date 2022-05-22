#TODO
# 1 день -- сделал расстановку тайлов 1 типа

from settings import *
import random

import tile

from drawer import *

if __name__ != '__main__': quit()

can_press_mouse = True
while 1:
    event = pg.event.get()
    for e in event:
        if pg.QUIT == e.type: quit()

    mouse_pressed = pg.mouse.get_pressed(3)
    if mouse_pressed[0] and can_press_mouse:
        tile.Tile.selected_tile = random.choice(tile.Tile.tiles_pile)

        can_press_mouse = False
        tile.Tile.place_tile(
            location=(pg.mouse.get_pos()[0] // GRID_SCALE * GRID_SCALE,
                      pg.mouse.get_pos()[1] // GRID_SCALE * GRID_SCALE),
            rotation=0)

        draw_board()

        draw_debug_info()

    elif not mouse_pressed[0]: can_press_mouse = True

    pg.display.flip()
