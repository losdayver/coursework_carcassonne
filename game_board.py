from settings import *
import random

class Player:
    turn = 0
    listed_players = []
    current_players = []

    def __init__(self, color, name='empty'):
        self.sprite = MEEPLE_SPRITE.copy()
        self.sprite.fill(color, special_flags=pg.BLEND_MIN)
        self.color = color
        self.name = name
        self.score = 0
        self.meeples_left = 7
        self.placed_meeples = {} # Здесь хранятся оккупированные миплами объекты вида { номер : количество миплов }
        self.meeples_coords = []
        Player.listed_players.append(self)

    def participate(self):
        Player.current_players.append(self)

    @staticmethod
    def participate_all():
        for p in Player.listed_players:
            p.participate()

game_modes = { 'tile_placing', 'meeple_placing'}
current_game_mode = 'tile_placing'

for i, c in enumerate(MEEPLE_COLORS):
    Player(c, f'Игрок{i}')

# Данный класс описывает тип тайла, а не отдельные сущности тайлов
class Tile:
    _connection_ids_to_replace = {}
    _id_counter = 0

    structure_score = {}
    total_amount = 72
    tiles_pile = [] # Список всех возможных видов тайлов
    selected_tile = None # Выбранный в данный момент тайл, который будет участвовать в следующем ходе
    selected_tile_rotation = 0 # Вращение выбранного тайла

    last_placed_tile = None

    def __init__(self, sprite:pg.Surface, quantity:int, connections:list=[], has_monastery:bool=False, has_shield:bool=False):
        # Количество тайлов данного типа в колоде (осталось)
        self.quantity = quantity

        # Здесь прописаны поля, дороги, города на тайле, а также их соединения
        self.connections = connections # { 'type' : 'town', 'connections' : [True, False, False, True], 'meeples' : []}

        # Данный список хранит какие типы соединений имеет тайл со всех сторон без информации о соединениях
        self.simlified_connections = ['field', 'field', 'field', 'field']

        for connection in self.connections:
            for i, con in enumerate(connection['connections']):
                if con: self.simlified_connections[i] = connection['type']

        # Есть ли монастырь?
        self.has_monastery = has_monastery

        # Есть ли щит?
        self.has_shield = has_shield

        # Картинка тайла из папки ./Resources
        self.sprite = sprite

        # Индекс тайла в списке tiles_pile
        self.index = len(Tile.tiles_pile)

        # Список координат и вращений тайлов этого типа на доске
        self.placements = [] # { location : (x,y), rotation : r, connection_ids: [] }

        Tile.tiles_pile.append(self)

    @staticmethod
    def pick_random_tile():
        random_number = random.randint(0, Tile.total_amount)
        counter = 0

        for t in Tile.tiles_pile:
            counter += t.quantity
            if counter > random_number:
                Tile.selected_tile = t
                return

    @staticmethod
    def place_tile(location, test_if_can_be_placed = True):
        global current_game_mode

        if test_if_can_be_placed and not Tile.can_place_tile(location): return False
        elif not test_if_can_be_placed:
            Tile.structure_score[0] = 1
            Tile.structure_score[1] = 1

        for t in Tile.tiles_pile:
            for l in t.placements:
                if l['location'] == location: return False

        Tile.selected_tile.quantity -= 1
        Tile.total_amount -= 1

        connection_ids = []

        for c in Tile.selected_tile.connections:
            connection_ids.append(Tile._id_counter)
            Tile._id_counter += 1

        Tile.selected_tile.placements.append({'location' : location,
                                              'rotation' : Tile.selected_tile_rotation,
                                              'connection_ids': connection_ids})

        Tile.structure_score.clear()

        for t in Tile.tiles_pile:
            for p in t.placements:
                for i, id in enumerate(p['connection_ids']):
                    connection_ids_already_checked = []

                    try:
                        p['connection_ids'][i] = Tile._connection_ids_to_replace[id]
                    except(Exception):
                        pass

                    if p['connection_ids'][i] in Tile.structure_score:
                        if p['connection_ids'][i] not in connection_ids_already_checked:
                            Tile.structure_score[p['connection_ids'][i]] += 1
                            connection_ids_already_checked.append(p['connection_ids'][i])
                    else: Tile.structure_score[p['connection_ids'][i]] = 1

        Tile._connection_ids_to_replace.clear()

        Tile.last_placed_tile = Tile.selected_tile

        Tile.pick_random_tile()

        print(Tile.structure_score)

        return True

    has_at_least_one_connection = False
    @staticmethod
    def can_place_tile(location):
        global has_at_least_one_connection
        has_at_least_one_connection = False
        def check_adjecent(x, y, r1, r2, t, p):
            global has_at_least_one_connection

            if p['location'][0] == location[0] + x and p['location'][1] == location[1] + y:
                has_at_least_one_connection = True
                if not t.simlified_connections[(r1 + p['rotation']) % 4] == \
                       Tile.selected_tile.simlified_connections[(r2 + Tile.selected_tile_rotation) % 4]:
                    return True
                else:
                    # записываем во временную переенную какие id необходимо заменить на какие
                    replace_this = -1
                    replace_to_this = -1
                    for i, c in enumerate(t.connections):
                        if c['connections'][(r1 + p['rotation']) % 4]:
                            replace_to_this = p['connection_ids'][i]
                            break

                    for i, c in enumerate(Tile.selected_tile.connections):
                        if c['connections'][(r2 + Tile.selected_tile_rotation) % 4]:
                            replace_this = i + Tile._id_counter

                            if replace_this in Tile._connection_ids_to_replace:
                                buffer = replace_this
                                replace_this = replace_to_this
                                replace_to_this = Tile._connection_ids_to_replace[buffer]

                            break

                    if replace_this != -1 and replace_to_this != -1 and replace_this != replace_to_this:
                        Tile._connection_ids_to_replace[replace_this] = replace_to_this

                    #print(Tile._connection_ids_to_replace)

        for t in Tile.tiles_pile:
            for p in t.placements:
                if check_adjecent(0, -1, 2, 0, t, p) or \
                check_adjecent(0, 1, 0, 2, t, p) or \
                check_adjecent(1, 0, 3, 1, t, p) or \
                check_adjecent(-1, 0, 1, 3, t, p): return False

        return has_at_least_one_connection

