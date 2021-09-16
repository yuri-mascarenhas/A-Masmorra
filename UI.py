from Player import *
from PPlay.sprite import *
from PPlay.window import *

class UI(object):
    #--------------------Atributos--------------------
    window: Window
    max_life: int
    life: float
    exp: float
    level: int
    potion: int
    potion_level: int
    delay_clock: dict[float]
    delays: dict[float]
    exp_sprite: Sprite
    life_sprite: list[Sprite]
    potion_sprite: list[Sprite]
    level_sprite: Sprite

    #---------------------Métodos---------------------
    def __init__(self, window, max_life, exp, level):
        self.window = window
        self.max_life = max_life
        self.life = max_life
        self.exp = exp
        self.level = level
        self.potion = 0
        self.potion_level = 1
        self.delay_clock = {"potion": 0,
                            "buy": 0}
        self.delays = {"potion": 3,
                       "buy": 1.5}
        self.delays["potion"] = 3
        self.delay_clock["potion"] = 0
        self.exp_sprite = Sprite("resources/ui/exp_bar2.png")
        self.exp_sprite.x = (window.width / 2) - (self.exp_sprite.width / 2)
        self.exp_sprite.y = window.height - self.exp_sprite.height
        self.life_sprite = []
        self.potion_sprite = []
        for i in range(max_life):
            new_life = Sprite("resources/ui/life_sheet.png", 3)
            new_life.set_total_duration(500)
            new_life.x = (i * new_life.width) + 5
            new_life.y = 5
            self.life_sprite.append(new_life)
    
    def set_exp(self, value: float):
        self.exp = value

    def set_potion_level(self, level: int):
        self.potion_level = level
    
    def get_potion_level(self):
        return self.potion_level

    def add_exp(self, value: float):
        self.exp += value

    def set_potion(self, value: int):
        self.potion = value

    def add_potion(self):
        self.potion += 1
        self.potion_sprite.append(Sprite("resources/ui/potion_200.png"))
        for i in range(len(self.potion_sprite)):
            self.potion_sprite[i].x = self.window.width - self.potion_sprite[i].width - (self.potion_sprite[i].width * i / 2)
        self.delay_clock["buy"] = self.delays["buy"]

    def use_potion(self):
        if(self.potion > 0):
            self.potion -= 1
            self.potion_sprite.pop()
            self.delay_clock["potion"] = self.delays["potion"]

    def can_use_potion(self):
        if(self.delay_clock["potion"] <= 0):
            return True
        else:
            return False

    def can_buy(self):
        if(self.delay_clock["buy"] <= 0):
            return True
        else:
            return False

    def level_up(self):
        self.level += 1

    def update_life_display(self, type: str, player: Player, value: float):
        if(type == "damage"):
            if(self.life != player.get_life()):
                update_count = value / 0.5
                pos = len(self.life_sprite) - 1
                while((update_count > 0) and (pos >= 0)):
                    if(self.life_sprite[pos].get_curr_frame() == 2):
                        pos -= 1
                    else:
                        self.life_sprite[pos].update()
                        update_count -= 1
                self.life = player.get_life()
        elif(type == "heal"):
            heal = value * 0.5
            pos = 0
            while((pos < len(self.life_sprite)) and (heal > 0)):
                if(self.life_sprite[pos].get_curr_frame() == 0):
                    pos += 1
                elif(self.life_sprite[pos].get_curr_frame() == 1):
                    heal -= 0.5
                    self.life_sprite[pos].set_curr_frame(0)
                else:
                    heal -= 0.5
                    self.life_sprite[pos].set_curr_frame(1)

    def decrease_all_delay(self, delta_time):
        for i in self.delays:
            self.delay_clock[i] -= delta_time

    def draw(self):
        for i in range(self.max_life):
            self.life_sprite[i].draw()
        for i in range(self.potion):
            self.potion_sprite[i].draw()
        pygame.draw.rect(self.window.screen, (86, 152, 204), 
                         (self.exp_sprite.x + 15, self.exp_sprite.y + 9, 370 * (self.exp / ((((self.level - 1)**2) * 15) + 55)), 5))
        self.exp_sprite.draw()



