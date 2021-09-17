from PPlay.sprite import *
from tile import *
from Player import *
import random

sprites_name_left = {"goblin": {"idle": ["resources/enemies/goblin/goblin_idle_left.png", "resources/enemies/orc_warrior/orc_warrior_idle_left.png", "resources/enemies/ogre/ogre_idle_left.png"],
                                "moving": ["resources/enemies/goblin/goblin_run_left.png", "resources/enemies/orc_warrior/orc_warrior_run_left.png", "resources/enemies/ogre/ogre_run_left.png"]},
                     "zombie": {"idle": ["resources/enemies/tiny_zombie/tiny_zombie_idle_left.png", "resources/enemies/zombie/zombie_idle_left.png", "resources/enemies/big_zombie/big_zombie_idle_left.png"],
                                "moving": ["resources/enemies/tiny_zombie/tiny_zombie_run_left.png", "resources/enemies/zombie/zombie_run_left.png", "resources/enemies/big_zombie/big_zombie_run_left.png"]},
                     "demon": {"idle": ["resources/enemies/imp/imp_idle_left.png", "resources/enemies/chort/chort_idle_left.png", "resources/enemies/big_demon/big_demon_idle_left.png"],
                               "moving": ["resources/enemies/imp/imp_run_left.png", "resources/enemies/chort/chort_run_left.png", "resources/enemies/big_demon/big_demon_run_left.png"]}}

