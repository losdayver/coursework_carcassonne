from settings import *
import random

game_modes = { 'tile_placing', 'meeple_placing' }
'''Здесь расписаны все возможные режимы игры (фазы)'''

current_game_mode = 'tile_placing'
'''В данной переменной хранится текущий режим игры (фаза)'''


'''---------------------------------------------КЛАССЫ------------------------------------------------------'''

class Player:
    '''Данный класс описывает игрока с его индивидуальными характеристиками, такими как: имя, цвет и т.д.'''

    turn = 0
    '''Номер игрока, который в данный момент ходит'''

    listed_players = []
    '''Список игроков данной партии'''

    current_players = []
    '''Список всех игроков в памяти приложения'''

    occupied_structures = {}
    '''
    В данном словаре хранятся занятые игроком структуры и количество миплов на них\n
    { <номер структуры> : { <игрок> : <количество миплов>, <игрок> : <количество миплов>, } }
    '''

    def __init__(self, color, name='empty'):
        self.sprite = MEEPLE_SPRITE.copy()
        '''Спрайт мипла копируется и окрашивается в сответствующий оттенок из MEEPLE_COLORS в settings.py'''

        self.sprite.fill(color, special_flags=pg.BLEND_MIN)
        self.color = color
        self.name = name
        self.score = 0
        self.meeples_left = 7
        self.meeples_coords = []
        '''Список координат всех поставленных игроком миплов (необходимо для отрисовки)'''

        Player.listed_players.append(self)
        '''При создании игрок добавляется в список игроков'''

    def participate(self):
        '''При выполнении данной функции игрок добавляется в партию'''
        Player.current_players.append(self)

    @staticmethod
    def participate_all():
        '''Данный метод добавляет всех игроков из списка listed_players в текущую партию'''
        for p in Player.listed_players:
            p.participate()

    @staticmethod
    def return_meeples():
        for s in Player.occupied_structures:
            if s in Tile.finished_structures:
                for p in Player.occupied_structures[s]:
                    p.score += 1
                Player.occupied_structures[s] = {}

