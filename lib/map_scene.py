#coding=utf-8 

import pygame
from pygame.locals import *
import struct
from time import gmtime
from random import randint
import sprite
import tank
import scene
import frame
#全局使用的
import global_member
import util

class Map_Scene(scene.Scene):
    def __init__(self, map_file):
        self.b_init_ok = False
        self.b_init_ok = self.init_data(map_file)
        
    #获取输入
    def get_input(self):
        return self.player_tank.get_input()
        
    #帧移动
    def frame_move(self, passed_time):
        
        self.timer_refresh_enemy_tank(passed_time)
        self.timer_revive_player()
        
        self.player_tank.move(passed_time)
        for value in self.enmey_tank_array:
            value.move(passed_time)
        global_member.g_bullet_manager.move(passed_time)
        global_member.g_explosion_manager.frame_move(passed_time)
        
    #渲染
    def render(self, passed_time):
        self.screen.blit(self.map_bk_ground[self.bk_ground_index], (0, 0))
    #    global_member.game_sprites_group.update(passed_time)
        for value in global_member.game_sprites_list:
            value.draw()
        global_member.g_bullet_manager.render()
        global_member.g_explosion_manager.render()
        global_member.g_font_manager.render(passed_time)
        
        if global_member.g_tank_win == True: self.win_sprite.render(passed_time)
        elif global_member.g_tank_over == True:
            print("over") 
            self.over_sprite.render(passed_time)
        
        pygame.display.update()
        
    
    def __del__(self):
        print("__del__ map_scene")

        
#protect
    def init_data(self, map_file):
        self.screen = global_member.g_screen
        #这个时间是用来定时器，定期刷新敌军机器人和复活玩家
        self.refresh__enemy_time = 5000 #毫秒
        self.passed_time_refresh_enemy_tank = 0
        
        #坐标
        self.map_coord = [[0 for col in range(global_member.MAP_WIDTH)] for row in range(global_member.MAP_HIGHT)]
        for row in range(global_member.MAP_HIGHT):
            for col in range(global_member.MAP_WIDTH):
                self.map_coord[row][col] = (col*57 + 28, row*57 + 28)
        #界面元素