sprites_name_right = {"goblin": {"idle": ["resources/enemies/goblin/goblin_idle_right.png", "resources/enemies/orc_warrior/orc_warrior_idle_right.png", "resources/enemies/ogre/ogre_idle_right.png"],
                                "moving": ["resources/enemies/goblin/goblin_run_right.png", "resources/enemies/orc_warrior/orc_warrior_run_right.png", "resources/enemies/ogre/ogre_run_right.png"]},
                     "zombie": {"idle": ["resources/enemies/tiny_zombie/tiny_zombie_idle_right.png", "resources/enemies/zombie/zombie_idle_right.png", "resources/enemies/big_zombie/big_zombie_idle_right.png"],
                                "moving": ["resources/enemies/tiny_zombie/tiny_zombie_run_right.png", "resources/enemies/zombie/zombie_run_right.png", "resources/enemies/big_zombie/big_zombie_run_right.png"]},
                     "demon": {"idle": ["resources/enemies/imp/imp_idle_right.png", "resources/enemies/chort/chort_idle_right.png", "resources/enemies/big_demon/big_demon_idle_right.png"],
                                "moving": ["resources/enemies/imp/imp_run_right.png", "resources/enemies/chort/chort_run_right.png", "resources/enemies/big_demon/big_demon_run_right.png"]}}

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
        self._vel = 100
        if(size < 3):
            if(type == "zombie"):
                self._vel *= 0.75
            elif(type == "demon"):
                self._vel *= 2
        self._life = 50 * size
        self._max_life = self._life
        self._type = type
        self._size = size
        self._state = "idle"
        self._facing = "left"
        self._sprite = {
            "idle": {
                "right": Sprite(sprites_name_right[type]["idle"][size - 1], 4),
                "left": Sprite(sprites_name_left[type]["idle"][size - 1], 4)
            },
            "moving": {
                "right": Sprite(sprites_name_right[type]["moving"][size - 1], 4),
                "left": Sprite(sprites_name_left[type]["moving"][size - 1], 4)
            }
        }
        for i in self._sprite:
            for key in self._sprite[i]:
                self._sprite[i][key].set_total_duration(700)
        self._damage_delay = 0
        self._move_delay = 0
        self._attack_delay = 0
        self._delays = {"move": 2, 
                        "damage": 0.5,
                        "attack": 1}

    """Retorna a vida atual do inimigo"""
    def get_life(self):
        return self._life

    """Retorna a vida máxima do inimigo"""
    def get_max_life(self):
        return self._max_life

    """Retorna o sprite do estado atual"""
    def get_sprite(self):
        return self._sprite[self._state][self._facing]
    
    """Retorna o tamanho/tipo do inimigo"""
    def get_size(self):
        return self._size

    """Diminui a vida do inimigo"""
    def get_damage(self, value: float):
        if(self._damage_delay <= 0):
            self._life -= value
            self._damage_delay = self._delays["damage"]

    """Define o dano que o inimigo causa ao jogador"""
    def do_damage(self):
        if(self._type == "goblin"):
            return self._size * 1.5
        elif(self._type == "demon"):
            return self._size
        else:
            return self._size * 0.5

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
            for key in self._sprite[i]:
                self._sprite[i][key].x = col * tile_size + (tile_size / 4)
                #self._sprite[i].y = lin * tile_size + (tile_size / 4)
                self._sprite[i][key].y = lin * tile_size - (self._sprite[self._state][self._facing].height - tile_size) 

    def is_player_in_front(self, player: Player):
        if(player.get_grid_position()[0] == self._grid_position[0] and player.get_grid_position()[1] == self._grid_position[1] + 1):
            return "l"
        elif(player.get_grid_position()[0] == self._grid_position[0] and player.get_grid_position()[1] == self._grid_position[1] - 1):
            return "r"
        elif(player.get_grid_position()[0] == self._grid_position[0] + 1 and player.get_grid_position()[1] == self._grid_position[1]):
            return "d"
        elif(player.get_grid_position()[0] == self._grid_position[0] - 1 and player.get_grid_position()[1] == self._grid_position[1]):
            return "u"
        else:
            return False

    """Define qual IA de movimento o inimigo usará"""
    def move(self,map: list[list[Tile]], tile_size: int, player: Player):
        if(self._size <= 2):
            self.move_small(map, tile_size, player)
        else:
            self.move_small(map, tile_size, player)

    """IA de movimento dos inimigos menores/médios"""
    def move_small(self, map: list[list[Tile]], tile_size: int, player: Player):
        player_grid = player.get_grid_position()
        if(self.is_player_nearby(player, 3 * self._size)):
            if not self.is_player_in_front(player):
                if(player_grid[0] < self._grid_position[0]):
                    if(self.can_move(map, 'u')):
                        self._destiny = self._sprite[self._state][self._facing].y - tile_size
                        self._grid_position[0] -= 1
                        self._state = "moving"
                        self._move_direction = 'u'
                        self._move_delay = self._delays["move"]
                elif(player_grid[1] < self._grid_position[1]):
                    if(self.can_move(map, 'l')):
                        self._destiny = self._sprite[self._state][self._facing].x - tile_size
                        self._grid_position[1] -= 1
                        self._state = "moving"
                        self._move_direction = 'l'
                        self._move_delay = self._delays["move"]
                elif(player_grid[0] > self._grid_position[0]):
                    if(self.can_move(map, 'd')):
                        self._destiny = self._sprite[self._state][self._facing].y + tile_size
                        self._grid_position[0] += 1
                        self._state = "moving"
                        self._move_direction = 'd'
                        self._move_delay = self._delays["move"]
                elif(player_grid[1] > self._grid_position[1]):
                    if(self.can_move(map, 'r')):
                        self._destiny = self._sprite[self._state][self._facing].x + tile_size
                        self._grid_position[1] += 1
                        self._state = "moving"
                        self._move_direction = 'r'
                        self._move_delay = self._delays["move"]
                if(player_grid[1] > self._grid_position[1]): self._facing = "right"
                else: self._facing = "left"
        else:
            directions = ['u', 'l', 'd', 'r']
            searching = True
            go = directions[random.randint(0,3)]
            if(self.can_move(map, go)):
                if(go == 'u'):
                    self._destiny = self._sprite[self._state][self._facing].y - tile_size
                    self._grid_position[0] -= 1
                elif(go == 'l'):
                    if(self._facing == "right"):
                        self._facing = "left"
                    self._destiny = self._sprite[self._state][self._facing].x - tile_size
                    self._grid_position[1] -= 1
                elif(go == 'd'):
                    self._destiny = self._sprite[self._state][self._facing].y + tile_size
                    self._grid_position[0] += 1
                else:
                    if(self._facing == "left"):
                        self._facing = "right"
                    self._destiny = self._sprite[self._state][self._facing].x + tile_size
                    self._grid_position[1] += 1
                self._state = "moving"
                self._move_direction = go
                self._move_delay = self._delays["move"]

    """Faz a animação de movimento do inimigo"""
    def move_animation(self, delta_time):
        if(self._state == "moving"):
            if(self._move_direction == "u"):
                if(self._sprite[self._state][self._facing].y > self._destiny):
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].move_y(-self._vel * delta_time)
                else:
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].y = self._destiny
                    self._state = "idle"
            elif(self._move_direction == "l"):
                if(self._sprite[self._state][self._facing].x > self._destiny):
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].move_x(-self._vel * delta_time)
                else:
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].x = self._destiny
                    self._state = "idle"
            elif(self._move_direction == "d"):
                if(self._sprite[self._state][self._facing].y < self._destiny):
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].move_y(self._vel * delta_time)
                else:
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].y = self._destiny
                    self._state = "idle"
            elif(self._move_direction == "r"):
                if(self._sprite[self._state][self._facing].x < self._destiny):
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].move_x(self._vel * delta_time)
                else:
                    for i in self._sprite:
                        for key in self._sprite[i]:
                            self._sprite[i][key].x = self._destiny
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

    def can_hit(self, player: Player):
        if(self._attack_delay < 0) and self.is_player_in_front(player) and player._state == "idle":
            return True
        else:
            return False
                
    """Retorna True se o player está numa distância r do inimigo"""
    def is_player_nearby(self, player: Player, radius: int):
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
        self._attack_delay -= time

    """Desenha o sprite do inimigo"""
    def draw(self, window):
        self._sprite[self._state][self._facing].update()
        pygame.draw.rect(window.screen, (255, 0, 0), 
                         (self._sprite[self._state][self._facing].x, self._sprite[self._state][self._facing].y - 7, self._sprite[self._state][self._facing].width * (self._life / self._max_life), 3))
        self._sprite[self._state][self._facing].draw()
