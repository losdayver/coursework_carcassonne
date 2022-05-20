#TODO
# 1 день -- сделал расстановку тайлов 1 типа

from settings import *

import tile

if __name__ != '__main__': quit()

can_press_mouse = True
while 1:
    event = pg.event.get()
    for e in event:
        if pg.QUIT == e.type: quit()

    mouse_pressed = pg.mouse.get_pressed(3)
    if mouse_pressed[0] and can_press_mouse:
        can_press_mouse = False
        tile.Tile.place_tile(
            location=(pg.mouse.get_pos()[0] // GRID_SCALE * GRID_SCALE,
                      pg.mouse.get_pos()[1] // GRID_SCALE * GRID_SCALE),
            rotation=0)

        for t in tile.Tile.tiles_pile[-1].locations:
            SCREEN.blit(tile.Tile.tiles_pile[-1].sprite, t['location'])

    elif not mouse_pressed[0]: can_press_mouse = True

    pg.display.flip()
