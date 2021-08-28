from PPlay.sprite import *
from tile import *

class Player(object):
    #--------------------Atributos--------------------
    _vel: int
    _life: int
    _sprite: Sprite
    _weapon: Sprite
    _move_delay: float              # contador para o delay do movimento
    _delay: float                   # define o valor do delay de movimento

    #--------------------Métodos--------------------
    def __init__(self, window, keyboard, mouse):
        self._vel = 200
        self._life = 3
        self._delay = 0.5
        self._move_delay = 0
        self._sprite = Sprite("assets/player/knight_idle_sheet.png", 4)

    """Define a posição x,y do player"""
    def set_position(self, x, y):
        self._sprite.x = x
        self._sprite.y = y

    """Retorna o sprite atual"""
    def get_sprite(self):
        return self._sprite

    """Diminui o tempo de delay do movimento"""
    def decrease_move_delay(self, time):
        self._move_delay -= time

    """Define o movimento do player"""
    def move(self, dir: str, tile_size):
        if(dir == 'u'):
            self._sprite.y -= tile_size
        if(dir == 'l'):
            self._sprite.x -= tile_size
        if(dir == 'd'):
            self._sprite.y += tile_size
        if(dir == 'r'):
            self._sprite.x += tile_size
        self._move_delay = self._delay
    
    """Define se o player pode se mover na direção especificada"""
    def can_move(self, map: list[list[Tile]], tile_size: int, dir: str):
        if(self._move_delay > 0):
            return False
        else:
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


    
    """Desenha o sprite do jogador"""
    def draw(self):
        self._sprite.draw()

    