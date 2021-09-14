from PPlay.sprite import *
from tile import *
from Player import *
import random

sprites_name_left = {"goblin": {"idle": ["resources/enemies/goblin/goblin_idle_left.png"],
                                "moving": ["resources/enemies/goblin/goblin_run_left.png"]},
                     "zombie": {"idle": ["resources/enemies/tiny_zombie/tiny_zombie_idle_left.png"],
                                "moving": ["resources/enemies/tiny_zombie/tiny_zombie_run_left.png"]}}

sprites_name_right = {"goblin": {"idle": ["resources/enemies/goblin/goblin_idle_right.png"],
                                "moving": ["resources/enemies/goblin/goblin_run_right.png"]},
                     "zombie": {"idle": ["resources/enemies/tiny_zombie/tiny_zombie_idle_right.png"],
                                "moving": ["resources/enemies/tiny_zombie/tiny_zombie_run_right.png"]}}

class Enemy(object):
    #--------------------Atributos--------------------
    _vel: int
    _life: float
    _max_life: int
    _type: str
    _size: int
    _sprite: dict[Sprite]
    _facing: str
    _state: str
    _destiny: int
    _move_direction: str
    _move_delay: float                     # contador para o delay do movimento
    _delays: dict[float]                   # define o valor do delay de movimento
    _grid_position: list[int]

    #--------------------Métodos--------------------
    def __init__(self, type: str, size: int):
        self._vel = 100 * size
        self._life = 50 * size
        self._max_life = self._life
        self._type = type
        self._size = size
        self._state = "idle"
        self._facing = "left"
        self._sprite = {"idle": Sprite(sprites_name_left[type]["idle"][size - 1], 4), 
                        "moving": Sprite(sprites_name_left[type]["moving"][size - 1], 4)}
        for i in self._sprite:
            self._sprite[i].set_total_duration(700)
        self._damage_delay = 0
        self._move_delay = 0
        self._delays = {"move": 2, 
                        "damage": 1}

    """Retorna a vida atual do inimigo"""
    def get_life(self):
        return self._life

    """Retorna a vida máxima do inimigo"""
    def get_max_life(self):
        return self._max_life

    """Retorna o sprite do estado atual"""
    def get_sprite(self):
        return self._sprite[self._state]
    
    """Retorna o tamanho/tipo do inimigo"""
    def get_size(self):
        return self._size

    """Diminui a vida do inimigo"""
    def get_damage(self, value: float):
        if(self._damage_delay <= 0):
            self._life -= value
            self._damage_delay = self._delays["damage"]

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
            self._sprite[i].x = (col * tile_size) + (tile_size / 4)
            self._sprite[i].y = lin * tile_size + (tile_size / 4)

    """Muda a direção do sprite"""
    def flip_sprite(self):
        if(self._facing == "left"):
            new_sprite = {"idle": Sprite(sprites_name_right[self._type]["idle"][self._size - 1], 4), 
                           "moving": Sprite(sprites_name_right[self._type]["moving"][self._size - 1], 4)}
            for i in self._sprite:
                new_sprite[i].set_total_duration(1000)
                new_sprite[i].x = self._sprite[i].x
                new_sprite[i].y = self._sprite[i].y
            self._sprite = new_sprite
            self._facing = "right"
        else:
            new_sprite = {"idle": Sprite(sprites_name_left[self._type]["idle"][self._size - 1], 4), 
                           "moving": Sprite(sprites_name_left[self._type]["moving"][self._size - 1], 4)}
            for i in self._sprite:
                new_sprite[i].set_total_duration(1000)
                new_sprite[i].x = self._sprite[i].x
                new_sprite[i].y = self._sprite[i].y
            self._sprite = new_sprite
            self._facing = "left"

    """Define qual IA de movimento o inimigo usará"""
    def move(self,map: list[list[Tile]], tile_size: int, player: Player):
        if(self._size == 1):
            self.move_small(map, tile_size, player)
        elif(self._size == 2):
            # Movimentação dos inimigos médios
            pass
        else:
            # Movimentação dos Bosses
            pass

    """IA de movimento dos inimigos menores/médios"""
    def move_small(self,map: list[list[Tile]], tile_size: int, player: Player):
        if(self.is_player_nearby(map, player, 3 * self._size)):
            if(player.get_grid_position()[0] < self._grid_position[0]):
                if(self.can_move(map, 'u')):
                    self._destiny = self._sprite[self._state].y - tile_size
                    self._grid_position[0] -= 1
                    self._state = "moving"
                    self._move_direction = 'u'
                    self._move_delay = self._delays["move"]
            elif(player.get_grid_position()[1] < self._grid_position[1]):
                if(self.can_move(map, 'l')):
                    if(self._facing == "right"):
                        self.flip_sprite()
                    self._destiny = self._sprite[self._state].x - tile_size
                    self._grid_position[1] -= 1
                    self._state = "moving"
                    self._move_direction = 'l'
                    self._move_delay = self._delays["move"]
            elif(player.get_grid_position()[0] > self._grid_position[0]):
                if(self.can_move(map, 'd')):
                    self._destiny = self._sprite[self._state].y + tile_size
                    self._grid_position[0] += 1
                    self._state = "moving"
                    self._move_direction = 'd'
                    self._move_delay = self._delays["move"]
            elif(player.get_grid_position()[1] > self._grid_position[1]):
                if(self.can_move(map, 'r')):
                    if(self._facing == "left"):
                        self.flip_sprite()
                    self._destiny = self._sprite[self._state].x + tile_size
                    self._grid_position[1] += 1
                    self._state = "moving"
                    self._move_direction = 'r'
                    self._move_delay = self._delays["move"]
        else:
            directions = ['u', 'l', 'd', 'r']
            searching = True
            go = directions[random.randint(0,3)]
            if(self.can_move(map, go)):
                if(go == 'u'):
                    self._destiny = self._sprite[self._state].y - tile_size
                    self._grid_position[0] -= 1
                elif(go == 'l'):
                    if(self._facing == "right"):
                        self.flip_sprite()
                    self._destiny = self._sprite[self._state].x - tile_size
                    self._grid_position[1] -= 1
                elif(go == 'd'):
                    self._destiny = self._sprite[self._state].y + tile_size
                    self._grid_position[0] += 1
                else:
                    if(self._facing == "left"):
                        self.flip_sprite()
                    self._destiny = self._sprite[self._state].x + tile_size
                    self._grid_position[1] += 1
                self._state = "moving"
                self._move_direction = go
                self._move_delay = self._delays["move"]

    """Faz a animação de movimento do inimigo"""
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

    """Retorna True se o inimigo pode se mover na direção especificada"""
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
    
    """Diminui o tempo de delay do dano recebido"""
    def decrease_damage_delay(self, time: int):
        self._damage_delay -= time

    """Diminui o tempo de todos os delays"""
    def decrease_all_delay(self, time: int):
        self._move_delay -= time
        self._damage_delay -= time

    """Desenha o sprite do inimigo"""
    def draw(self, window):
        self._sprite[self._state].update()
        pygame.draw.rect(window.screen, (255, 0, 0), 
                         (self._sprite[self._state].x, self._sprite[self._state].y - 7, self._sprite[self._state].width * (self._life / self._max_life), 3))
        self._sprite[self._state].draw()