#        self.map_items_frame = []
#        util.load_image_to_array(self.map_items_frame, "data\\map_item\\", 0, 97, 1)
        global_member.g_active_scene.loading_scene_.set_show_text(u"加载地图元素")
        global_member.g_active_scene.loading_scene_.set_show_percent(5)
        if len(global_member.g_map_item_frame) == 0:
            util.load_image_to_array(global_member.g_map_item_frame, "data\\map_item\\", 0, 97, 1)
        
        if len(global_member.g_number) == 0:
            for index in range(5):
                images_temp = []
                util.load_image_to_array(images_temp, "data\\Number\\", 0 + index*12, 11 + index*12, 1)
                global_member.g_number.append(images_temp)
            
        
        #界面背景
        self.map_bk_ground = []
        util.load_image_to_array_(self.map_bk_ground, "data\\bk_ground\\", 0, 8, 1)
        
        global_member.g_active_scene.loading_scene_.set_show_text(u"初始化地图元素")
        global_member.g_active_scene.loading_scene_.set_show_percent(20)
        
        
        #加载地图
        try:
            map_file = open(map_file, mode = 'rb')
        except:
            self.b_init_ok = False
            return False
        self.bk_ground_index = struct.unpack('i', map_file.read(4))[0]
        for row in range(global_member.MAP_HIGHT):
            for col in range(global_member.MAP_WIDTH):
                object = sprite.Base_Object()
                n_image_index = struct.unpack('i', map_file.read(4))[0]
                if n_image_index == -1: continue
                object.init_object(self.map_coord[row][col][0], self.map_coord[row][col][1], global_member.g_map_item_frame[n_image_index])
                #object可以被子弹摧毁，但是不可以穿越
                if (n_image_index >= 0 and n_image_index <= 6) or (n_image_index >= 10 and n_image_index <= 31) or (n_image_index >= 40 and n_image_index <= 48):
                    object.flag |= global_member.OBJ_FLAG_ABLE_DESTROY
                #object可以被子弹穿越，但是不可以摧毁
                elif (n_image_index >= 7 and n_image_index <= 9) or (n_image_index >= 32 and n_image_index <= 39):
                    object.flag |= global_member.OBJ_FLAG_ABLE_THROUGH
                elif n_image_index == 75 or n_image_index == 76:
                    object.flag |= global_member.OBJ_FLAG_NO_HIT
                #老家
                elif n_image_index == 77:
                    object.flag |= global_member.OBJ_FLAG_MILITARYBASE | global_member.OBJ_FLAG_ABLE_DESTROY
                    #设置血量，显示血条
                    object.is_show_hp = True
                    object.hp, object.remain_hp = 150, 150
                    object.hp_show = sprite.Hp_Process()
                global_member.game_sprites_list.append(object)        
                if n_image_index >= 16 and n_image_index <= 59:
                    object.set_hit_offest(4, 4)
        print("地图加载完毕")
        #加载爆炸资源
        global_member.g_active_scene.loading_scene_.set_show_text(u"加载爆炸资源文件")
        global_member.g_active_scene.loading_scene_.set_show_percent(33)
        
        global_member.g_explosion_manager.init_data_Explosion_Manager()
        #加载子弹
        global_member.g_active_scene.loading_scene_.set_show_text(u"加载子弹资源文件")
        global_member.g_active_scene.loading_scene_.set_show_percent(39)
        
        global_member.g_bullet_manager.init_data_Bullet_Manager()
        #加载坦克资源
        global_member.g_active_scene.loading_scene_.set_show_text(u"加载坦克资源文件")
        global_member.g_active_scene.loading_scene_.set_show_percent(47)
        
        global_member.g_tank_manager.init_data_Tank_Frames_Manager()
        #加载胜利动画
        win_image_array = []
        win_image_array.append(pygame.image.load("data\\UI\\gamewin.png").convert_alpha())
        self.win_sprite = sprite.Game_Win_Over()
        self.win_sprite.init_sprite(global_member.WINDOW_WIDTH/2, global_member.WINDOW_HEIGHT + win_image_array[0].get_height(), win_image_array)
        self.win_sprite.move_to_pos(global_member.WINDOW_WIDTH/2, global_member.WINDOW_HEIGHT/3, 0, 3)
        self.win_sprite.fps = 60
        #加载失败动画
        over_image_array = []
        over_image_array.append(pygame.image.load("data\\UI\\gameover.png").convert_alpha())
        self.over_sprite = sprite.Game_Win_Over()
        self.over_sprite.init_sprite(global_member.WINDOW_WIDTH/2, global_member.WINDOW_HEIGHT + win_image_array[0].get_height(), over_image_array)
        self.over_sprite.move_to_pos(global_member.WINDOW_WIDTH/2, global_member.WINDOW_HEIGHT/3, 0, 3)
        self.over_sprite.fps = 60
        
        global_member.g_active_scene.loading_scene_.set_show_text(u"初始化玩家坦克，敌军坦克")
        global_member.g_active_scene.loading_scene_.set_show_percent(82)
                
        #玩家坦克 
        self.player_tank = tank.Player_Tank()
        self.player_tank.init_tank(self.map_coord[12][5][0], self.map_coord[12][5][1], 32 + randint(0, global_member.g_tank_type_count - 32 -1))
        #global_member.game_sprites_group.add(self.player_tank)
        global_member.game_sprites_list.append(self.player_tank)  
        #敌军[0][1],[0][6],[0][11],[0][16]
        self.enmey_tank_array = []
        for index in range(global_member.g_enemy_start_count):
            enemy_tank = tank.Enemy_Tank()
            enemy_tank.init_tank(self.map_coord[0][1 + index*5][0], self.map_coord[0][1 + index*5][1], randint(0, 31))
            self.enmey_tank_array.append(enemy_tank)
            global_member.game_sprites_list.append(enemy_tank) 
        
        #音乐
        global_member.g_active_scene.loading_scene_.set_show_text(u"加载音乐")
        global_member.g_active_scene.loading_scene_.set_show_percent(96)
        
        pygame.mixer.music.load("data\\music\\bg_2.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)
        
        global_member.g_active_scene.loading_scene_.set_show_text(u"初始化完毕")
        global_member.g_active_scene.loading_scene_.set_show_percent(100)
        self.b_init_ok = True
        
    #每隔三秒检测一次，如果还有敌军坦克没有出完，则初始一辆敌军坦克
    #返回坐标index, 没有返回 None
    def enemy_pos_birth_is_enable(self):
        list_enable_index = []
        for index in range(4):
            index_enable = True
            for value in global_member.game_sprites_list:
                if value.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK or \
                   value.sprite_type == global_member.SPRITE_TYPE_ENEMY_TANK:
                    if value.b_die == True: continue
                    if abs(self.map_coord[0][1 + index*5][0] - value.show_x_central_pos) < (57 + value.width - value.sprite_screen_offest_width*2)/2 and \
                       abs(self.map_coord[0][1 + index*5][1] - value.show_y_central_pos) < (57 + value.height - value.sprite_screen_offest_height*2)/2:
                       #此位置无效
                            index_enable = False
                            break
            if index_enable == True: list_enable_index.append(index)
        return list_enable_index
                                    
    def player_pos_birth_is_enable(self):
       for value in global_member.game_sprites_list:
           if value.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK or \
           value.sprite_type == global_member.SPRITE_TYPE_ENEMY_TANK:
               if value.b_die == True: continue
               if abs(self.map_coord[12][5][0] - value.show_x_central_pos) < (57 + value.width - value.sprite_screen_offest_width*2)/2 and \
                  abs(self.map_coord[12][5][1] - value.show_y_central_pos) < (57 + value.height - value.sprite_screen_offest_height*2)/2:
                 return True
       return False
                   
    def get_enemy_playing_count(self):
        count = 0
        for value in self.enmey_tank_array:
            if value.b_die != True:
                count += 1
        return count
        
        
    #定时函数，每 "三"秒检测一次，是否需要剩余机器人
    def timer_refresh_enemy_tank(self, passed_time):
        if global_member.g_enemy_wait_for_refresh == 0:
            return
        self.passed_time_refresh_enemy_tank += passed_time
        if self.passed_time_refresh_enemy_tank > self.refresh__enemy_time:
            self.passed_time_refresh_enemy_tank = self.passed_time_refresh_enemy_tank%self.refresh__enemy_time
            if self.get_enemy_playing_count() >= global_member.g_contain_max_enemy: return
            list_pos_index = self.enemy_pos_birth_is_enable()
            print(list_pos_index)
            for index in list_pos_index:
                enemy_tank = tank.Enemy_Tank()
                enemy_tank.init_tank(self.map_coord[0][1 + index*5][0], self.map_coord[0][1 + index*5][1], randint(1, 31))
                self.enmey_tank_array.append(enemy_tank)
                global_member.game_sprites_list.append(enemy_tank) 
                #剩余等待刷新的 -1或者存活数目上限
                global_member.g_enemy_wait_for_refresh -= 1
                if global_member.g_enemy_wait_for_refresh == 0 or self.get_enemy_playing_count() == global_member.g_contain_max_enemy:
                    return
    
    def timer_revive_player(self):
        if self.player_tank.b_die == True and global_member.g_player_tank_life > 0 and abs(gmtime().tm_sec - self.player_tank.die_sec) > 2:
            self.player_tank.b_die = False
            self.player_tank.set_position(self.map_coord[12][5][0], self.map_coord[12][5][1])
            self.player_tank.set_dir(global_member.DIR_UP)
            self.player_tank.set_action(global_member.ACTION_TYPE_STOP)
            self.remain_hp = self.hp
                        
    def release(self):
        pygame.mixer.music.stop()
