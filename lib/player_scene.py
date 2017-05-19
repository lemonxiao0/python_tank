#!/usr/bin/env python
#coding=utf-8

import pygame
from pygame.locals import *
import threading
import scene
import map_scene
import global_member
import util
import loading_scene
import time

def thread_init_map_scene():
    print("begin load")
    print(global_member.g_active_scene)
    time.sleep(1)
    global_member.g_active_scene.map_scene = map_scene.Map_Scene(global_member.g_map_path + "\\" + str(global_member.g_active_scene.index_chapter) + ".map")
    if global_member.g_active_scene.map_scene.b_init_ok == False:
        global_member.go_to_scene("Menu")
        return;
    print("end load")
    global_member.g_active_scene.load_ok = True

class Player_Scene(scene.Scene):
    #获取输入
    def get_input(self):
        if self.load_ok == True and self.loading_scene_.show_over() == True: 
            return self.map_scene.get_input()
        else:
            return self.loading_scene_.get_input()
    
    #帧移动
    def frame_move(self, passed_time) :
        if self.load_ok == True and self.loading_scene_.show_over() == True :       
            self.map_scene.frame_move(passed_time)
        else:
            self.loading_scene_.frame_move(passed_time)
        
    #渲染
    def render(self, passed_time) :
        if self.load_ok == True and self.loading_scene_.show_over() == True:
            self.map_scene.render(passed_time)
        else:
            self.loading_scene_.render(passed_time)
    
    #释放资源
    def release(self):
        pass
    
    def __init__(self):
        scene.Scene.__init__(self)
        self.loading_scene_ = loading_scene.Loading_Scene(True, True)
        self.loading_scene_.set_show_text_pos(479, 660)
        self.loading_scene_.set_show_percent_pos(532, 245)
       #输赢    
        self.b_win, self.b_lost = False, False
       #地图scene
        self.map_scene = None
       #关卡
        self.index_chapter = 0
        self.chapter_enemy_count = 0
       #初始剩余机器生命
        self.player_tank_count = 3
        global_member.g_player_tank_life = self.player_tank_count
       #初始第一关
        self.init_data_Player_Scene()
       #加载完毕
        self.load_ok = False

    def __del__(self):
        del global_member.game_sprites_list[:]
        del global_member.g_bullet_manager.bullet_array[:]
        del global_member.g_explosion_manager.explosion_array[:]
        
    def start_next_chapter(self):
        self.index_chapter += 1
        del global_member.game_sprites_list[:]
        del global_member.g_bullet_manager.bullet_array[:]
        del global_member.g_explosion_manager.explosion_array[:]
        del global_member.g_font_manager.font_array[:]
        self.init_data_Player_Scene() 
        
    def init_data_Player_Scene(self):
        #显示等待界面
        self.load_ok = False
        self.loading_scene_.reset()
        #输赢    
        self.b_win, self.b_lost = False, False
        #根据关卡得这关总共有多少机器人, 每2关增加一个机器人，最高20个/初级版
        self.chapter_enemy_count = global_member.g_enemy_start_count + self.index_chapter/2 + 2
        if self.chapter_enemy_count > 20: self.chapter_enemy_count = 20
        #每局的敌军坦克总数 
        global_member.g_chapter_enemy_tank_count = self.chapter_enemy_count
        #需要等待刷新的敌军坦克数目
        global_member.g_enemy_wait_for_refresh = self.chapter_enemy_count - global_member.g_enemy_start_count
        #初始化此局打爆机器数
        global_member.g_enemy_have_smash = 0
        #输赢
        global_member.g_tank_win, global_member.g_tank_over = False, False
        #地图背景
        self.map_scene = None
        thread_map = threading.Thread(target = thread_init_map_scene, name = "map_scene")
        thread_map.start()
        print("threading is running")
        #self.map_scene = map_scene.Map_Scene(global_member.g_map_path + "\\" + str(self.index_chapter) + ".map")
        
    
    
    
    
