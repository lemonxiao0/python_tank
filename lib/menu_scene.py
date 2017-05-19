#coding=utf-8 
import scene
import pygame, sys
from pygame.locals import *

import global_member
'''
初始界面menu
'''

class MenuScene(scene.Scene):
    def __init__(self):
        self.init_data()
#public   
    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: return QUIT
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.select_item = (self.select_item - 1)%self.menu_items
                    self.play_select_music()
                elif event.key == K_DOWN:
                    self.select_item = (self.select_item + 1)%self.menu_items
                    self.play_select_music()
                elif event.key == K_RETURN:
                    if self.select_item == 0:
                        global_member.go_to_scene("Map")
                    elif self.select_item == 3:
                        return QUIT
                elif event.key == K_F1:
                    global_member.screen_shot()	
    
    #帧移动
    def frame_move(self, passed_time):
        pass
    
    #渲染
    def render(self, passed_time):
        if self.control_frame_rate(passed_time) == False: return
        self.screen.blit(self.bk_ground_image, (0, 0));
        for index in range(self.menu_items):
            n_item_width = self.menu_surface[index * 2].get_width()
            if index == self.select_item:
                self.screen.blit(self.menu_surface[index * 2 + 1], (self.start_x, self.start_y + (self.space_between) * index))
            else:
                self.screen.blit(self.menu_surface[index * 2], (self.start_x, self.start_y + (self.space_between) * index))
        self.show_font()
        global_member.g_font_manager.render(passed_time)
        pygame.display.update()
#protect
    def control_frame_rate(self, passed_time):
        self.passed_time += passed_time
        if self.passed_time >= 1000/self.fps:
            self.passed_time = self.passed_time % (1000/self.fps)
            return True
        return False
            
    def play_select_music(self):
        self.select_music.stop()
        self.select_music.play(0)
    
    #显示文字
    def show_font(self):
        str_show_list = self.font_item_state[self.select_item].split('\n')
        index = 0
        for value in str_show_list:
            font_surface_obj = self.font_obj.render(value, True, global_member.color_fonr)
            self.screen.blit(font_surface_obj, (global_member.menu_font_show_pos[0], global_member.menu_font_show_pos[1] + font_surface_obj.get_height() * index))
            index += 1
            
    def init_data(self):
        self.select_item = 0
        self.screen = global_member.g_screen
        self.start_x, self.start_y = global_member.menu_start_x, global_member.menu_start_y
        self.space_between = global_member.menu_button_between_space
        self.menu_surface = []
        self.menu_items = 0
        #挑战模式
        self.menu_surface.append(pygame.image.load("data\\UI\\ChallengeMode_0.png").convert_alpha())
        self.menu_surface.append(pygame.image.load("data\\UI\\ChallengeMode_1.png").convert_alpha())
        #剧情模式
        self.menu_surface.append(pygame.image.load("data\\UI\\DramaMode_0.png").convert_alpha())
        self.menu_surface.append(pygame.image.load("data\\UI\\DramaMode_1.png").convert_alpha())
        #高分
        self.menu_surface.append(pygame.image.load("data\\UI\\HiScore_0.png").convert_alpha())
        self.menu_surface.append(pygame.image.load("data\\UI\\HiScore_1.png").convert_alpha())
        #退出
        self.menu_surface.append(pygame.image.load("data\\UI\\ExitGame_0.png").convert_alpha())
        self.menu_surface.append(pygame.image.load("data\\UI\\ExitGame_1.png").convert_alpha())
        #item总共多少项
        self.menu_items = len(self.menu_surface)/2
        #背景
        self.bk_ground_image = pygame.image.load("data\\UI\\menu_bg.jpg").convert()
        #控制fps
        self.fps = global_member.g_menu_fps
        self.passed_time = 0
        #音乐
        pygame.mixer.music.load("data\\music\\menu_music.mp3")
        pygame.mixer.music.play(-1, 8)
        pygame.mixer.music.set_volume(0.8)
        self.select_music = pygame.mixer.Sound("data\\sound\\menuSelect.wav")
        #字体
        self.font_obj = pygame.font.Font("data\\font\\15.TTF", 20) 
        self.font_item_state = []
        self.font_item_state.append(global_member.szChallengeMode)
        self.font_item_state.append(global_member.szDramaMode)
        self.font_item_state.append(global_member.szHiScore)
        self.font_item_state.append(global_member.szExitGame)
        
    def release(self):
        pygame.mixer.music.stop()
        
         