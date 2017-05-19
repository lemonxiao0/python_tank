#!/usr/bin/env python
#coding=utf-8

import pygame
from pygame.locals import *
import scene
import global_member
import util

class Loading_Scene(scene.Scene):
    #获取输入
    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: return QUIT        
    
    #帧移动
    def frame_move(self, passed_time):
        pass
    
    #渲染
    def render(self, passed_time):
        self.passed_time += passed_time
        if self.passed_time > 1000/self.fps:
           if self.current_show_percent < self.percent: self.current_show_percent += 1
        else:
            self.passed_time = self.passed_time % (1000/self.fps)
        
        self.screen.blit(self.bk_ground, (0, 0))
        #显示文字
        str_show_list = self.show_text.split('\n')
        index = 0
        for value in str_show_list:
            font_surface_obj = self.font_obj.render(value, True, global_member.color_fonr)
            self.screen.blit(font_surface_obj, (self.show_text_x_pos, self.show_text_y_pos + font_surface_obj.get_height() * index))
            index += 1
        #显示百分比
        #首先显示百分号，再显示个位，再显示十位， 再显示百位
        hundred, decate, unit = (self.current_show_percent/100)%10, (self.current_show_percent/10)%10, self.current_show_percent%10
        self.screen.blit(self.numeral_image_array[10], (self.show_percent_x_pos - self.image_width/2, self.show_percent_y_pos - self.image_height/2 ))
        self.screen.blit(self.numeral_image_array[unit], (self.show_percent_x_pos - self.image_width- self.image_width/2, self.show_percent_y_pos- self.image_height/2))
        if decate != 0 or hundred != 0:
            self.screen.blit(self.numeral_image_array[decate], (self.show_percent_x_pos - self.image_width * 2- self.image_width/2, self.show_percent_y_pos- self.image_height/2))
        if hundred != 0:
            self.screen.blit(self.numeral_image_array[hundred], (self.show_percent_x_pos - self.image_width * 3- self.image_width/2, self.show_percent_y_pos- self.image_height/2))
        pygame.display.update()
        
    #释放资源， __del__ 有时候 __del__ 不好用的时候使用
    def release(self):
        pass
    
#protect
    #参数： 是否显示文字， 是否显示百分比
    def __init__(self, is_show_text, is_show_percent):
        scene.Scene.__init__(self)
        self.screen = global_member.g_screen
        self.show_text, self.percent, self.current_show_percent = u"", 0, 0
        self.show_text_x_pos, self.show_text_y_pos = 0, 0
        self.show_percent_x_pos, self.show_percent_y_pos = 0, 0
        self.bk_ground = pygame.image.load("data\\UI\\Loading.jpg")
        self.font_obj = pygame.font.Font("data\\font\\15.TTF", 40)
        self.is_show_text, self.is_show_percent =is_show_text, is_show_percent
        self.load_resources()
        self.fps = 25
        self.passed_time = 0
    
    def reset(self):
        self.show_text, self.percent, self.current_show_percent = u"", 0, 0
    
    def show_over(self):
        if self.current_show_percent == self.percent:
            return True
        return False
    
    def load_resources(self):
        self.numeral_image_array = []
        util.load_image_to_array(self.numeral_image_array, "data\\UI\\", 0, 10, 1)
        self.image_width, self.image_height = self.numeral_image_array[0].get_width(), self.numeral_image_array[0].get_height()
    
    def set_show_text(self, show_text):
        self.show_text = show_text
        
    def set_show_percent(self, percent):
        self.percent = percent
        
    def set_show_text_pos(self, x_pos, y_pos):
        self.show_text_x_pos, self.show_text_y_pos = x_pos, y_pos
    
    def set_show_percent_pos(self, x_pos, y_pos):
        self.show_percent_x_pos, self.show_percent_y_pos = x_pos, y_pos
        
        
        