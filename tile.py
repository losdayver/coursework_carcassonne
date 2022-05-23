from settings import *

class Tile:
    tiles_pile = [] # Список всех возможных видов тайлов
    selected_tile = None # Выбранный в данный момент тайл, который будет участвовать в следующем хрде

    def __init__(self, sprite:pg.Surface, quantity:int, connections:list=[], has_monastery:bool=False, has_shield:bool=False):
        self.quantity = quantity # Количество тайлов данного типа в колоде (осталось)
        self.connections = connections # Здесь прописаны поля, дороги, города на тайле
        # Оформление имеет вид { 'type' : 'town', 'connections' : [True, False, False, True]}

        self.has_monastery = has_monastery
        self.has_shield = has_shield
        self.sprite = sprite
        self.index = len(Tile.tiles_pile) # Индекс тайла в списке всех видов тайлов tiles_pile

        self.placements = [] # { location : (x,y), rotation : r }

        Tile.tiles_pile.append(self)

    @staticmethod
    def place_tile(location, rotation):
        is_place_occupied = False
        print(location)

        for t in Tile.tiles_pile:
            for l in t.placements:
                if l['location'] == location: return

        Tile.selected_tile.quantity -= 1
        Tile.selected_tile.placements.append({'location' : location, 'rotation' : rotation})

Tile.selected_tile = Tile(quantity=4,
    connections=[],
    has_monastery = True,
    sprite = pg.image.load('./resources/tile-b.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    has_monastery = True,
    sprite = pg.image.load('./resources/tile-a.png'))

Tile.selected_tile = Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, True, True]}],
    has_shield = True,
    sprite = pg.image.load('./resources/tile-c.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]}],
    sprite = pg.image.load('./resources/tile-r.png'))

Tile.selected_tile = Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-q.png'))

Tile.selected_tile = Tile(quantity=1,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]},
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    sprite = pg.image.load('./resources/tile-t.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        {'type' : 'town', 'connections' : [True, True, False, True]},
        {'type' : 'road', 'connections' : [False, False, True, False]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-s.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]}],
    sprite = pg.image.load('./resources/tile-n.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-m.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        {'type' : 'town', 'connections' : [True, False, False, True]},
        {'type' : 'road', 'connections' : [False, True, True, False]}],
    sprite = pg.image.load('./resources/tile-p.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, True]},
        { 'type' : 'road', 'connections' : [False, True, True, False]}],
    has_shield=True,
    sprite=pg.image.load('./resources/tile-o.png'))

Tile.selected_tile = Tile(quantity=1,
    connections=[
        { 'type' : 'town', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-g.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [False, True, False, True]}],
    has_shield=True,
    sprite = pg.image.load('./resources/tile-f.png'))

Tile.selected_tile = Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'town', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-i.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'town', 'connections' : [False, False, True, False]}],
    sprite = pg.image.load('./resources/tile-h.png'))

Tile.selected_tile = Tile(quantity=5,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]}],
    sprite = pg.image.load('./resources/tile-e.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, True]}],
    sprite = pg.image.load('./resources/tile-k.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, True, False]}],
    sprite = pg.image.load('./resources/tile-j.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-l.png'))

Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-d.png'))

Tile.selected_tile = Tile(quantity=8,
    connections=[
        { 'type' : 'road', 'connections' : [True, False, True, False]}],
    sprite = pg.image.load('./resources/tile-u.png'))

Tile.selected_tile = Tile(quantity=9,
    connections=[
        { 'type' : 'road', 'connections' : [False, False, True, True]}],
    sprite = pg.image.load('./resources/tile-v.png'))

Tile.selected_tile = Tile(quantity=4,
    connections=[
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-w.png'))

Tile.selected_tile = Tile(quantity=1,
    connections=[
        { 'type' : 'road', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, False]},
        { 'type' : 'road', 'connections' : [False, False, True, False]},
        { 'type' : 'road', 'connections' : [False, False, False, True]}],
    sprite = pg.image.load('./resources/tile-x.png'))

# Starting tile
Tile.selected_tile = Tile(quantity=3,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, False]},
        { 'type' : 'road', 'connections' : [False, True, False, True]}],
    sprite = pg.image.load('./resources/tile-d.png'))

