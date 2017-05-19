#!/usr/bin/env python
#coding=utf-8

import pygame
from pygame.locals import *
import global_member
import util
import sprite
import os

class Explosion(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        
    def start(self, x_pos, y_pos, image_array):
        self.init_sprite(x_pos, y_pos, image_array)
        
        self.set_fps(20)
        

class Explosion_Manager(object):
    def __init__(self):
        self.explosion_array = []
        self.explosion_frames = []
    #    self.init_data_Explosion_Manager()
        
    def __del__(self):
        del self.explosion_array[:]
        del self.explosion_frames[:]
        
    def start_explosion(self, x_pos, y_pos, explosion_index):
        explosion = Explosion()
        explosion.start(x_pos, y_pos, self.explosion_frames[explosion_index])
        self.explosion_array.append(explosion)
     
    def render(self):
        for value in self.explosion_array:
            if value.b_die == True:
                self.explosion_array.remove(value)
                break
        
        for value in self.explosion_array:
            value.draw()
    
    def frame_move(self, passed_time):
        for value in self.explosion_array:
            if value.b_die == False:
                 value.play_animation(passed_time)
    
    def release(self):
        del self.explosion_array[:]
        
    def init_data_Explosion_Manager(self):
        if len(self.explosion_frames) > 0:
            return        
        for index in range(global_member.g_explosion_count):
            image_array_temp = []
            util.load_all_image_to_array(image_array_temp, str(global_member.g_explosion_path)+"\\"+str(index)+"\\", 0, 1)
            self.explosion_frames.append(image_array_temp)

