from PPlay.sprite import *
from tile import *

class Player(object):
    #--------------------Atributos--------------------
    _level: int
    _exp: float
    _vel: int
    _max_life: int
    _life: float
    _str: int
    _state: str
    _sprite: dict[Sprite]
    _weapon: Sprite
    _facing: str
    _destiny: int
    _move_direction: str
    _delays_clock: dict[float]             # lista de contadores dos delays
    _attack_delay: float                   # contador para o delay do ataque
    _damage_delay: float                   # contador para o delay do dano recebido
    _move_delay: float                     # contador para o delay do movimento
    _delays: dict[float]                   # define o valor dos delays
    _grid_position: list[int]

    #---------------------Métodos---------------------
    def __init__(self):
        self._level = 1
        self._exp = 0
        self._vel = 100
        self._max_life = 3
        self._life = self._max_life
        self._str = 15
        self._state = "idle"
        self._sprite = {"idle": Sprite("resources/player/knight_idle_right.png", 4),
                        "moving": Sprite("resources/player/knight_run_right.png", 4)}
        self._weapon = Sprite("resources/player/sword_right.png")
        self._facing = "right"
        for i in self._sprite:
            self._sprite[i].set_total_duration(700)
        self._move_delay = 0
        self._damage_delay = 0
        self._attack_delay = 0
        self._delays = {"move": 0.5,
                        "attack": 0.5,
                        "damage": 1.0}
        self._grid_position = [0, 0]


    """Define a posição x,y do player"""
    def set_position(self, x: int, y: int):
        for i in self._sprite:
            self._sprite[i].x = x
            self._sprite[i].y = y

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

    """Diminui a vida do jogador"""
    def get_damage(self, value: int):
        if(self._damage_delay <= 0):
            self._life -= value
            self._damage_delay = self._delays["damage"]
 
    """Retorna a posição do player na matriz-mapa"""
    def get_grid_position(self):
        return self._grid_position

    """Adiciona um valor específico de experiência"""
    def add_exp(self, value: float):
        self._exp += value

    """Define um valor específico para experiência"""
    def set_exp(self, value: float):
        self._exp = value

    """Aumenta o level em 1"""
    def level_up(self):
        self._level += 1

    """Diminui o tempo de delay do movimento"""
    def decrease_all_delay(self, time: int):
        self._move_delay -= time
        self._attack_delay -= time
        self._damage_delay -= time

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
        self._move_delay = self._delays["move"]
    
    """Define se o player pode se mover na direção especificada"""
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

    """Controla o ataque do jogador"""
    def attack(self):
        if(self._attack_delay <= 0):
            if(self._facing == "right"):
                self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2)
            else:
                self._weapon.x = self._sprite[self._state].x - (self._sprite[self._state].width / 2)
            self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)
            self._attack_delay = self._delays["attack"]

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
        if(self._attack_delay > 0):
            if(self._attack_delay > (self._delays["attack"]/2)):
                if(self._facing == "right"):
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) + (30 * self._attack_delay)
                else:
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (self._weapon.width) - (30 * self._attack_delay)
                self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)
            else:
                if(self._facing == "right"):
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (30 * (self._delays["attack"] - self._attack_delay))
                else:
                    self._weapon.x = self._sprite[self._state].x + (self._sprite[self._state].width / 2) - (self._weapon.width) + (30 * (self._delays["attack"] - self._attack_delay))
                self._weapon.y = self._sprite[self._state].y + (self._sprite[self._state].height / 2) + (self._weapon.height / 2)

    """Retorna True se o jogador tiver atacando"""
    def is_attacking(self):
        if(self._attack_delay > 0):
            return True
        else:
            return False

    """Retorna True se o jogador estiver invulnerável"""
    def is_immortal(self):
        if(self._damage_delay > 0):
            return True
        else:
            return False

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
        if(self._attack_delay > 0):
            self._weapon.draw()

    