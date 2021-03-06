from settings import *
import random

game_modes = { 'tile_placing', 'meeple_placing', 'game_end' }
'''Здесь расписаны все возможные режимы игры (фазы)'''

current_game_mode = 'tile_placing'
'''В данной переменной хранится текущий режим игры (фаза)'''


'''---------------------------------------------КЛАССЫ------------------------------------------------------'''

class Player:
    '''Данный класс описывает игрока с его индивидуальными характеристиками, такими как: имя, цвет и т.д.'''

    turn = 0
    '''Номер игрока, который в данный момент ходит'''

    listed_players = []
    '''Список всех игроков в памяти приложения'''

    current_players = []
    '''Список игроков данной партии'''

    occupied_structures = {}
    '''
    В данном словаре хранятся занятые игроком структуры и количество миплов на них\n
    { <номер структуры> : { <игрок> : <количество миплов>, <игрок> : <количество миплов>, } }
    '''

    monasteries = {}
    '''
    В данном списке хранятся монастыри и список клеток, необходимых для их завершения\n
    { <позиция монастыря> : { 'player' : <игрок, занявший монастырь>, 'locations_left' : [], } }
    '''

    unfinished_structures = []
    '''
    В данном списке хранятся id незавершенных структур
    '''

    def __init__(self, color, name='empty'):
        self.sprite = MEEPLE_SPRITE.copy()
        '''Спрайт мипла копируется и окрашивается в сответствующий оттенок из MEEPLE_COLORS в settings.py'''

        self.sprite.fill(color, special_flags=pg.BLEND_MIN)
        self.color = color
        self.name = name
        self.score = 0
        self.meeples_left = 7
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
        '''Данный метод возвращает все фишки подданных на завершенных объектах, а также на незавершенных при финальном подсчете очков'''

        structures_checked = []

        for t in Tile.tiles_pile:
            for p in t.placements:
                for monastery_position in Player.monasteries:
                    if p['location'] in Player.monasteries[monastery_position]['locations_left']:
                        Player.monasteries[monastery_position]['locations_left'].remove(p['location'])


                if t.has_monastery and p['location'] in Player.monasteries:
                    if not any(Player.monasteries[p['location']]['locations_left']):
                        Player.monasteries[p['location']]['player'].score += 9
                        del Player.monasteries[p['location']]
                    elif current_game_mode == 'game_end':
                        Player.monasteries[p['location']]['player'].score += 9 - len(Player.monasteries[p['location']]['locations_left'])
                        del Player.monasteries[p['location']]

                for i, m in enumerate(p['connection_ids']):
                    if (m not in Player.unfinished_structures and m in Player.occupied_structures) or \
                            (current_game_mode == 'game_end' and m in Player.occupied_structures):

                        if m not in structures_checked:
                            structures_checked.append(m)
                            max_count = 0

                            for player in Player.occupied_structures[m]:
                                if max_count == 0:
                                    max_count = Player.occupied_structures[m][player]
                                elif Player.occupied_structures[m][player] > max_count:
                                    max_count = Player.occupied_structures[m][player]

                            for player in Player.occupied_structures[m]:
                                if Player.occupied_structures[m][player] == max_count:
                                    if current_game_mode == 'game_end' and t.connections[i]['type'] == 'town':
                                        player.score += Tile.structure_score[m]//2
                                    else: player.score += Tile.structure_score[m]

                        if p['connection_meeples'][i] != None:
                            p['connection_meeples'][i].meeples_left += 1
                            p['connection_meeples'][i] = None

        print(Player.monasteries)

