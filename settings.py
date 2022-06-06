import pygame as pg
pg.init()
pg.display.set_caption('Каркассон')

DEBUG_MODE = False
'''Включен ли режиим отладки?'''

FPS = 60
'''Количество кадров в секунду'''

GRID_SCALE = 78
'''Размер клетки игрового поля в пикселях'''

SCREEN = pg.display.set_mode([1280, 720], pg.RESIZABLE)
'''Переменная, содержащая ссылку на объект экрана приложения'''

VIEW_PORT_CENTRE = [0, 0]
'''Координаты положения камеры (левый верхний угол)'''

MEEPLE_COLORS = [(200,0,0),
                 (0,200,0),
                 (0,0,200),
                 (200,0,200),
                 (50,50,50)]
'''Список всех возможных цветов игроков'''

# Sprites
MEEPLE_SPRITE = pg.image.load('./resources/meeple2.png')
'''Картинка подданного'''

HAND_SIGN_SPRITE = pg.image.load('./resources/hand_sign.png')
'''Картинка руки для определения хода'''

# Шрифты
REGULAR_FONT = pg.font.SysFont('Arial', 15)
DEBUG_FONT = pg.font.SysFont('Comic Sans', 30)
SMALL_FONT = pg.font.SysFont('Comic Sans', 12)