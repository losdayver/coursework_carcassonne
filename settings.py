import pygame as pg
import numpy as np

FPS = 30
GRID_SCALE = 78
pg.init()
SCREEN = pg.display.set_mode([1280, 720])
VIEW_PORT_CENTRE = [0, 0]
VIEW_PORT_MOV_SPEED = 8