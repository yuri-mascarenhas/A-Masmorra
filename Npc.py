from PPlay.sprite import *
from tile import *
from Player import *
import random

class Npc(object):
    #--------------------Atributos--------------------
    _sprite: Sprite
    _potions: int
    _potion_level: int
    _grid_position: list[int]
    _active: bool

    #---------------------Métodos---------------------
    def __init__(self):
        self._sprite = Sprite("resources/npc/wizzard_idle.png", 4)
        self._sprite.set_total_duration(1000)
        self._sprite.y = -self._sprite.height
        self._potions = 1
        self._potion_level = 1
        self._active = False

    def is_active(self):
        return self._active

    def set_active(self, value: bool = True):
        self._active = value

    def set_position(self, map: list[list[Tile]], tile_size, player: Player):
        searching = True
        while(searching):
            lin = random.randint(0, len(map) - 1)
            col = random.randint(0, len(map[lin]) - 1)
            if((map[lin][col] != None) and (player.get_grid_position() != [lin, col])):
                searching = False
        self._grid_position = [lin, col]
        self._sprite.x = (col * tile_size)

    def summon_animation(self, delta_time: float, tile_size: int):
        if(self._sprite.y < self._grid_position[0] * tile_size - (self._sprite.height - tile_size)):
            self._sprite.move_y(100 * delta_time)

    def draw(self):
        self._sprite.update()
        self._sprite.draw()