# Здесь описаны все возможные виды тайлов в оригинальной игре
Tile(quantity=4,
    connections=[],
    has_monastery = True,
    sprite = pg.image.load('./resources/tile-b.png'))

Tile(quantity=2,
    connections=[
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    has_monastery = True,
    sprite = pg.image.load('./resources/tile-a.png'))

Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, True, True]}],
    has_shield = True,
    sprite = pg.image.load('./resources/tile-c.png'))

Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]}],
    sprite = pg.image.load('./resources/tile-r.png'))

Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-q.png'))

Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]},
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    sprite = pg.image.load('./resources/tile-t.png'))

Tile(quantity=2,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]},
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-s.png'))

Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]}],
    sprite = pg.image.load('./resources/tile-n.png'))

Tile(quantity=2,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-m.png'))

Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]},
        {'type' : 'road', 'connections' : [False, True, True, False]}],
    sprite = pg.image.load('./resources/tile-p.png'))

Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, True]},
        { 'type' : 'road', 'connections' : [False, True, True, False]}],
    has_shield=True,
    sprite=pg.image.load('./resources/tile-o.png'))

Tile(quantity=1,
    connections=[
        { 'type' : 'town', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-g.png'))

Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [False, True, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-f.png'))

Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'town', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-i.png'))

Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'town', 'connections' : [False, False, True, False]}],
    sprite = pg.image.load('./resources/tile-h.png'))

Tile(quantity=5,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]}],
    sprite = pg.image.load('./resources/tile-e.png'))

Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, True]}],
    sprite = pg.image.load('./resources/tile-k.png'))

Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, True, False]}],
    sprite = pg.image.load('./resources/tile-j.png'))

Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-l.png'))

Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-d.png'))

Tile(quantity=8,
    connections=[
        { 'type' : 'road', 'connections' : [True, False, True, False]}],
    sprite = pg.image.load('./resources/tile-u.png'))

Tile(quantity=9,
    connections=[
        { 'type' : 'road', 'connections' : [False, False, True, True]}],
    sprite = pg.image.load('./resources/tile-v.png'))

Tile(quantity=4,
    connections=[
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-w.png'))

Tile(quantity=1,
    connections=[
        { 'type' : 'road', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-x.png'))

# Starting tile
Tile.selected_tile = Tile(quantity=1,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-d.png'))

