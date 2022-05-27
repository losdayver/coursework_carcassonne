if __name__ != '__main__': quit()

import random
from settings import *
import game_board
from drawer import *

mouse_lock = False
mouse_lock_location = [0,0]
can_press_mouse = True
can_press_rotate = True
can_press_debug = True
clock = pg.time.Clock()

game_board.Player.participate_all()
#game_board.Player.listed_players[0].participate()
#game_board.Player.listed_players[1].participate()

game_board.selected_tile = game_board.Tile.tiles_pile[-1]
game_board.Tile.place_tile([7, 5], False)
game_board.Player.turn = 0

while 1:
    event = pg.event.get()
    for e in event:
        if pg.QUIT == e.type: quit()

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed(3)

    if mouse_pressed[2] or keys_pressed[pg.K_SPACE]:
        if not mouse_lock:
            mouse_lock = True
            mouse_lock_location = pg.mouse.get_pos()
        else:
            VIEW_PORT_CENTRE[0] += mouse_lock_location[0] - pg.mouse.get_pos()[0]
            VIEW_PORT_CENTRE[1] += mouse_lock_location[1] - pg.mouse.get_pos()[1]
            mouse_lock_location = pg.mouse.get_pos()
    else: mouse_lock = False

    if keys_pressed[pg.K_r] and can_press_rotate:
        can_press_rotate = False
        game_board.Tile.selected_tile_rotation += 1
        game_board.Tile.selected_tile_rotation %= 4
    elif not keys_pressed[pg.K_r]: can_press_rotate = True

    if can_press_debug and keys_pressed[pg.K_d]:
        can_press_debug = False
        DEBUG_MODE = not DEBUG_MODE
    elif not keys_pressed[pg.K_d]: can_press_debug = True

    if mouse_pressed[0] and can_press_mouse:
        can_press_mouse = False
        game_board.Tile.place_tile(
            location=((pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]) // GRID_SCALE,
                      (pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]) // GRID_SCALE),)

    elif not mouse_pressed[0]: can_press_mouse = True

    SCREEN.fill([255, 255, 255])
    draw_board()

    if DEBUG_MODE:
        draw_debug_info()

    draw_tile_highlight(location=((pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]) // GRID_SCALE * GRID_SCALE - VIEW_PORT_CENTRE[0],
                                  ((pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]) // GRID_SCALE * GRID_SCALE - VIEW_PORT_CENTRE[1])))
    draw_gui()

    pg.display.flip()

    clock.tick(FPS)
