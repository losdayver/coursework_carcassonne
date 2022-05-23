#TODO
# 1 день -- сделал расстановку тайлов 1 типа
# 2 день -- сделал визуальный дебаг

if __name__ != '__main__': quit()

from settings import *
import random

import game_board

from drawer import *

counter = 0
for y in [2*i for i in range(5)]:
    for x in [2*i for i in range(5)]:
        game_board.Tile.place_tile(
            location=(x, y),
            rotation=0)
        game_board.Tile.selected_tile = game_board.Tile.tiles_pile[counter]
        counter+=1

mouse_lock = False
mouse_lock_location = [0,0]
can_press_mouse = True
clock = pg.time.Clock()
while 1:
    event = pg.event.get()
    for e in event:
        if pg.QUIT == e.type: quit()

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_UP]: VIEW_PORT_CENTRE[1] -= VIEW_PORT_MOV_SPEED
    if keys_pressed[pg.K_DOWN]: VIEW_PORT_CENTRE[1] += VIEW_PORT_MOV_SPEED
    if keys_pressed[pg.K_RIGHT]: VIEW_PORT_CENTRE[0] += VIEW_PORT_MOV_SPEED
    if keys_pressed[pg.K_LEFT]: VIEW_PORT_CENTRE[0] -= VIEW_PORT_MOV_SPEED

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

    print(mouse_lock_location)


    if mouse_pressed[0] and can_press_mouse:

        can_press_mouse = False
        game_board.Tile.place_tile(
            location=((pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]) // GRID_SCALE,
                      (pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]) // GRID_SCALE),
            rotation=random.randint(0,4))

        game_board.Tile.selected_tile = random.choice(game_board.Tile.tiles_pile)

    elif not mouse_pressed[0]: can_press_mouse = True

    SCREEN.fill([0,0,0])
    draw_board()
    draw_debug_info()
    draw_gui()

    pg.display.flip()

    clock.tick(FPS)
