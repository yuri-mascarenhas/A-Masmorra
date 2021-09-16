from PPlay.sprite import *
from tile import *
import math

class Player(object):
    #--------------------Atributos--------------------
    _level: int
    _exp: float
    _points: int
    _str: int
    _vit: int
    _agi: int
    _vel: int
    _max_life: int
    _life: float
    _state: str
    _sprite: dict[Sprite]
    _weapon: Sprite
    _facing: str
    _destiny: int
    _move_direction: str
    _delay_clock: dict[float]              # lista de contadores dos delays
    _delays: dict[float]                   # define o valor dos delays
    _grid_position: list[int]

    #---------------------Métodos---------------------
    def __init__(self):
        self._level = 1
        self._exp = 0
        self._points = 1
        self._str = 5
        self._vit = 3
        self._agi = 1
        self._vel = 100
        self._max_life = self._vit // 3
        self._life = self._max_life
        self._state = "idle"
        self._sprite = {"idle": Sprite("resources/player/knight_idle_right.png", 4),
                        "moving": Sprite("resources/player/knight_run_right.png", 4)}
        self._weapon = Sprite("resources/player/sword_right.png")
        self._facing = "right"
        for i in self._sprite:
            self._sprite[i].set_total_duration(700)
        self._delay_clock = {"move": 0,
                             "attack": 0,
                             "damage": 1}
        self._delays = {"move": 1.0,
                        "attack": 0.5,
                        "damage": 1.0}
        self._grid_position = [0, 0]


    """Define a posição x,y do player"""
    def set_position(self, x: int, y: int):
        for i in self._sprite:
            self._sprite[i].x = x
            self._sprite[i].y = y

    """Define a posição no grid"""
    def set_grid_position(self, lin: int, col: int):
        self._grid_position = [lin, col]

    """Define a posição inicial do Player"""
    def set_initial_position(self, map: list[list[Tile]], tile_size):
        setted = False
        lin = 0
        while((lin < len(map)) and (not setted)):
            col = 0
            while((col < len(map[lin])) and (not setted)):
                if(map[lin][col] != None):
                    setted = True
                    self.set_position(col * tile_size, (lin * tile_size) - (self._sprite[self._state].height - tile_size))
                    self._grid_position = [lin, col]
                col += 1
            lin += 1

    """Retorna o sprite atual"""
    def get_sprite(self):
        return self._sprite[self._state]
    
    """Retorna o atributo força"""
    def get_str(self):
        return self._str

    def get_agi(self):
        return self._agi

    def get_vit(self):
        return self._vit

    def get_stats(self):
        stats = {"str": self._str, "agi": self._agi, "vit": self._vit}
        return stats

    def get_life(self):
        return self._life

    def get_max_life(self):
        return self._max_life

    def get_exp(self):
        return self._exp

    def get_level(self):
        return self._level

    def get_facing(self):
        return self._facing

    def get_points(self):
        return self._points

    """Diminui a vida do jogador"""
    def get_damage(self, value: int):
        if(self._delay_clock["damage"] <= 0):
            self._life -= value
            self._delay_clock["damage"] = self._delays["damage"]
 
    """Retorna a posição do player na matriz-mapa"""
    def get_grid_position(self):
        return self._grid_position

    """Adiciona um valor específico de experiência"""
    def add_exp(self, value: float):
        self._exp += value

    def add_points(self, value):
        self._points += value

    def remove_point(self):
        self._points -= 1

    def set_life(self, value: float):
        self._life = value

    """Aumenta a vida de acordo com a poção e seu level"""
    def use_potion(self, level: int):
        self._life += 0.5 * level

    """Define um valor específico para experiência"""
    def set_exp(self, value: float):
        self._exp = value

    """Define os valores especificados para os stats e o que eles alteram"""
    def set_stats(self, str: int, agi: int, vit: int):
        self._str = str
        self._agi = agi
        self._delays["move"] = 1.24 - 0.60 * math.log((0.21 * self._agi) + 1.27) 
        self._vel = 67.04 * math.log((2.11 * self._agi) + 3.41) - 14.69 
        self._vit = vit
        self._max_life = vit // 3

    """Aumenta o level em 1"""
    def level_up(self):
        self._level += 1

    """Diminui o tempo de delay do movimento"""
    def decrease_all_delay(self, time: int):
        for i in self._delay_clock:
            self._delay_clock[i] -= time

    """Define o movimento"""
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
        self._delay_clock["move"] = self._delays["move"]
    
    """Define se o player pode se mover na direção especificada"""
    def can_move(self, map: list[list[Tile]], dir: str):
        if(self._delay_clock["move"] > 0 or self._state == "moving"):
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

    """Controla o ataque"""
    def attack(self):
        if(self._delay_clock["attack"] <= 0):
            if(self._facing == "right"):
                self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2)
            else:
                self._weapon.x = self._sprite[self._state].x - (self._sprite[self._state].width / 2)
            self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)
            self._delay_clock["attack"] = self._delays["attack"]

    """Faz a animação do movimento"""
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
            elif(self._move_direction == "d"):
                if(self._sprite[self._state].y < self._destiny):
                    self._sprite[self._state].move_y(self._vel * delta_time)
                else:
                    for i in self._sprite:
                        self._sprite[i].y = self._destiny
                    self._state = "idle"
            elif(self._move_direction == "r"):
                if(self._sprite[self._state].x < self._destiny):
                    self._sprite[self._state].move_x(self._vel * delta_time)
                else:
                    for i in self._sprite:
                        self._sprite[i].x = self._destiny
                    self._state = "idle"

    """Faz a animação de ataque"""
    def attack_animation(self, delta_time):
        if(self._delay_clock["attack"] > 0):
            if(self._delay_clock["attack"] > (self._delays["attack"]/2)):
                if(self._facing == "right"):
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) + (30 * self._delay_clock["attack"])
                else:
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (self._weapon.width) - (30 * self._delay_clock["attack"])
                self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)
            else:
                if(self._facing == "right"):
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (30 * (self._delays["attack"] - self._delay_clock["attack"]))
                else:
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (self._weapon.width) + (30 * (self._delays["attack"] - self._delay_clock["attack"]))
                self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)

    """Retorna True se o jogador tiver atacando"""
    def is_attacking(self):
        if(self._delay_clock["attack"] > 0):
            return True
        else:
            return False

    """Retorna True se o jogador estiver invulnerável"""
    def is_immortal(self):
        if(self._delay_clock["damage"] > 0):
            return True
        else:
            return False

    """Muda a direção/facing"""
    def flip_sprite(self):
        if(self._facing == "right"):
            new_sprite = {"idle": Sprite("resources/player/knight_idle_left.png", 4),
                          "moving": Sprite("resources/player/knight_run_left.png", 4)}
            new_weapon = Sprite("resources/player/sword_left.png")
            new_weapon.x = self._weapon.x
            new_weapon.y = self._weapon.y
            for i in self._sprite:
                new_sprite[i].set_total_duration(self._sprite[i].get_total_duration())
                new_sprite[i].x = self._sprite[i].x
                new_sprite[i].y = self._sprite[i].y
            self._sprite = new_sprite
            self._weapon = new_weapon
            self._facing = "left"
        else:
            new_sprite = {"idle": Sprite("resources/player/knight_idle_right.png", 4),
                          "moving": Sprite("resources/player/knight_run_right.png", 4)}
            new_weapon = Sprite("resources/player/sword_right.png")
            new_weapon.x = self._weapon.x
            new_weapon.y = self._weapon.y
            for i in self._sprite:
                new_sprite[i].set_total_duration(self._sprite[i].get_total_duration())
                new_sprite[i].x = self._sprite[i].x
                new_sprite[i].y = self._sprite[i].y
            self._sprite = new_sprite
            self._weapon = new_weapon
            self._facing = "right"

    """Desenha o sprite do jogador e sua arma"""
    def draw(self):
        self._sprite[self._state].update()
        self._sprite[self._state].draw()
        if(self._delay_clock["attack"] > 0):
            self._weapon.draw()

    