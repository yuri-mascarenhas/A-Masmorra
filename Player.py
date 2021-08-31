from PPlay.sprite import *
from tile import *

class Player(object):
    #--------------------Atributos--------------------
    _vel: int
    _life: int
    _state: str
    _sprite: dict[Sprite]
    _weapon: Sprite
    _destiny: int
    _move_direction: str
    _move_delay: float              # contador para o delay do movimento
    _delay: float                   # define o valor do delay de movimento
    _grid_position: list[int]

    #--------------------Métodos--------------------
    def __init__(self):
        self._vel = 100
        self._life = 3
        self._state = "idle"
        self._sprite = {"idle": Sprite("resources/player/knight_idle_right.png", 4),
                        "moving": Sprite("resources/player/knight_run.png", 4)}
        for i in self._sprite:
            self._sprite[i].set_total_duration(500)
        self._move_delay = 0
        self._delay = 0.5
        self._grid_position = [0, 0]

    """Define a posição x,y do player"""
    def set_position(self, x: int, y: int):
        for i in self._sprite:
            self._sprite[i].x = x
            self._sprite[i].y = y

    def set_initial_position(self, map: list[list[Tile]], tile_size):
        setted = False
        lin = 0
        while((lin < len(map)) and (not setted)):
            col = 0
            while((lin < len(map[lin])) and (not setted)):
                if(map[lin][col] != None):
                    setted = True
                    self.set_position(col * tile_size, (lin * tile_size) - (self._sprite[self._state].height - tile_size))
                    self._grid_position = [lin, col]
                col += 1
            lin += 1

    """Retorna o sprite atual"""
    def get_sprite(self):
        return self._sprite[self._state]

    """Diminui o tempo de delay do movimento"""
    def decrease_move_delay(self, time: int):
        self._move_delay -= time

    """Define o movimento do player"""
    def move(self, dir: str, tile_size: int):
        if(dir == 'u'):
            self._destiny = self._sprite[self._state].y - tile_size
            self._grid_position[0] -= 1
        if(dir == 'l'):
            self._destiny = self._sprite[self._state].x - tile_size
            self._grid_position[1] -= 1
        if(dir == 'd'):
            self._destiny = self._sprite[self._state].y + tile_size
            self._grid_position[0] += 1
        if(dir == 'r'):
            self._destiny = self._sprite[self._state].x + tile_size
            self._grid_position[1] += 1
        self._state = "moving"
        self._move_direction = dir
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

    """Faz a animação com movimento do jogador"""
    def move_animation(self, delta_time):
        if(self._state == "moving"):
            if(self._move_direction == "u"):
                if(self._sprite[self._state].y > self._destiny):
                    self._sprite[self._state].move_y(-self._vel * delta_time)
                else:
                    for i in self._sprite:
                        self._sprite[i].y = self._destiny
                    self._state = "idle"
            elif(self._move_direction == "l"):
                if(self._sprite[self._state].x > self._destiny):
                    self._sprite[self._state].move_x(-self._vel * delta_time)
                else:
                    for i in self._sprite:
                        self._sprite[i].x = self._destiny
                    self._state = "idle"
            if(self._move_direction == "d"):
                if(self._sprite[self._state].y < self._destiny):
                    self._sprite[self._state].move_y(self._vel * delta_time)
                else:
                    #self._sprite[self._state].y = self._destiny
                    for i in self._sprite:
                        self._sprite[i].y = self._destiny
                    self._state = "idle"
            if(self._move_direction == "r"):
                if(self._sprite[self._state].x < self._destiny):
                    self._sprite[self._state].move_x(self._vel * delta_time)
                else:
                    for i in self._sprite:
                        self._sprite[i].x = self._destiny
                    self._state = "idle"

    """Desenha o sprite do jogador"""
    def draw(self):
        self._sprite[self._state].update()
        self._sprite[self._state].draw()

    