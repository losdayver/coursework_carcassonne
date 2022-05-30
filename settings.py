import pygame as pg
pg.init()
pg.display.set_caption('Каркассон')

DEBUG_MODE = False
FPS = 60
GRID_SCALE = 78
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
HAND_SIGN_SPRITE = pg.image.load('./resources/hand_sign.png')

REGULAR_FONT = pg.font.SysFont('Arial', 15)
DEBUG_FONT = pg.font.SysFont('Comic Sans', 30)