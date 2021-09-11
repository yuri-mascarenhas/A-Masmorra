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
    exp_sprite: Sprite
    life_sprite: list[Sprite]
    level_sprite: Sprite

    #---------------------Métodos---------------------
    def __init__(self, window, max_life, exp, level):
        self.window = window
        self.max_life = max_life
        self.life = max_life
        self.exp = exp
        self.level = level
        self.exp_sprite = Sprite("resources/ui/exp_bar2.png")
        self.exp_sprite.x = (window.width / 2) - (self.exp_sprite.width / 2)
        self.exp_sprite.y = window.height - self.exp_sprite.height
        self.life_sprite = []
        for i in range(max_life):
            new_life = Sprite("resources/ui/life_sheet.png", 3)
            new_life.set_total_duration(500)
            new_life.x = (i * new_life.width) + 5
            new_life.y = 5
            self.life_sprite.append(new_life)
    
    def set_exp(self, value: float):
        self.exp = value

    def add_exp(self, value: float):
        self.exp += value

    def level_up(self):
        self.level += 1

    def update_life_display(self, player: Player, value: float):
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

    def draw(self):
        for i in range(self.max_life):
            self.life_sprite[i].draw()
        pygame.draw.rect(self.window.screen, (86, 152, 204), 
                         (self.exp_sprite.x + 15, self.exp_sprite.y + 9, 370 * (self.exp / ((((self.level - 1)**2) * 15) + 55)), 5))
        self.exp_sprite.draw()



