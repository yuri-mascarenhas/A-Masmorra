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
    _grid_position: list[int]

    #--------------------Métodos--------------------
    def __init__(self):
        self._vel = 200
        self._life = 3
        self._sprite = Sprite("assets/player/knight_idle_sheet.png", 4)
        self._move_delay = 0
        self._delay = 0.25
        self._grid_position = [0, 0]

    """Define a posição x,y do player"""
    def set_position(self, x: int, y: int):
        self._sprite.x = x
        self._sprite.y = y

    def set_initial_position(self, map: list[list[Tile]], tile_size):
        setted = False
        lin = 0
        while((lin < len(map)) and (not setted)):
            col = 0
            while((lin < len(map[lin])) and (not setted)):
                if(map[lin][col] != None):
                    setted = True
                    self.set_position(col * tile_size, (lin * tile_size) - (tile_size / 2))
                    self._grid_position = [lin, col]
                col += 1
            lin += 1

    """Retorna o sprite atual"""
    def get_sprite(self):
        return self._sprite

    """Diminui o tempo de delay do movimento"""
    def decrease_move_delay(self, time: int):
        self._move_delay -= time

    """Define o movimento do player"""
    def move(self, dir: str, tile_size: int):
        if(dir == 'u'):
            self._sprite.y -= tile_size
            self._grid_position[0] -= 1
        if(dir == 'l'):
            self._sprite.x -= tile_size
            self._grid_position[1] -= 1
        if(dir == 'd'):
            self._sprite.y += tile_size
            self._grid_position[0] += 1
        if(dir == 'r'):
            self._sprite.x += tile_size
            self._grid_position[1] += 1
        self._move_delay = self._delay
    
    """Define se o player pode se mover na direção especificada"""
    def can_move(self, map: list[list[Tile]], tile_size: int, dir: str):
        if(self._move_delay > 0):
            return False
        else:
            if(dir == 'u'):
                if(self._grid_position[0] == 0):
                    return False
                elif(map[self._grid_position[0] - 1][self._grid_position[1]] == None):
                    return False
                else:
                    return True
            if(dir == 'l'):
                if(self._grid_position[1] == 0):
                    return False
                elif(map[self._grid_position[0]][self._grid_position[1] - 1] == None):
                    return False
                else:
                    return True
            if(dir == "d"):
                if(self._grid_position[0] == len(map) - 1):
                    return False
                elif(map[self._grid_position[0] + 1][self._grid_position[1]] == None):
                    return False
                else:
                    return True
            if(dir == "r"):
                if(self._grid_position[1] == len(map[0]) - 1):
                    return False
                elif(map[self._grid_position[0]][self._grid_position[1] + 1] == None):
                    return False
                else:
                    return True
                


    
    """Desenha o sprite do jogador"""
    def draw(self):
        self._sprite.draw()

    