class Tile:
    '''Данный класс описывает тип тайла, а не отдельные сущности тайлов'''

    _connection_ids_to_replace = {}
    '''Временная переменная для can_place_tile()'''

    _adjecent_tiles = {}

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
        '''При создании типа тайла он добавляется в список всех возможных тайлов'''

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
    def find_unfinished_structures():
        '''Находит все незавершенные строения на доске и записывает их в Player.unfinished_structures'''

        Player.unfinished_structures.clear()
        for t in Tile.tiles_pile:
            for p in t.placements:

                for c_i, c in enumerate(t.connections):
                    for i in range(4):

                        if not (c['connections'][i] == p['enclosed_connections'][i] or p['enclosed_connections'][i]):
                            if p['connection_ids'][c_i] not in Player.unfinished_structures:
                                Player.unfinished_structures.append(p['connection_ids'][c_i])

    @staticmethod
    def place_tile(location, is_this_the_first_tile = True):
        '''
        Данный метод выставляет тайл на доску (если это возмжно), а также делает все необходимые расчеты за ход

        :param location: tuple с координатами (x, y)

        :param is_this_the_first_tile: True, если это стартовый (первый) тайл
        '''
        Tile.structure_score.clear()
        Player.occupied_structures.clear()
        Tile._connection_ids_to_replace.clear()

        global current_game_mode

        if is_this_the_first_tile and not Tile.can_place_tile(location): return False
        elif not is_this_the_first_tile:
            Tile.structure_score[0] = 2
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

        temp_tile = {'location' : location,
                                              'rotation' : Tile.selected_tile_rotation,
                                              'connection_ids' : connection_ids,
                                              'connection_meeples' : [None,] * len(connection_ids),
                                              'enclosed_connections' : [False, False, False, False]}

        # На устанавливаемом тайле обозначаем завершены ли enclosed_connections

        if 'top' in Tile._adjecent_tiles: temp_tile['enclosed_connections'][(0 + temp_tile['rotation']) % 4] = True
        if 'right' in Tile._adjecent_tiles: temp_tile['enclosed_connections'][(1 + temp_tile['rotation']) % 4] = True
        if 'bottom' in Tile._adjecent_tiles: temp_tile['enclosed_connections'][(2  + temp_tile['rotation']) % 4] = True
        if 'left' in Tile._adjecent_tiles: temp_tile['enclosed_connections'][(3  + temp_tile['rotation']) % 4] = True

        Tile.selected_tile.placements.append(temp_tile)

        for t in Tile.tiles_pile:
            for p in t.placements:
                print(p['location'])

                for i, id in enumerate(p['connection_ids']):
                    connection_ids_already_checked = []

                    # Данный фрагмент кода отвечает за подсчет
                    # количества миплов на каждом соединении
                    # и записывает их в Player.occupied_structures

                    plr = p['connection_meeples'][i]

                    if plr != None:
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

                    how_many_points = 1
                    if t.connections[i]['type'] == 'town':
                        how_many_points = 2
                        if t.has_shield: how_many_points = 4

                    if p['connection_ids'][i] in Tile.structure_score:
                        if p['connection_ids'][i] not in connection_ids_already_checked:
                            Tile.structure_score[p['connection_ids'][i]] += how_many_points
                            connection_ids_already_checked.append(p['connection_ids'][i])
                    else:
                        Tile.structure_score[p['connection_ids'][i]] = how_many_points

        Tile.last_placed_tile = Tile.selected_tile

        Tile.find_unfinished_structures()

        return True

    has_at_least_one_connection = False
    @staticmethod
    def can_place_tile(location:tuple) -> bool:
        '''
        Данная функция проверяет возможность установки тайла на позицию location

        :param location: tuple с координатами (x, y)

        :returns bool: возвращает True, если установка тайла возможна
        '''

        global has_at_least_one_connection
        has_at_least_one_connection = False

        Tile._adjecent_tiles.clear()

        def check_adjecent(x, y, r1, r2, t, p, side):
            global has_at_least_one_connection

            if p['location'][0] == location[0] + x and p['location'][1] == location[1] + y:
                has_at_least_one_connection = True
                if not t.simlified_connections[(r1 + p['rotation']) % 4] == \
                       Tile.selected_tile.simlified_connections[(r2 + Tile.selected_tile_rotation) % 4]:
                    return True
                else:
                    '''записываем в временную переменную какие id необходимо заменить на какие'''
                    replace_this = -1
                    replace_to_this = -1
                    for i, c in enumerate(t.connections):
                        if c['connections'][(r1 + p['rotation']) % 4]:
                            replace_to_this = p['connection_ids'][i]
                            break

                    for i, c in enumerate(Tile.selected_tile.connections):
                        if c['connections'][(r2 + Tile.selected_tile_rotation) % 4]:
                            replace_this = i + Tile.id_counter

                            if replace_this in Tile._connection_ids_to_replace:
                                buffer = replace_this
                                replace_this = replace_to_this
                                replace_to_this = Tile._connection_ids_to_replace[buffer]

                            break

                    if replace_this != -1 and replace_to_this != -1 and replace_this != replace_to_this:
                        Tile._connection_ids_to_replace[replace_this] = replace_to_this

                Tile._adjecent_tiles[side] = p

        for t in Tile.tiles_pile:
            for p in t.placements:
                if check_adjecent(0, -1, 2, 0, t, p, 'top') or \
                check_adjecent(0, 1, 0, 2, t, p, 'bottom') or \
                check_adjecent(1, 0, 3, 1, t, p, 'right') or \
                check_adjecent(-1, 0, 1, 3, t, p, 'left'): return False

        # Если тайл не конфликтует с соседними, то на соседних изменяем значения соединений enclosed_connections

        if 'top' in Tile._adjecent_tiles:
            Tile._adjecent_tiles['top']['enclosed_connections'][(2 + Tile._adjecent_tiles['top']['rotation']) % 4] = True

        if 'right' in Tile._adjecent_tiles:
            Tile._adjecent_tiles['right']['enclosed_connections'][(3 + Tile._adjecent_tiles['right']['rotation']) % 4] = True

        if 'bottom' in Tile._adjecent_tiles:
            Tile._adjecent_tiles['bottom']['enclosed_connections'][(0 + Tile._adjecent_tiles['bottom']['rotation']) % 4] = True

        if 'left' in Tile._adjecent_tiles:
            Tile._adjecent_tiles['left']['enclosed_connections'][(1 + Tile._adjecent_tiles['left']['rotation']) % 4] = True

        return has_at_least_one_connection

