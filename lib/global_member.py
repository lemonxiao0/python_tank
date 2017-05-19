#coding=utf-8
import pygame 
from time import gmtime
from random import randint
import menu_scene
import player_scene
import bullet
import explosion
import frame
import sprite
import time
import os
'''
这里定义的是全局的变量，方便直接使用的哦
'''

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 768

'''
地图宽高(格子数) 格子大小为 57 x 57 像素
'''
MAP_WIDTH  = 18
MAP_HIGHT  = 14

'''
动作类型定义
'''
MAX_ACTION = 3 #坦克动作(行,停,开炮)
MAX_DIR    = 4 #方向数(上下左右)


ACTION_TYPE_STOP = 0	#停止
ACTION_TYPE_MOVE = 1	#走动
ACTION_TYPE_FIRE = 2	#开炮

DIR_UP    = 0	#上
DIR_LEFT  = 1	#左
DIR_DOWN  = 2	#下
DIR_RIGHT = 3	#右


'''
游戏对象特征标志
'''
OBJ_FLAG_ABLE_DESTROY = 1 #对象可摧毁
OBJ_FLAG_ABLE_THROUGH = 2 #对象可穿越
OBJ_FLAG_MILITARYBASE = 4 #玩家基地
OBJ_FLAG_NO_HIT       = 8 #不会和任何单位产生碰撞，地图地面装饰物,任何对象x可穿越

'''
游戏对象类型
'''
SPRITE_TYPE_PLAYER_TANK = 1 #玩家
SPRITE_TYPE_ENEMY_TANK  = 2 #敌军坦克


        
'''
menu_scene 用到得变量
'''        
menu_start_x, menu_start_y = 410, 310
menu_button_between_space = 50
menu_font_show_pos = (5, 668)

szChallengeMode = u"闯关防守模式，玩家在进攻的同时要防守好基地\n\
操作说明:\n\
键盘：方向键  ----  控制移动                    空格键 ---- 发射炮弹"

szDramaMode = u"此功能尚未开发，敬请期待！";

szHiScore = u"显示玩家历史分数记录。";

szExitGame = u"此游戏使用python开发，如果您对此感兴趣，可找作者lemonxiao0@163.com 索取源码\n\
不用python写游戏啦, 太麻烦了. 这只是一个简易版的demon。"

color_fonr = (255, 255, 255)
'''
所有界面显示都要用到的screen
'''
g_screen = None
g_active_scene = None


def go_to_scene(strName):
    global g_active_scene, g_font_manager
    g_active_scene.release()
    g_active_scene = None
    g_font_manager.clear()
    if strName == "Menu":
        g_active_scene = menu_scene.MenuScene()
    elif strName == "Map":
        g_active_scene = player_scene.Player_Scene()
    else:
        pass

'''
截屏使用的
'''
def screen_shot():
    global g_screen
    str_file_path = ''
    if os.path.exists("Screen_Shot") == False: os.mkdir("Screen_Shot");
    while True:
        n_randint = randint(0, 100);
        str_file_path = os.path.join("Screen_Shot", time.strftime('%Y-%m-%d %H%M%S ',time.localtime(time.time()))) + str(n_randint) + str(".png")
        if os.path.exists(str_file_path) == False:
            break
        
    pygame.image.save(g_screen, str_file_path)
    g_font_manager.start(str("Screen_Shot: ") + str_file_path, 600, 140, 20, color = (54, 133, 252), speed_x = 0, speed_y = -2)
    #g_font_manager.start_image(520, 600, 20, 20, 4, speed_x = randint(-3, 3), speed_y = 4)            
'''
控制界面的刷新帧
menu_fps 30 主循环是控制帧在70，这个帧已经很快，基本超过人得视觉范围
从主界面传进来时间，和自己的以过时间相加，看是否 大于 1000/menu_fps ,大于说明时间到了，得刷新，保留 总时间%81000/menu_fps)
'''
g_game_fps = 60
g_menu_fps = 30
g_map_bk_ground_fps = 30

'''
存放所有的sprite
'''
game_sprites_group = pygame.sprite.Group()
game_sprites_list = []

'''
坦克的路径
'''
g_map_path = "data\\map"
g_tank_path = "data\\tank_modle"
g_bullet_path = "data\\bullet"
g_explosion_path = "data\\explosion"


'''
管理frane的，一次加载，之后直接使用，无需重新加载，速度优先嘛
'''
g_font_manager = sprite.Font_Manager()
g_bullet_manager = bullet.Bullet_Manager()
g_explosion_manager = explosion.Explosion_Manager()
g_tank_type_count = 33 #坦克的种类
g_tank_manager = frame.Tank_Frame_Manager()
g_map_item_frame = []
g_number = []   #数字
'''
子弹和爆炸的种类数目
'''
g_bullet_count = 4
g_explosion_count = 4

