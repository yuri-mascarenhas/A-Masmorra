from PPlay.sprite import *
from tile import *
from Player import *
import random

class Enemy(object):
    #--------------------Atributos--------------------
    _vel: int
    _life: int
    _type: str
    _size: int
    _sprite: dict[Sprite]
    _state: str
    _destiny: int
    _move_direction: str
    _move_delay: float              # contador para o delay do movimento
    _delay: float                   # define o valor do delay de movimento
    _grid_position: list[int]

    #--------------------Métodos--------------------
    def __init__(self, type: str, size: int, life: int):
        self._vel = 200
        self._life = life
        self._type = type
        self._size = size
        self._state = "idle"
        self._sprite = {"idle": Sprite("resources/enemies/goblin/goblin_idle_anim_f0.png"), 
                        "moving": Sprite("resources/enemies/goblin/goblin_run_anim_f3.png")}
        self._move_delay = 0
        self._delay = 2

    """Define a posição x,y do inimigo"""
    def set_initial_position(self, map: list[list[Tile]], tile_size: int, player: Player):
        searching = True
        while(searching):
            lin = random.randint(0, len(map) - 1)
            col = random.randint(0, len(map[lin]) - 1)
            if((map[lin][col] != None) and (player.get_grid_position() != [lin, col])):
                searching = False
        self._grid_position = [lin, col]
        for i in self._sprite:
            self._sprite[i].x = col * tile_size
            self._sprite[i].y = lin * tile_size

    """Define qual IA de movimento o inimigo usará"""
    def move(self,map: list[list[Tile]], tile_size: int, player: Player):
        if(self._size <= 2):
            self.move_small(map, tile_size, player)
    
    """IA de movimento dos inimigos menores/médios"""
    def move_small(self,map: list[list[Tile]], tile_size: int, player: Player):
        if(self.is_player_nearby(map, player, 3 * self._size)):
            if(player.get_grid_position()[0] < self._grid_position[0]):
                if(self.can_move(map, 'u')):
                    self._destiny = self._sprite[self._state].y - tile_size
                    self._grid_position[0] -= 1
                    self._state = "moving"
                    self._move_direction = 'u'
                    self._move_delay = self._delay
            elif(player.get_grid_position()[1] < self._grid_position[1]):
                if(self.can_move(map, 'l')):
                    self._destiny = self._sprite[self._state].x - tile_size
                    self._grid_position[1] -= 1
                    self._state = "moving"
                    self._move_direction = 'l'
                    self._move_delay = self._delay
            elif(player.get_grid_position()[0] > self._grid_position[0]):
                if(self.can_move(map, 'd')):
                    self._destiny = self._sprite[self._state].y + tile_size
                    self._grid_position[0] += 1
                    self._state = "moving"
                    self._move_direction = 'd'
                    self._move_delay = self._delay
            elif(player.get_grid_position()[1] > self._grid_position[1]):
                if(self.can_move(map, 'r')):
                    self._destiny = self._sprite[self._state].x + tile_size
                    self._grid_position[1] += 1
                    self._state = "moving"
                    self._move_direction = 'r'
                    self._move_delay = self._delay
        else:
            directions = ['u', 'l', 'd', 'r']
            searching = True
            go = directions[random.randint(0,3)]
            if(self.can_move(map, go)):
                if(go == 'u'):
                    self._destiny = self._sprite[self._state].y - tile_size
                    self._grid_position[0] -= 1
                elif(go == 'l'):
                    self._destiny = self._sprite[self._state].x - tile_size
                    self._grid_position[1] -= 1
                elif(go == 'd'):
                    self._destiny = self._sprite[self._state].y + tile_size
                    self._grid_position[0] += 1
                else:
                    self._destiny = self._sprite[self._state].x + tile_size
                    self._grid_position[1] += 1
                self._state = "moving"
                self._move_direction = go
                self._move_delay = self._delay

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

    """Define se o inimigo pode se mover na direção especificada"""
    def can_move(self, map: list[list[Tile]], dir: str):
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

    """Retorna True se o player está numa distância r do inimigo"""
    def is_player_nearby(self,map: list[list[Tile]], player: Player, radius: int):
        if((player.get_grid_position()[0] >= self._grid_position[0] - radius) and 
           (player.get_grid_position()[0] <= self._grid_position[0] + radius) and
           (player.get_grid_position()[1] >= self._grid_position[1] - radius) and
           (player.get_grid_position()[1] <= self._grid_position[1] + radius)):
            return True
        else:
            return False

    """Diminui o tempo de delay do movimento"""
    def decrease_move_delay(self, time: int):
        self._move_delay -= time

    """Desenha o sprite do inimigo"""
    def draw(self):
        #self._sprite[self._state].update()
        self._sprite[self._state].draw()


