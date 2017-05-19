#coding=utf-8 
import pygame
from pygame.locals import *
import global_member
import menu_scene
import map_scene
#游戏主循环类
class Game(object):   
#public    
    #获取输入
    def get_input(self):
        pass
    
    #帧移动
    def frame_move(self, passed_time):
        pass
    
    #渲染
    def render(self, passed_time):
        pass
#protect
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Azeal Python_tank")
        pygame.mixer.set_num_channels(15)
        pygame.mixer.pre_init(44100, 16, 2, 1024*4)
        #控制输入的频率
        self.passed_time = 0
        try:
            global_member.g_screen = pygame.display.set_mode((global_member.WINDOW_WIDTH, global_member.WINDOW_HEIGHT), HWSURFACE | SRCALPHA , 32)
        except:
            global_member.g_screen = pygame.display.set_mode((global_member.WINDOW_WIDTH, global_member.WINDOW_HEIGHT), SRCALPHA, 32)
        try:
            pygame.display.set_icon(pygame.image.load("data\\icon.png").convert_alpha())
        except:
            # some platfom do not allow change icon after shown
            pass
        global_member.g_active_scene = menu_scene.MenuScene()
   #     global_member.g_active_scene = map_scene.Map_Scene("data\\map\\0.map")

    def game_loop(self):
        time_clock = pygame.time.Clock()
        while True:
            passed_time = time_clock.tick(global_member.g_game_fps)
            if global_member.g_active_scene == None: continue

            if QUIT == global_member.g_active_scene.get_input():
                global_member.g_active_scene.release()
                break
            
            global_member.g_active_scene.frame_move(passed_time)
            
            global_member.g_active_scene.render(passed_time)
            
        pygame.display.quit()   
            
            
     
def run():
    GameApp = Game()
    GameApp.game_loop()  
        
