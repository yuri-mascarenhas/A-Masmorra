from PPlay.sprite import *
from PPlay.window import *
from PPlay.sound import *
from Player import *

buttons = {"main": {"play": Sprite("resources/menu/button_play.png"),
                    "stats": Sprite("resources/menu/button_stats.png"),
                    "rank": Sprite("resources/menu/button_rank.png"),
                    "exit": Sprite("resources/menu/button_exit.png")},
           "stats": {"back": Sprite("resources/menu/button_back.png"),
                     "confirm": Sprite("resources/menu/button_confirm.png")}}

sub_buttons = {"str": {"plus": Sprite("resources/menu/button_plus.png", 2),
                       "minus": Sprite("resources/menu/button_minus.png", 2)},
               "vit": {"plus": Sprite("resources/menu/button_plus.png", 2),
                       "minus": Sprite("resources/menu/button_minus.png", 2)},
               "agi": {"plus": Sprite("resources/menu/button_plus.png", 2),
                       "minus": Sprite("resources/menu/button_minus.png", 2)}}

class Menu(object):
    #--------------------Atributos--------------------
    _window: Window
    _type: str
    _buttons: dict[Sprite]
    _sub_buttons: dict[Sprite]
    _logo: Sprite
    _text: dict[Sprite]
    _sounds: dict[str]
    _music: Sound
    _select: Sprite
    _stats: dict[int]

    #---------------------Métodos---------------------
    def __init__(self, window: Window, type: str):
        self._window = window
        self._type = type
        self._buttons = buttons[type]
        self._text = {"str": Sprite("resources/menu/text_str.png"),
                          "vit": Sprite("resources/menu/text_vit.png"),
                          "agi": Sprite("resources/menu/text_agi.png")}
        self._sub_buttons = sub_buttons
        self._logo = Sprite("resources/menu/logo.png")
        self._sounds = {"selected": "resources/music/selected.ogg",
                        "menu_bg": "resources/music/main_menu.ogg"}
        self._music = Sound(self._sounds["menu_bg"])
        self._select = Sprite("resources/menu/select.png")
        self._select.y = -self._select.height
        self.organize()

    def get_buttons_name(self):
        return self._buttons.keys()

    def get_sub_buttons_name(self):
        return self._sub_buttons.keys()

    def get_button(self, name: str):
        if(name in self._buttons.keys()):
            return self._buttons[name]

    def get_sub_button(self, name: str):
        return self._sub_buttons[name]

    def get_all_buttons(self):
        return self._buttons

    def get_texts_name(self):
        return self._text.keys()

    def get_text(self, name: str):
        return self._text[name]

    def get_stat(self, name: str):
        return self._stats[name]

    def get_stats(self):
        return self._stats

    def get_str(self):
        return self._stats["str"]

    def get_agi(self):
        return self._stats["agi"]

    def get_vit(self):
        return self._stats["vit"]

    def set_button_position(self, name: str, x: int, y: int):
        if(name in self._buttons.keys()):
            self._buttons[name].x = x
            self._buttons[name].y = y

    def set_stats(self, str: int, agi: int, vit: int):
        self._stats = {"str": str, "agi": agi, "vit": vit}

    def add_stat(self, stat: str, value: int):
        self._stats[stat] += value

    """Define as posições dos botões 'mais' e 'menos' onde cada um se distancia de dist do ponto x para esquerda ou para direita"""
    def set_sub_buttons_position(self, name: str, x: int, y: int, dist: int):
        self._sub_buttons[name]["minus"].y = y
        self._sub_buttons[name]["plus"].y = y
        self._sub_buttons[name]["minus"].x = x - dist - self._sub_buttons[name]["minus"].width
        self._sub_buttons[name]["plus"].x = x + dist

    def set_logo_position(self, x: int, y: int):
        self._logo.x = x
        self._logo.y = y

    def set_text_position(self,name: str, x: int, y: int):
        self._text[name].x = x
        self._text[name].y = y

    """Define a posição do _select no botão informado"""
    def set_selected_over(self, name: str):
        if(name in self._buttons.keys()):
            self._select.x = self._buttons[name].x - (self._select.width / 2)
            self._select.y = self._buttons[name].y + ((self._buttons[name].height / 2) - (self._select.height / 2))

    """Muda o sprite do sub-botão informado"""
    def set_sub_state(self, name: str, signal: str, selected: bool):
        if(selected):
            self._sub_buttons[name][signal].set_curr_frame(1)
        else:
            self._sub_buttons[name][signal].set_curr_frame(0)

    """Organiza o layout dos botões/logo de acordo com o tipo (Main menu, rank ou stats)"""
    def organize(self):
        if(self._type == "main"):
            self.set_logo_position((self._window.width / 2) - (self._logo.width / 2), 20)
            y_button = self._logo.y + self._logo.height + 30
            for name in self._buttons:
                self.set_button_position(name, (self._window.width / 2) - (self._buttons[name].width / 2), y_button)
                y_button += self._buttons[name].height + 15
        elif(self._type == "stats"):
            y_name = 50
            for name in self._text:
                self.set_text_position(name, (self._window.width / 6) - (self._text[name].width / 2), y_name)
                self.set_sub_buttons_position(name, self._window.width / 6, self._text[name].y + self._text[name].height + 30, 5)
                y_name = self._sub_buttons[name]["plus"].y + self._sub_buttons[name]["plus"].height + 75
            self.set_button_position("back", self._window.width * 2 / 3, (self._window.height / 2) + 50)
            self.set_button_position("confirm", self._window.width * 2 / 3, (self._window.height / 2) - self._buttons["confirm"].height - 50)

    def is_sub_pressed(self, name: str, signal: str):
        if(self._sub_buttons[name][signal].get_curr_frame() == 1):
            return True
        else:
            return False

    def play_bgm(self):
        if(not self._music.is_playing()):
            self._music = Sound(self._sounds["menu_bg"])
            self._music.play()

    def play_selected(self):
        if(self._music.is_playing()):
            self._music.fadeout(500)
            self._music = Sound(self._sounds["selected"])
            self._music.play()

    def draw(self):
        if(self._type == "main"):
            self._logo.draw()
        self._select.draw()
        for i in self._buttons:
            self._buttons[i].draw()
        if(self._type == "stats"):
            for i in self._sub_buttons:
                self._text[i].draw()
                self._sub_buttons[i]["plus"].draw()
                self._sub_buttons[i]["minus"].draw()
        