class Tile:
    '''Данный класс описывает тип тайла, а не отдельные сущности тайлов'''

    _connection_ids_to_replace = {}
    '''Временная переменная для can_place_tile()'''

    _placements_to_modify = {}

    _current_tile_placement_to_modify = []

    _finished_structures = {}

    finished_structures = []

    id_counter = 0
    '''Счетчик айдишников строений'''

    structure_score = {}
    '''В данной переменной хранится счет всех строений текущей партии'''

    total_amount = 72
    '''Количество всех тайлов в игре'''

    tiles_pile = []
    '''Список всех возможных видов тайлов'''

    selected_tile = None
    '''Выбранный в данный момент тайл, который будет участвовать в следующем ходе'''

    selected_tile_rotation = 0
    '''Вращение выбранного тайла'''

    last_placed_tile = None
    '''Данная переменная ссылается на прошлый поставленный тайл'''

    def __init__(self, sprite:pg.Surface, quantity:int, connections:list=[], has_monastery:bool=False, has_shield:bool=False):
        '''
        :param sprite: спрайт тайла
        :param quantity: количество тайлов данного типа в колоде
        :param connections: соединения тайла
        :param has_monastery: есть ли монастырь?
        :param has_shield: есть ли щит?
        '''

        self.quantity = quantity
        '''Количество тайлов данного типа в колоде (осталось)'''

        self.connections = connections
        '''
        Здесь прописаны поля, дороги, города на тайле, а также их соединения\n
        { 'type' : 'town', 'connections' : [True, False, False, True], 'meeples' : []}
        '''

        self.simlified_connections = ['field', 'field', 'field', 'field']
        '''Данный список хранит какие типы соединений имеет тайл со всех сторон без информации о соединениях'''

        for connection in self.connections:
            for i, con in enumerate(connection['connections']):
                if con: self.simlified_connections[i] = connection['type']


        self.has_monastery = has_monastery
        '''Есть ли монастырь?'''

        self.has_shield = has_shield
        '''Есть ли щит?'''

        self.sprite = sprite
        '''Картинка тайла из папки ./Resources'''

        self.index = len(Tile.tiles_pile)
        '''Индекс тайла в списке tiles_pile'''


        self.placements = []
        '''
        Список координат и вращений тайлов этого типа на доске\n
        { location : (x,y), rotation : r, connection_ids: [] }
        '''


        Tile.tiles_pile.append(self)
        '''При создании типа тайла он добавляется в список всех возможных тайло'''

    @staticmethod
    def pick_random_tile():
        '''Данный метод выбирает случайный тайл из списка всех возможных (при условии, что тайл, выбранный случайным образом все еще в "колоде")'''

        random_number = random.randint(0, Tile.total_amount)
        counter = 0

        for t in Tile.tiles_pile:
            counter += t.quantity
            if counter > random_number:
                Tile.selected_tile = t
                return

    @staticmethod
    def place_tile(location, is_this_the_first_tile = True):
        '''
        Данный метод выставляет тайл на доску (если это возмжно), а также делает все необходимые расчеты за ход

        :param location: tuple с координатами (x, y)

        :param is_this_the_first_tile: True, если это стартовый (первый) тайл
        '''
        Tile.structure_score.clear()
        Player.occupied_structures.clear()
        Tile._finished_structures.clear()

        global current_game_mode

        if is_this_the_first_tile and not Tile.can_place_tile(location): return False
        elif not is_this_the_first_tile:
            Tile.structure_score[0] = 1
            Tile.structure_score[1] = 1

        for t in Tile.tiles_pile:
            for l in t.placements:
                if l['location'] == location: return False

        Tile.selected_tile.quantity -= 1
        Tile.total_amount -= 1

        connection_ids = []

        for c in Tile.selected_tile.connections:
            connection_ids.append(Tile.id_counter)
            Tile.id_counter += 1

        tile_temp = { 'location' : location,
                      'rotation' : Tile.selected_tile_rotation,
                      'connection_ids' : connection_ids,
                      'connection_meeples' : [None,] * len(connection_ids),
                      'connection_score_to_enclose' : [0,] * len(connection_ids) }

        # enclosed_ids_connections заполняем значениями, равными количеству листьев графа соответствующего соединения
        for i, connection in enumerate(Tile.selected_tile.connections):
            for c in connection['connections']:
                if c: tile_temp['connection_score_to_enclose'][i] += 1

        for i, connection in enumerate(tile_temp['connection_score_to_enclose']):
            if i in Tile._current_tile_placement_to_modify: tile_temp['connection_score_to_enclose'][i] -= 1

        Tile.selected_tile.placements.append(tile_temp)

        for t in Tile.tiles_pile:
            for p in t.placements:

                if (p['location'][0], p['location'][1]) in Tile._placements_to_modify:
                    p['connection_score_to_enclose'][Tile._placements_to_modify[p['location'][0], p['location'][1]]] -= 1

                for i, id in enumerate(p['connection_ids']):
                    connection_ids_already_checked = []


                    '''Данный фрагмент кода отвечает за подсчет 
                    количества миплов на каждом соединении 
                    и записывает их в Player.occupied_structures'''

                    plr = p['connection_meeples'][i]

                    if plr != None:
                        if p['connection_ids'][i] in Tile.finished_structures:
                            p['connection_meeples'][i] = None
                        else:
                            if id in Player.occupied_structures and plr in Player.occupied_structures[id]:
                                Player.occupied_structures[id][plr] += 1
                            elif id in Player.occupied_structures and any(Player.occupied_structures[id]):
                                Player.occupied_structures[id][plr] = 1
                            else:
                                Player.occupied_structures[id] = {}
                                Player.occupied_structures[id][plr] = 1

                    try:
                        p['connection_ids'][i] = Tile._connection_ids_to_replace[id]
                    except(Exception):
                        pass

                    if p['connection_score_to_enclose'][i] != 0:
                        Tile._finished_structures[id] = False

                    if p['connection_ids'][i] in Tile.structure_score:
                        if p['connection_ids'][i] not in connection_ids_already_checked:
                            Tile.structure_score[p['connection_ids'][i]] += 1
                            if t.has_shield: Tile.structure_score[p['connection_ids'][i]] += 1
                            connection_ids_already_checked.append(p['connection_ids'][i])
                    else:
                        Tile.structure_score[p['connection_ids'][i]] = 1
                        if t.has_shield: Tile.structure_score[p['connection_ids'][i]] += 1

        Tile._connection_ids_to_replace.clear()

        Tile.last_placed_tile = Tile.selected_tile

        for i in Tile.structure_score:
            if i not in Tile._finished_structures:
                if i not in Tile.finished_structures:
                    Tile.finished_structures.append(i)

        print(Tile._finished_structures)

        return True

    has_at_least_one_connection = False
    @staticmethod
    def can_place_tile(location:tuple) -> bool:
        '''
        Данная функция проверяет возможность установки тайла на позицию location

        :param location: tuple с координатами (x, y)

        :returns bool: возвращает True, если установка тайла возможна
        '''

        Tile._placements_to_modify.clear()
        Tile._current_tile_placement_to_modify.clear()

        global has_at_least_one_connection
        has_at_least_one_connection = False
        def check_adjecent(x, y, r1, r2, t, p):
            global has_at_least_one_connection

            if p['location'][0] == location[0] + x and p['location'][1] == location[1] + y:
                has_at_least_one_connection = True
                if not t.simlified_connections[(r1 + p['rotation']) % 4] == \
                       Tile.selected_tile.simlified_connections[(r2 + Tile.selected_tile_rotation) % 4]:
                    # Тайл поставить нельзя
                    return True
                else:
                    # Тайл поставить можно
                    #записываем в временную переменную какие id необходимо заменить на какие
                    replace_this = -1
                    replace_to_this = -1
                    for i, c in enumerate(t.connections):
                        if c['connections'][(r1 + p['rotation']) % 4]:
                            replace_to_this = p['connection_ids'][i]

                            Tile._placements_to_modify[p['location'][0], p['location'][1]] = i

                            break

                    for i, c in enumerate(Tile.selected_tile.connections):
                        if c['connections'][(r2 + Tile.selected_tile_rotation) % 4]:

                            Tile._current_tile_placement_to_modify.append(i)

                            replace_this = i + Tile.id_counter

                            if replace_this in Tile._connection_ids_to_replace:
                                buffer = replace_this
                                replace_this = replace_to_this
                                replace_to_this = Tile._connection_ids_to_replace[buffer]

                            break

                    if replace_this != -1 and replace_to_this != -1 and replace_this != replace_to_this:
                        Tile._connection_ids_to_replace[replace_this] = replace_to_this

        for t in Tile.tiles_pile:
            for p in t.placements:
                if check_adjecent(0, -1, 2, 0, t, p) or \
                check_adjecent(0, 1, 0, 2, t, p) or \
                check_adjecent(1, 0, 3, 1, t, p) or \
                check_adjecent(-1, 0, 1, 3, t, p): return False

        return has_at_least_one_connection