'''------------------------------------------------ГЛОБАЛЬНЫЕ ФУНКЦИИ---------------------------------------------'''

def place_meeple(orientation):
    '''
    Уставнавливает подданного на плитку

    :param orientation: строка, описывающая положение устанавливаемого мипла на тайле
    :returns True, если ход завершен, возвращает False, если мипла нельзя поставить
    '''

    global current_game_mode

    flag = False

    if Player.current_players[Player.turn].meeples_left < 1: return True

    #print(orientation)
    if orientation == None:
        flag = True

    elif orientation == 'centre':
        if Tile.last_placed_tile.has_monastery:

            tile_loc = Tile.last_placed_tile.placements[-1]['location']
            locations = []

            for x in range(3):
                for y in range(3):
                    if not (x == 1 and y == 1):
                        locations.append((tile_loc[0] - 1 + x, tile_loc[1] - 1 + y))

            Player.monasteries[(tile_loc[0], tile_loc[1])] = {'player' : Player.current_players[Player.turn], 'locations_left' : locations}
            Player.current_players[Player.turn].meeples_left -= 1
            flag = True
        else: return False
    else:
        for l in Tile.last_placed_tile.connections:
            if flag: break
            for i, c in enumerate(Tile.last_placed_tile.connections):
                index_rotated = Tile.last_placed_tile.placements[-1]['rotation']
                if orientation == 'right': index_rotated += 1
                elif orientation == 'down': index_rotated += 2
                elif orientation == 'left': index_rotated += 3
                index_rotated %= 4

                if c['connections'][index_rotated]:

                    if Tile.last_placed_tile.placements[-1]['connection_ids'][i] in Player.occupied_structures: return False

                    Tile.last_placed_tile.placements[-1]['connection_meeples'][i] = Player.current_players[Player.turn]

                    Player.current_players[Player.turn].meeples_left -= 1
                    flag = True
                    break

    if flag:
        Player.return_meeples()

        if Tile.total_amount < 1:
            current_game_mode = 'game_end'

        return True

    return False

for i, c in enumerate(MEEPLE_COLORS):
    Player(c, f'Игрок{i}')

Player.listed_players[0].name = 'Олег'

#Здесь описаны все возможные виды тайлов в оригинальной игре
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