from PPlay.sprite import *

class Player(object):
    #--------------------Atributos--------------------
    _vel = 0
    _life = 0
    _sprite = None
    _weapon = None

    #--------------------Métodos--------------------
    def __init__(self, window, keyboard, mouse):
        self._window = window
        self._keyboard = keyboard
        self._mouse = mouse
        self._vel = 200
        self.life = 3
        self._sprite = Sprite("assets/player/knight_idle_sheet.png", 4)

    """Define a posição x,y do player"""
    def set_position(self, x, y):
        self._sprite.x = x
        self._sprite.y = y

    def move(self):
        if(self._keyboard.key_pressed("A")):
            self._sprite.move_x(-self._vel * self._window.delta_time())
        if(self._keyboard.key_pressed("D")):
            self._sprite.move_x(self._vel * self._window.delta_time())
        if(self._keyboard.key_pressed("W")):
            self._sprite.move_y(-self._vel * self._window.delta_time())
        if(self._keyboard.key_pressed("S")):
            self._sprite.move_y(self._vel * self._window.delta_time())

    def get_sprite(self):
        return self._sprite

    def draw(self):
        self._sprite.draw()

    