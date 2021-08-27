from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from tile import *
from Map import *
from Player import *
from Enemy import *

window = Window(800, 600)
keyboard = Window.get_keyboard()
mouse = Window.get_mouse()
window.set_title("A Masmorra")

tiles = wall_tileset = Tileset([
    Tile("resources/tiles/floor/floor_1.png", 1, 0),
    Tile("resources/tiles/floor/floor_2.png", 1, 0),
    Tile("resources/tiles/floor/floor_3.png", 1, 0),
    Tile("resources/tiles/wall/wall_corner_bottom_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_bottom_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_front_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_front_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_corner_top_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_fountain_top.png", 1, 2),
    Tile("resources/tiles/wall/wall_hole_1.png", 1, 2),
    Tile("resources/tiles/wall/wall_hole_2.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_l_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_l_top_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_mid_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_mid_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_t_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_inner_corner_t_top_rigth.png", 1, 2),
    Tile("resources/tiles/wall/wall_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_mid.png", 1, 2),
    Tile("resources/tiles/wall/wall_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_front_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_front_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_mid_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_mid_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_side_top_right.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_left.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_mid.png", 1, 2),
    Tile("resources/tiles/wall/wall_top_right.png", 1, 2)
    ])


bg = Sprite("assets/bg.png")
map = Map(800, 600, 48, 48, tiles, 3)
player = Player(window, keyboard, mouse)
enemy = Enemy("assets/enemies/orc_boss_idle_sheet.png", window, keyboard, mouse)

player.set_position(400,300)
#-------------------------Game Loop-------------------------
while(not keyboard.key_pressed("ESC")):
    # Update dos Game Objects
    if(keyboard.key_pressed("W")):
        if(player.can_move(map.get_layer(0), map.get_grid_size(),"u")):
            player.move("u")
    if(keyboard.key_pressed("A")):
        if(player.can_move(map.get_layer(0), map.get_grid_size(),"l")):
            player.move("l")
    if(keyboard.key_pressed("S")):
        if(player.can_move(map.get_layer(0), map.get_grid_size(),"d")):
            player.move("d")
    if(keyboard.key_pressed("D")):
        if(player.can_move(map.get_layer(0), map.get_grid_size(),"r")):
            player.move("r")
        

    # Draw dos Game Objects
    bg.draw()
    map.draw_layer(0)
    player.draw()
    map.draw_layer(2)
    window.update()
