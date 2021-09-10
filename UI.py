from Player import *
from PPlay.sprite import *
from PPlay.window import *

class UI(object):
    window: Window
    max_life: int
    life: float
    exp: float
    level: int
    life_sprite: list[Sprite]
    exp_sprite: Sprite
    level_sprite: Sprite

    def __init__(self, window, max_life, exp, level):
        self.window = window
        self.max_life = max_life
        self.life = max_life
        self.exp = exp
        self.level = level
        self.life_sprite = []
        for i in range(max_life):
            new_life = Sprite("resources/ui/life_sheet.png", 3)
            new_life.set_total_duration(500)
            new_life.x = (i * new_life.width) + 5
            new_life.y = 5
            self.life_sprite.append(new_life)

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


