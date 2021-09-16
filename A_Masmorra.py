from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from tile import *
from Map import *
from Player import *
from Enemy import *
from Menu import *
from UI import *
from Npc import *
import random

window = Window(800, 600)
keyboard = Window.get_keyboard()
mouse = Window.get_mouse()
window.set_title("A Masmorra")

tiles = Tileset([
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
small_maps = ["resources/maps/map_small_u_shape.txt",
              "resources/maps/map_small_trident.txt", 
              "resources/maps/map_small_square.txt",
              "resources/maps/map_small_random_shape.txt",
              "resources/maps/map_small_h_shape.txt"]
big_maps = ["resources/maps/map_big_random_shape.txt",
            "resources/maps/map_big_square.txt",
            "resources/maps/map_big_u_shape.txt",
            "resources/maps/map_medium_t_shape.txt",
            "resources/maps/map_mediun_l_shape.txt"]

state = "menu"
map_level = 1
level_started = False
bg = Sprite("assets/bg.png")
music = Sound("resources/music/play_theme.ogg")
player = Player()
main_menu = Menu(window, "main")
stats_menu = Menu(window, "stats")
stats_menu.set_stats(player.get_str(), player.get_agi(), player.get_vit())
map = Map(800, 600, 48, 48, tiles, 3)
wiz = Npc()
enemies = []
enemies_type = ["goblin", "zombie"]
start_delay = 4


#---------------------Funções Auxiliares---------------------
def move(key: str):
    if(player.can_move(map.get_layer(0), key)):
        player.move(key, map.get_grid_size())

def decrease_delays():
    player.decrease_all_delay(window.delta_time())
    ui.decrease_all_delay(window.delta_time())
    for i in range(len(enemies)):
        enemies[i].decrease_all_delay(window.delta_time())

def animations():
    player.move_animation(window.delta_time())
    player.attack_animation(window.delta_time())
    for i in range(len(enemies)):
        enemies[i].move_animation(window.delta_time())
    if(wiz.is_active()):
        wiz.summon_animation(window.delta_time(), map.get_grid_size())

def damage_control():
    for i in range(len(enemies)):
        if(player._weapon.collided(enemies[i].get_sprite()) and player.is_attacking()):
            enemies[i].get_damage(5 * player.get_str())
        if(player.get_sprite().collided(enemies[i].get_sprite())):
            player.get_damage(enemies[i].get_size() * 0.5)
            ui.update_life_display("damage", player, enemies[i].get_size() * 0.5)

def level_control():
    exp_to_next = (((player.get_level() - 1)**2) * 15) + 55
    if(player.get_exp() >= exp_to_next):
        player.level_up()
        player.add_points(1)
        player.set_exp(0)
        ui.level_up()
        ui.set_exp(0)

def enemies_draw():
    for i in range(len(enemies)):
        enemies[i].draw(window)

def clear_enemies():
    for i in range(len(enemies)):
        if(i < len(enemies)):
            if(enemies[i].get_life() <= 0):
                gain = (enemies[i].get_max_life() / 3) * enemies[i].get_size()
                player.add_exp(gain)
                ui.add_exp(gain)
                enemies.pop(i)

def npc_interaction():
    global map_level
    global level_started
    if(wiz.is_player_nearby(player, 1)):
        if(keyboard.key_pressed("E")):
            if(wiz.get_potions() > 0):
                if(ui.can_buy()):
                    ui.add_potion()
                    wiz.remove_potion()
        if(keyboard.key_pressed("F") and (wiz.is_active())):
            wiz.unsummon()
            wiz.set_active(False)
            level_started = False

def npc_dialogue():
    if(wiz.is_player_nearby(player, 1)):
        if(wiz.get_potions() > 0):
            window.draw_text("você pode comprar " + str(wiz.get_potions()) + " poções", wiz.get_sprite().x - 56, wiz.get_sprite().y - 42, size=14, color=(255,255,255), font_name="Arial", bold=False, italic=False)
            window.draw_text("pressione E para comprar", wiz.get_sprite().x - 56, wiz.get_sprite().y - 28, size=14, color=(255,255,255), font_name="Arial", bold=False, italic=True)
            window.draw_text("pressione F para ir para próxima fase", wiz.get_sprite().x - 56, wiz.get_sprite().y - 14, size=14, color=(255,255,255), font_name="Arial", bold=False, italic=True)
        else:
            window.draw_text("não há mais poções para compra", wiz.get_sprite().x - 56, wiz.get_sprite().y - 28, size=14, color=(255,255,255), font_name="Arial", bold=False, italic=False)
            window.draw_text("pressione F para ir para próxima fase", wiz.get_sprite().x - 56, wiz.get_sprite().y - 14, size=14, color=(255,255,255), font_name="Arial", bold=False, italic=True)

def show_stats():
    window.draw_text(str(stats_menu.get_str()), stats_menu.get_text("str").x + stats_menu.get_text("str").width + 20 , stats_menu.get_text("str").y - 5 , size=40, color=(255,100,100), font_name="Arial", bold=False, italic=True)
    window.draw_text(str(stats_menu.get_agi()), stats_menu.get_text("agi").x + stats_menu.get_text("agi").width + 20 , stats_menu.get_text("agi").y - 5 , size=40, color=(255,100,100), font_name="Arial", bold=False, italic=True)
    window.draw_text(str(stats_menu.get_vit()), stats_menu.get_text("vit").x + stats_menu.get_text("vit").width + 20 , stats_menu.get_text("vit").y - 5 , size=40, color=(255,100,100), font_name="Arial", bold=False, italic=True)

def change_stats_temp():
    for name in stats_menu.get_sub_buttons_name():
        if(mouse.is_over_object(stats_menu.get_sub_button(name)["plus"])):
            if(mouse.is_button_pressed(1)):
                if((not stats_menu.is_sub_pressed(name, "plus")) and (player.get_points() > 0)):
                    stats_menu.add_stat(name, 1)
                    player.remove_point()
                stats_menu.set_sub_state(name, "plus", True)
            else:
                stats_menu.set_sub_state(name, "plus", False)
        elif(mouse.is_over_object(stats_menu.get_sub_button(name)["minus"])):
            if(mouse.is_button_pressed(1)):
                if((not stats_menu.is_sub_pressed(name, "minus")) and (stats_menu.get_stat(name) != player.get_stats()[name])):
                    stats_menu.add_stat(name, -1)
                    player.add_points(1)
                stats_menu.set_sub_state(name, "minus", True)
            else:
                stats_menu.set_sub_state(name, "minus", False)

def summon_enemies():
    global enemies
    for i in range(map_level):
        new_enemy = Enemy(enemies_type[random.randint(0,1)], 1)
        enemies.append(new_enemy)
        enemies[i].set_initial_position(map.get_layer(0), map.get_grid_size(), player)


#-------------------------Game States-------------------------
def play():
    global state
    global map_level
    global level_started
    global enemies
    global music
    global start_delay

    # Inicialização
    if(not music.is_playing()):
        music = Sound("resources/music/play_theme.ogg")
        music.set_volume(15)
        music.play()
    if(not level_started):     
        if(map_level <= 10):
            index = random.randint(0, len(small_maps) - 1)
            map.load_map(small_maps[index])
        else:
            index = random.randint(0, len(big_maps) - 1)
            map.load_map(big_maps[index])  
        player.set_initial_position(map.get_layer(0), map.get_grid_size())
        summon_enemies()
        start_delay = 4
        map_level += 1
        level_started = True

    # Summon do NPC     
    if((len(enemies) == 0) and (not wiz.is_active()) and (map_level > 1)):
        wiz.set_position(map.get_layer(0), map.get_grid_size(), player)
        wiz.set_active()

    if(start_delay > 0):
        start_delay -= window.delta_time()
    else:
        # Update do Player
        if(keyboard.key_pressed("W")):
            move("u")
        elif(keyboard.key_pressed("A")):
            move("l")
        elif(keyboard.key_pressed("S")):
            move("d")
        elif(keyboard.key_pressed("D")):
            move("r")

        if((mouse.get_position()[0] < player.get_sprite().x) and (player.get_facing() == "right")):
            player.flip_sprite()
        if((mouse.get_position()[0] > player.get_sprite().x) and (player.get_facing() == "left")):
            player.flip_sprite()

        if(mouse.is_button_pressed(1)):
            player.attack()

        if(keyboard.key_pressed("SPACE")):
            if(ui.can_use_potion()):
                ui.use_potion()
                player.use_potion(ui.get_potion_level())
                ui.update_life_display("heal", player, ui.get_potion_level())

        # Updates Unificados
        decrease_delays()
        animations()
        damage_control()
        level_control()
        npc_interaction()

        # Update dos inimigos
        for i in range(len(enemies)):
            enemies[i].move(map.get_layer(0), map.get_grid_size(), player)
        clear_enemies()

        # Checkando game state
        if(player.get_life() <= 0):
            player.set_grid_position(0,0)
            map_level = 1
            level_started = False
            enemies = []
            music.fadeout(2000)
            state = "menu"

    # Draw dos Game Objects
    bg.draw()
    map.draw_layer(0)
    enemies_draw()
    if(player.can_move(map.get_layer(0), 'u')):
        player.draw()
        map.draw_layer(2)
    else:
        map.draw_layer(2)
        player.draw()
    wiz.draw()
    npc_dialogue()
    ui.draw()
    if(start_delay > 0):
        window.draw_text(str(int(start_delay)), (window.width / 2) - 25 , (window.height / 2) - 25, size=50, color=(255,255,255), font_name="Arial", bold=True, italic=False)
    window.update()

def menu():
    global state
    global ui
    # Update dos Game Objects
    for name in main_menu.get_buttons_name():
        if(mouse.is_over_object(main_menu.get_button(name))):
            main_menu.set_selected_over(name)
            if(mouse.is_button_pressed(1)):
                main_menu.play_selected()
                state = name
                if(name == "play"):
                    player.set_life(player.get_max_life())
                    ui = UI(window, player.get_max_life(), player.get_exp(), player.get_level())

                
    # Draw/play dos Game Objects
    main_menu.play_bgm()
    bg.draw()
    main_menu.draw()
    window.update()

def stats():
    global state

    # Update dos Game Objects
    for name in stats_menu.get_buttons_name():
        if(mouse.is_over_object(stats_menu.get_button(name))):
            stats_menu.set_selected_over(name)
            if(mouse.is_button_pressed(1)):
                stats_menu.play_selected()
                if(name == "back"):
                    unconfirmed_pts = 0
                    for i in stats_menu.get_stats():
                        if(stats_menu.get_stat(i) != player.get_stats()[i]):
                            unconfirmed_pts += abs(stats_menu.get_stat(i) - player.get_stats()[i])
                    player.add_points(unconfirmed_pts)
                    stats_menu.set_stats(player.get_str(), player.get_agi(), player.get_vit())
                    state = "menu"
                if(name == "confirm"):
                    player.set_stats(stats_menu.get_stat("str"), stats_menu.get_stat("agi"), stats_menu.get_stat("vit"))
    change_stats_temp()
    
    # Draw/play dos Game Objects
    stats_menu.play_bgm()
    bg.draw()
    stats_menu.draw()
    show_stats()
    window.draw_text("PTS: " + str(player.get_points()), stats_menu.get_button("confirm").x + 48, stats_menu.get_button("confirm").y - 24 , size=24, color=(100,255,100), font_name="Arial", bold=True, italic=False)
    window.update()

#-------------------------Game Loop-------------------------
while(state != "exit"):
    if(state == "menu"):
        menu()
    if(state == "play"):
        play()
    if(state == "stats"):
        stats()
