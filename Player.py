from PPlay.sprite import *
from tile import *

class Player(object):
    #--------------------Atributos--------------------
    _vel: int
    _life = 0
    _sprite = None
    _weapon = None

    #--------------------Métodos--------------------
    def __init__(self, window, keyboard, mouse):
        self._window = window
        self._keyboard = keyboard
        self._mouse = mouse
        self._vel = 200
        self._life = 3
        self._sprite = Sprite("assets/player/knight_idle_sheet.png", 4)

    """Define a posição x,y do player"""
    def set_position(self, x, y):
        self._sprite.x = x
        self._sprite.y = y

    """Define o movimento do player"""
    def move(self, dir: str):
        if(dir == 'u'):
            self._sprite.move_y(-self._vel * self._window.delta_time())
        if(dir == 'l'):
            self._sprite.move_x(-self._vel * self._window.delta_time())
        if(dir == 'd'):
            self._sprite.move_y(self._vel * self._window.delta_time())
        if(dir == 'r'):
            self._sprite.move_x(self._vel * self._window.delta_time())
    
    """Define se o player pode se mover na direção especificada"""
    def can_move(self, map: list[list[Tile]], tile_size: int, dir: str):
        upper_left = [int(self._sprite.y // tile_size), int(self._sprite.x // tile_size)]
        upper_right = [int(self._sprite.y // tile_size), int((self._sprite.x + self._sprite.width) // tile_size)]
        lower_left = [int((self._sprite.y + self._sprite.height) // tile_size), int(self._sprite.x // tile_size)]
        lower_right = [int((self._sprite.y + self._sprite.height) // tile_size), int((self._sprite.x + self._sprite.width) // tile_size)]
        if(dir == 'u'):
            if((map[int((self._sprite.y + self._sprite.height / 2) // tile_size)][int(self._sprite.x // tile_size)] != None) and 
               (map[int((self._sprite.y + self._sprite.height / 2) // tile_size)][int((self._sprite.x + self._sprite.width) // tile_size)] != None)):  
                return True
            else:
                return False
        if(dir == 'l'):
            if((map[int((self._sprite.y + self._sprite.height / 2) // tile_size)][int((self._sprite.x - 10) // tile_size)] != None) and 
               (map[int((self._sprite.y + self._sprite.height) // tile_size)][int((self._sprite.x - 10) // tile_size)] != None)):  
                return True
            else:
                return False
        if(dir == "d"):
            if((map[int((self._sprite.y + self._sprite.height + 10) // tile_size)][int(self._sprite.x // tile_size)] != None) and 
               (map[int((self._sprite.y + self._sprite.height + 10) // tile_size)][int((self._sprite.x + self._sprite.width) // tile_size)] != None)):  
                return True
            else:
                return False
        if(dir == "r"):
            if((map[int((self._sprite.y + self._sprite.height / 2) // tile_size)][int((self._sprite.x + self._sprite.width + 10) // tile_size)] != None) and 
               (map[int((self._sprite.y + self._sprite.height) // tile_size)][int((self._sprite.x + self._sprite.width + 10) // tile_size)] != None)):  
                return True
            else:
                return False

    def get_sprite(self):
        return self._sprite

    def draw(self):
        self._sprite.draw()

    