'''------------------------------------------------ГЛОБАЛЬНЫЕ ФУНКЦИИ---------------------------------------------'''

def place_meeple(orientation, location):
    '''
    Возвращает True, если ход завершен, возвращает False, если мипла нельзя поставить

    :param orientation: строка, описывающая положение устанавливаемого мипла на тайле
    '''

    #print(orientation)
    if orientation == None:
        Tile.pick_random_tile()
        return True

    if orientation == 'centre':
        if Tile.last_placed_tile.has_monastery:
            Player.current_players[Player.turn].meeples_coords.append(location)
            Player.current_players[Player.turn].meeples_left -= 1
            Tile.pick_random_tile()
            return True
        else: return False

    for l in Tile.last_placed_tile.connections:
        for i, c in enumerate(Tile.last_placed_tile.connections):
            index_rotated = Tile.last_placed_tile.placements[-1]['rotation']
            if orientation == 'right': index_rotated += 1
            elif orientation == 'down': index_rotated += 2
            elif orientation == 'left': index_rotated += 3
            index_rotated %= 4

            if c['connections'][index_rotated]:

                if Tile.last_placed_tile.placements[-1]['connection_ids'][i] in Player.occupied_structures: return False

                Tile.last_placed_tile.placements[-1]['connection_meeples'][i] = Player.current_players[Player.turn]
                Player.current_players[Player.turn].meeples_coords.append(location)
                Player.current_players[Player.turn].meeples_left -= 1
                Tile.pick_random_tile()
                return True
    return False

for i, c in enumerate(MEEPLE_COLORS):
    Player(c, f'Игрок{i}')

Player.listed_players[0].name = 'Олежка пельмежка'

'''Здесь описаны все возможные виды тайлов в оригинальной игре'''
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

'''Starting tile'''
Tile.selected_tile = Tile(quantity=1,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-d.png'))