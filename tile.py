from settings import *

class Tile:
    tiles_pile = []
    selected_tile = None

    def __init__(self, quantity:int, connections:list, has_monastery:bool, has_shield:bool, sprite:pg.Surface):
        self.quantity = quantity
        self.connections = connections
        self.has_monastery = has_monastery
        self.has_shield = has_shield
        self.sprite = sprite
        self.index = len(Tile.tiles_pile)

        self.locations = [] # { location : (x,y), rotation : r }

        Tile.tiles_pile.append(self)

    @staticmethod
    def place_tile(location, rotation):
        Tile.selected_tile.quantity -= 1
        Tile.selected_tile.locations.append({'location' : location, 'rotation' : rotation})


Tile.selected_tile = Tile(quantity=2,
    connections=[
        { 'type' : 'town', 'connections' : [True, False, False, True]},
        { 'type' : 'road', 'connections' : [False, True, True, False]},],
    has_monastery = False,
    has_shield = True,
    sprite = pg.image.load('./resources/tile-o.png'))