'''
初始敌军塔克数目
'''
g_enemy_start_count = 4     #一般不变
'''
还要刷新出多少敌军坦克
'''
g_enemy_wait_for_refresh = 0   #实时改变, 开局初始化
'''
每张地图容许存在的基本的最高敌军坦克数目
'''
g_contain_max_enemy = 6    #不变
'''
这一局已经打爆了多少机器人
'''
g_enemy_have_smash = 0    #实时改变
'''
'''
g_player_tank_life = 3    #实时改变
g_chapter_enemy_tank_count = 0 #每局开始初始化

g_tank_win, g_tank_over = False, False


#提供几个常用的函数

#子弹攻击基地 参数： 子弹伤害，谁攻击的
#
#子弹攻击坦克 参数：子弹, 被攻击坦克value
def bullet_hit_tank(bullet, hit_object):
    global g_enemy_have_smash, g_player_tank_life, g_explosion_manager,  g_tank_win, g_tank_over
    #玩家攻击、敌军攻击敌军，直接pass, 不管
    bullet_damage = bullet.get_bullet_damage()
    b_crit = False
    if bullet.from_sprite.sprite_type == hit_object.sprite_type: 
        return
    else:
        if bullet.from_sprite.sprite_type == SPRITE_TYPE_PLAYER_TANK:
            if bullet.from_sprite.Is_Crit() == True:
                  bullet_damage *= 3 
                  b_crit = True
        hit_object.remain_hp -= bullet_damage
        if hit_object.sprite_type == SPRITE_TYPE_ENEMY_TANK and hit_object.remain_hp < 0:
            g_enemy_have_smash += 1     #这局打爆坦克数目
            hit_object.b_die = True
            hit_object.remain_hp = hit_object.hp
        elif hit_object.sprite_type == SPRITE_TYPE_PLAYER_TANK and hit_object.remain_hp < 0: 
            g_player_tank_life -= 1
            hit_object.die_sec = gmtime().tm_sec
            hit_object.b_die = True
            hit_object.remain_hp = hit_object.hp
    
    if hit_object.b_die == True:
        g_explosion_manager.start_explosion(hit_object.show_x_central_pos, hit_object.show_y_central_pos, 2)
    else:
        g_explosion_manager.start_explosion(hit_object.show_x_central_pos, hit_object.show_y_central_pos, 3)
    
    #玩家坦克，检测暴击
    
    if b_crit == True:
        #g_font_manager.start(str(bullet_damage), 1000, hit_object.show_x_central_pos, hit_object.show_y_central_pos, color = (255, 0, 0))
        g_font_manager.start_image(bullet_damage, 600, hit_object.show_x_central_pos, hit_object.show_y_central_pos, 4, speed_x = randint(-3, 3), speed_y = 4)
    else:
        #g_font_manager.start(str(bullet_damage), 500, hit_object.show_x_central_pos, hit_object.show_y_central_pos)
       g_font_manager.start_image(bullet_damage, 200, hit_object.show_x_central_pos, hit_object.show_y_central_pos, 0, speed_x = randint(-2, 2), speed_y = 3)
    print(bullet_damage)
    if g_player_tank_life == 0:
        g_tank_over = True
    elif g_chapter_enemy_tank_count == g_enemy_have_smash:
        g_tank_win = True


        

#子弹攻击坦克 参数：子弹, 基地组织
#子弹打基地有暴击效果
def bulet_hit_military_base(bullet, hit_object):
    global g_tank_over
    bullet_damage = bullet.get_bullet_damage()
    b_crit = False
    if bullet.from_sprite.sprite_type == SPRITE_TYPE_PLAYER_TANK:
        if bullet.from_sprite.Is_Crit() == True:
            bullet_damage *= 3 
            b_crit = True
    
    if bullet.from_sprite.sprite_type == SPRITE_TYPE_ENEMY_TANK:
        print("enemy attack me")
    else:
        print("i do known")
    
    hit_object.remain_hp -= bullet_damage
    if hit_object.remain_hp < 0:
        g_tank_over = True
        hit_object.remain_hp = 0
    #显示伤害，暴击了，杂事红色
    if b_crit == True:
        #g_font_manager.start(str(bullet_damage), 1000, hit_object.show_x_central_pos, hit_object.show_y_central_pos, color = (255, 0, 0))
        g_font_manager.start_image(bullet_damage, 400, hit_object.show_x_central_pos, hit_object.show_y_central_pos, 2, speed_x = 2, speed_y = 3)
    else:
        #g_font_manager.start(str(bullet_damage), 500, hit_object.show_x_central_pos, hit_object.show_y_central_pos)
        g_font_manager.start_image(bullet_damage, 400, hit_object.show_x_central_pos, hit_object.show_y_central_pos, 2, speed_x = 2, speed_y = 3)
        
        
    
    
    
