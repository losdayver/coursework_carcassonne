if __name__ != '__main__': quit()

import random
from settings import *
import game_board
from drawer import *

# Переменные для регистрации нажатий и тд
MOUSE_LOCK = False
MOUSE_LOCK_LOCATION = [0, 0]
CAN_PRESS_MOUSE = True
CAN_PRESS_ROTATE = True
CAN_PRESS_DEBUG = True
CAN_PLACE_MEEPLE = False
MEEPLE_ORIENTATION = None

clock = pg.time.Clock()

game_board.Player.listed_players[0].participate()
game_board.Player.listed_players[1].participate()

game_board.selected_tile = game_board.Tile.tiles_pile[-1]
game_board.Tile.place_tile((7, 5), False)
Tile.pick_random_tile()

while 1:
    event = pg.event.get()
    for e in event:
        if pg.QUIT == e.type: quit()

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed(3)

    if game_board.current_game_mode == 'tile_placing':

        # Вращаение тайлов
        if keys_pressed[pg.K_r] and CAN_PRESS_ROTATE:
            CAN_PRESS_ROTATE = False
            game_board.Tile.selected_tile_rotation += 1
            game_board.Tile.selected_tile_rotation %= 4
        elif not keys_pressed[pg.K_r]:
            CAN_PRESS_ROTATE = True

        # Установка тайлов
        if mouse_pressed[0] and CAN_PRESS_MOUSE:
            CAN_PRESS_MOUSE = False
            if game_board.Tile.place_tile(
                location=((pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]) // GRID_SCALE,
                          (pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]) // GRID_SCALE), ):
                game_board.current_game_mode = 'meeple_placing'
        elif not mouse_pressed[0]:
            CAN_PRESS_MOUSE = True

    elif game_board.current_game_mode == 'meeple_placing':

        # Установка миплов
        if mouse_pressed[0] and CAN_PLACE_MEEPLE:
            if game_board.place_meeple(MEEPLE_ORIENTATION):
                CAN_PLACE_MEEPLE = False
                Tile.pick_random_tile()

                if game_board.current_game_mode != 'game_end':
                    game_board.current_game_mode = 'tile_placing'
                    Player.turn += 1
                    Player.turn %= len(Player.current_players)
                else:
                    Player.return_meeples()

        elif not mouse_pressed[0]:
            CAN_PLACE_MEEPLE = True

    # Режим дебага
    if CAN_PRESS_DEBUG and keys_pressed[pg.K_d]:
        CAN_PRESS_DEBUG = False
        DEBUG_MODE = not DEBUG_MODE
    elif not keys_pressed[pg.K_d]:
        CAN_PRESS_DEBUG = True

    # Перемещение вьюпорта
    if mouse_pressed[2] or keys_pressed[pg.K_SPACE]:
        if not MOUSE_LOCK:
            MOUSE_LOCK = True
            MOUSE_LOCK_LOCATION = pg.mouse.get_pos()
        else:
            VIEW_PORT_CENTRE[0] += MOUSE_LOCK_LOCATION[0] - pg.mouse.get_pos()[0]
            VIEW_PORT_CENTRE[1] += MOUSE_LOCK_LOCATION[1] - pg.mouse.get_pos()[1]
            MOUSE_LOCK_LOCATION = pg.mouse.get_pos()
    else:
        MOUSE_LOCK = False

    SCREEN.fill([255, 255, 255])

    # Отрисовка подсветки текущего / прошлого тайла
    if game_board.current_game_mode == 'tile_placing' and Tile.total_amount < 71:
        highlight_last_tile(abs((Player.turn-1)%len(Player.current_players)))
    elif Tile.total_amount < 71: highlight_last_tile(Player.turn)

    draw_board()

    # Отрисовка "призрака тайла"
    if game_board.current_game_mode == 'tile_placing':
        draw_tile_highlight(location=((pg.mouse.get_pos()[0] + VIEW_PORT_CENTRE[0]) // GRID_SCALE * GRID_SCALE - VIEW_PORT_CENTRE[0],
                                  ((pg.mouse.get_pos()[1] + VIEW_PORT_CENTRE[1]) // GRID_SCALE * GRID_SCALE - VIEW_PORT_CENTRE[1])))
    # Отрисовка "призрака мипла"
    elif game_board.current_game_mode == 'meeple_placing':

        MEEPLE_ORIENTATION = draw_meeple_highlight()

    #draw_all_meeples()

    if DEBUG_MODE:
        draw_debug_info()

    draw_gui()

    pg.display.flip()

    clock.tick(FPS)
