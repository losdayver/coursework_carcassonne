from settings import *
import random

# Данный класс описывает тип тайла, а не отдельные сущности тайлов
class Tile:
    total_amount = 72
    tiles_pile = [] # Список всех возможных видов тайлов
    selected_tile = None # Выбранный в данный момент тайл, который будет участвовать в следующем ходе
    selected_tile_rotation = 0 # Вращение выбранного тайла

    def __init__(self, sprite:pg.Surface, quantity:int, connections:list=[], has_monastery:bool=False, has_shield:bool=False):
        # Количество тайлов данного типа в колоде (осталось)
        self.quantity = quantity

        # Здесь прописаны поля, дороги, города на тайле, а также их соединения
        self.connections = connections # { 'type' : 'town', 'connections' : [True, False, False, True]}

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
        self.placements = [] # { location : (x,y), rotation : r }

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
        if test_if_can_be_placed and not Tile.can_place_tile(location): return

        print(Tile.selected_tile.simlified_connections)
        is_place_occupied = False
        print(location)

        for t in Tile.tiles_pile:
            for l in t.placements:
                if l['location'] == location: return

        Tile.selected_tile.quantity -= 1
        Tile.total_amount -= 1
        Tile.selected_tile.placements.append({'location' : location, 'rotation' : Tile.selected_tile_rotation})

        Tile.pick_random_tile()

    @staticmethod
    def can_place_tile(location):
        has_at_least_one_connection = False

        for t in Tile.tiles_pile:
            for p in t.placements:

                # Проверяемый тайл выше текущего
                if p['location'][0] == location[0] and p['location'][1] == location[1] - 1:
                    has_at_least_one_connection = True
                    if not t.simlified_connections[(2 + p['rotation']) % 4] == \
                    Tile.selected_tile.simlified_connections[(0 + Tile.selected_tile_rotation) % 4]:
                        return False

                # Проверяемый тайл ниже текущего
                elif p['location'][0] == location[0] and p['location'][1] == location[1] + 1:
                    has_at_least_one_connection = True
                    if not t.simlified_connections[(0 + p['rotation']) % 4] == \
                    Tile.selected_tile.simlified_connections[(2 + Tile.selected_tile_rotation) % 4]:
                        return False

                # Проверяемый тайл правее текущего
                elif p['location'][0] == location[0] + 1 and p['location'][1] == location[1]:
                    has_at_least_one_connection = True
                    if not t.simlified_connections[(3 + p['rotation']) % 4] == \
                    Tile.selected_tile.simlified_connections[(1 + Tile.selected_tile_rotation) % 4]:
                        return False

                # Проверяемый тайл левее текущего
                elif p['location'][0] == location[0] - 1 and p['location'][1] == location[1]:
                    has_at_least_one_connection = True
                    if not t.simlified_connections[(1 + p['rotation']) % 4] == \
                    Tile.selected_tile.simlified_connections[(3 + Tile.selected_tile_rotation) % 4]:
                        return False


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

