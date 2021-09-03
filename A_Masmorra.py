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
player = Player()
player.set_initial_position(map.get_layer(0), map.get_grid_size())
enemy = Enemy("goblin", 1, 3)
enemy.set_initial_position(map.get_layer(0), map.get_grid_size(), player)



#-------------------------Game Loop-------------------------
while(not keyboard.key_pressed("ESC")):
    # Update do Player
    if(keyboard.key_pressed("W")):
        if(player.can_move(map.get_layer(0),"u")):
            player.move("u", map.get_grid_size())
    if(keyboard.key_pressed("A")):
        if(player.can_move(map.get_layer(0), "l")):
            player.move("l", map.get_grid_size())
    if(keyboard.key_pressed("S")):
        if(player.can_move(map.get_layer(0), "d")):
            player.move("d", map.get_grid_size())
    if(keyboard.key_pressed("D")):
        if(player.can_move(map.get_layer(0), "r")):
            player.move("r", map.get_grid_size())
    player.decrease_move_delay(window.delta_time())
    player.move_animation(window.delta_time())
    
    # Update dos inimigos
    enemy.move(map.get_layer(0), map.get_grid_size(), player)
    enemy.move_animation(window.delta_time())
    enemy.decrease_move_delay(window.delta_time())

    # Draw dos Game Objects
    bg.draw()
    map.draw_layer(0)
    map.draw_layer(2)
    enemy.draw()
    player.draw()
    window.update()
