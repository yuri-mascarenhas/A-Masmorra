from PPlay.sprite import *
from PPlay.window import *
from PPlay.sound import *
from Player import *


class Menu(object):
    #--------------------Atributos--------------------
    _buttons: dict[Sprite]
    _logo: Sprite
    _sounds: dict[str]
    _music: Sound
    _select: Sprite

    #---------------------Métodos---------------------
    def __init__(self):
        self._buttons = {"play": Sprite("resources/menu/button_play.png"),
                         "stats": Sprite("resources/menu/button_stats.png"),
                         "rank": Sprite("resources/menu/button_rank.png"),
                         "exit": Sprite("resources/menu/button_exit.png")}
        self._logo = Sprite("resources/menu/logo.png")
        self._sounds = {"selected": "resources/music/selected.ogg",
                        "menu_bg": "resources/music/main_menu.ogg"}
        self._music = Sound(self._sounds["menu_bg"])
        self._select = Sprite("resources/menu/select.png")
        self._select.y = -self._select.height

    def get_buttons_name(self):
        return self._buttons.keys()

    def get_button(self, name: str):
        if(name in self._buttons.keys()):
            return self._buttons[name]

    def get_all_buttons(self):
        return self._buttons

    def set_button_position(self, name: str, x: int, y: int):
        if(name in self._buttons.keys()):
            self._buttons[name].x = x
            self._buttons[name].y = y

    def set_logo_position(self, x: int, y: int):
        self._logo.x = x
        self._logo.y = y

    """Define a posição do _select no botão informado"""
    def set_selected_over(self, name: str):
        if(name in self._buttons.keys()):
            self._select.x = self._buttons[name].x - (self._select.width / 2)
            self._select.y = self._buttons[name].y + ((self._buttons[name].height / 2) - (self._select.height / 2))

    """Organiza o layout dos botões/logo de acordo com o tipo (Main menu, rank ou stats)"""
    def organize(self, window: Window, type: str):
        if(type == "main"):
            self.set_logo_position((window.width / 2) - (self._logo.width / 2), 20)
            y_button = self._logo.y + self._logo.height + 30
            for name in self._buttons:
                self.set_button_position(name, (window.width / 2) - (self._buttons[name].width / 2), y_button)
                y_button += self._buttons[name].height + 15

    def play_bgm(self):
        if(not self._music.is_playing()):
            self._music.play()

    def play_selected(self):
        if(self._music.is_playing()):
            self._music.fadeout(500)
            self._music = Sound(self._sounds["selected"])
            self._music.play()
            

    def draw(self):
        self._logo.draw()
        self._select.draw()
        for i in self._buttons:
            self._buttons[i].draw()
        