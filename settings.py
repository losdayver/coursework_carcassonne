import pygame as pg

FPS = 60
GRID_SCALE = 78
pg.init()
SCREEN = pg.display.set_mode([1280, 720], pg.RESIZABLE)
VIEW_PORT_CENTRE = [0, 0]
VIEW_PORT_MOV_SPEED = 8

MEEPLE_COLORS = [(200,0,0),
                 (0,200,0),
                 (0,0,200),
                 (200,0,200),
                 (50,50,50)]
# Sprites
MEEPLE_SPRITE = pg.image.load('./resources/meeple.png')

REGULAR_FONT = pg.font.SysFont('Arial', 20)