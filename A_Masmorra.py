from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from Map import *
from Player import *
from Enemy import *

window = Window(800, 600)
keyboard = Window.get_keyboard()
mouse = Window.get_mouse()
window.set_title("A Masmorra")

bg = Sprite("assets/bg.png")
map = Map("maps/teste.txt", 13, 17)
player = Player(window, keyboard, mouse)
enemy = Enemy(window, keyboard, mouse)

#-------------------------Game Loop-------------------------
while(not keyboard.key_pressed("ESC")):
    # Update dos Game Objects

    # Draw dos Game Objects
    bg.draw()
    map.draw()
    player.move()
    enemy.move()
    player.draw()
    enemy.draw()
    window.update()
