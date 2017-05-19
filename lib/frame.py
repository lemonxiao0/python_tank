#!/usr/bin/env python
#coding=utf-8

import pygame
from pygame.locals import *
import global_member
import util
import os
'''
主要是负责 tank的图片管理，应为tank的图片种类偏多 静止 移动 攻击 4个方向
'''
class Tank_Frame(object):
    def __init__(self):
        self.init_data()
        self.tank_name = None
        
    def load_tank_by_name(self, tank_name):
        self.tank_name = tank_name
        file_path = os.path.join(global_member.g_tank_path, tank_name)
        #move
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_MOVE][global_member.DIR_UP],   os.path.join(file_path, 'move', 'up\\'),     0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_MOVE][global_member.DIR_LEFT], os.path.join(file_path,  'move', 'left\\'),  0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_MOVE][global_member.DIR_DOWN], os.path.join(file_path, 'move', 'down\\'),   0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_MOVE][global_member.DIR_RIGHT],os.path.join(file_path, 'move', 'right\\'),  0,  1)
        #second load attack images
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_FIRE][global_member.DIR_UP],   os.path.join(file_path, 'attack', 'up\\'),    0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_FIRE][global_member.DIR_LEFT], os.path.join(file_path, 'attack', 'left\\'),  0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_FIRE][global_member.DIR_DOWN], os.path.join(file_path, 'attack', 'down\\'),  0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_FIRE][global_member.DIR_RIGHT],os.path.join(file_path, 'attack', 'right\\'), 0,  1)
        #third static images
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_STOP][global_member.DIR_UP],   os.path.join(file_path, 'direction', 'up\\'),    0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_STOP][global_member.DIR_LEFT], os.path.join(file_path, 'direction', 'left\\'),  0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_STOP][global_member.DIR_DOWN], os.path.join(file_path, 'direction', 'down\\'),  0,  1)
        util.load_all_image_to_array(self.tank_frames[global_member.ACTION_TYPE_STOP][global_member.DIR_RIGHT],os.path.join(file_path, 'direction', 'right\\'), 0,  1)
        
        
    def get_image_count(self, action_index, dir_index):
        return len(self.tank_frames[action_index][dir_index])
    
    def get_image_width(self):
        return self.tank_frames[0][0][0].get_width()
    
    def get_image_height(self):
        return self.tank_frames[0][0][0].get_height()
    
    def init_data(self):
        self.tank_frames = [[0 for dir in range(global_member.MAX_DIR)] for action in range(global_member.MAX_ACTION)]
        for dir in range(global_member.MAX_DIR):
            for action in range(global_member.MAX_ACTION):
                image_array_temp = []
                self.tank_frames[action][dir] = image_array_temp
                
    def draw(self, action_index, dir_index, current_index,  x_pos, y_pos):
        image = self.tank_frames[action_index][dir_index][current_index]
        self.rect = Rect(x_pos - self.get_image_width()/2, y_pos - self.get_image_height()/2, self.get_image_width(), self.get_image_height())
        
        global_member.g_screen.blit(image, self.rect)
 


class Tank_Frame_Manager:
    def __init__(self):
        self.default = 0
        self.tank_frame_array = []
    
    def __del__(self):
        print("__del__ Tank_Frame_Manager")
        del self.tank_frame_array[:]
    
    def load_tank_frame_by_index(self, tank_index):
        if tank_index >= len(self.tank_frame_array): tank_index = 0
        return self.tank_frame_array[tank_index]
    
    def init_data_Tank_Frames_Manager(self):
        if len(self.tank_frame_array) > 0 : return
        for index in range(global_member.g_tank_type_count):
            tank_frame_temp = Tank_Frame()
            tank_frame_temp.load_tank_by_name(str(index))
            self.tank_frame_array.append(tank_frame_temp)
            #进度
            global_member.g_active_scene.loading_scene_.set_show_percent(47 + index)
 
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
        
class Bullet_Frame(object):
    def __init__(self):
        self.init_data()
        
    def load_bullet_by_name(self, tank_name):
        file_path = os.path.join(global_member.g_bullet_path, tank_name)
        #move
        util.load_all_image_to_array(self.bullet_frames[global_member.DIR_UP],   os.path.join(file_path, 'up\\'),    0, 1)
        util.load_all_image_to_array(self.bullet_frames[global_member.DIR_LEFT], os.path.join(file_path, 'left\\'),  0, 1)
        util.load_all_image_to_array(self.bullet_frames[global_member.DIR_DOWN], os.path.join(file_path, 'down\\'),  0, 1)
        util.load_all_image_to_array(self.bullet_frames[global_member.DIR_RIGHT],os.path.join(file_path, 'right\\'), 0, 1)
       
        
    def get_image_count(self, dir):
        return len(self.bullet_frames[dir])
    
    def get_image_width(self, dir):
        return self.bullet_frames[dir][0].get_width()
    
    def get_image_height(self, dir):
        return self.bullet_frames[dir][0].get_height()
    
    def init_data(self):
        self.bullet_frames = [0 for dir in range(global_member.MAX_DIR)]
        for dir in range(global_member.MAX_DIR):
            image_array_temp = []
            self.bullet_frames[dir] = image_array_temp
                
    def draw(self, dir_index, current_index,  x_pos, y_pos):
        image = self.bullet_frames[dir_index][current_index]
        self.rect = Rect(x_pos - self.get_image_width(dir_index)/2, y_pos - self.get_image_height(dir_index)/2, self.get_image_width(dir_index), self.get_image_height(dir_index))
        
        global_member.g_screen.blit(image, self.rect)
    