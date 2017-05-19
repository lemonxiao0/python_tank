#coding=utf-8 
import pygame
from pygame.locals import *

import util
import global_member

#静态，大多数是用来显示地图背景
class Base_Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.init_data()
    
    def init_object(self, x_pos, y_pos, image):
        self.show_x_central_pos, self.show_y_central_pos, self.image = x_pos, y_pos, image
        self.rect.w, self.rect.h = self.image.get_width(), self.image.get_height()
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2
        self.width, self.height = self.rect.w, self.rect.h

    #设置显示图片的中心
    def set_position(self, x_pos, y_pos):
        self.show_x_central_pos, self.show_y_central_pos = x_pos, y_pos
    
    #设置死亡状态
    def set_die(self, bDie):
        self.b_die = bDie
    
    #获取类型
    def get_sprite_type(self):
        return self.sprite_type
    
    def set_sprite_type(self, type):
        self.sprite_type = type
    
    def update(self, passed_time):
        pass
    
    def draw(self):
        hul_index = 0
        if self.b_die == True: return
        global_member.g_screen.blit(self.image, self.rect)
        if self.is_show_hp == True:
            if self.flag & global_member.OBJ_FLAG_MILITARYBASE: hul_index = 2
            elif self.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK: hul_index = 1
            elif self.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK: hul_index = 1            
            self.hp_show.show_pos(self.show_x_central_pos, self.show_y_central_pos - 30, (self.remain_hp * 100) / self.hp, hul_index)
    
    def set_hit_offest(self, offest_width, offest_height):
        self.sprite_screen_offest_width, self.sprite_screen_offest_height = offest_width, offest_height
        
    def init_data(self):
        self.screen = global_member.g_screen
        self.show_x_central_pos = 0
        self.show_y_central_pos = 0
        self.width = 0
        self.height = 0
        self.flag  = 0  #是否破坏，可穿越
        self.sprite_type = 0 #玩家坦克还是敌军
        self.image = None
        self.rect  = Rect(0, 0, 0, 0)
        self.b_die = False #是否死亡
        self.die_sec = 0 #主要是用来复活玩家坦克使用的 秒单位 
        self.sprite_screen_offest_width, self.sprite_screen_offest_height = 0, 0
        #血量，只有基地和坦克等部分单位有这个属性，其余的地图装饰物是木有哦
        self.hp , self.remain_hp= 0, 0
        self.hp_show = None     #血条显示类
        self.is_show_hp = False #是否显示血条

#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#动态的
class Sprite(Base_Object):
    def __init__(self):
        Base_Object.__init__(self)
        self.init_data_Sprite()
        
    def init_sprite(self, x_pos, y_pos, image_array):
        self.show_x_central_pos, self.show_y_central_pos, self.images_array = x_pos, y_pos, image_array
        self.image = self.images_array[self.current_index + 1]
        self.rect.w, self.rect.h = self.image.get_width(), self.image.get_height()
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2
        self.width, self.height = self.rect.w, self.rect.h
        self.image_count = len(self.images_array)
    
    def set_fps(self, fps):
        self.fps = fps
    
    def set_animation_loop(self, b_loop):
        self.b_animation_loop = b_loop
    
    def play_animation(self, passed_time):
        if self.b_die == True: return
        self.passed_time += passed_time
        if self.passed_time >= 1000/self.fps:
            self.current_index += 1
            self.passed_time = self.passed_time % (1000/self.fps)
            if self.current_index >= self.image_count:
                if self.b_animation_loop == False:
                    self.b_die = True
                self.current_index = 0
            

    def update(self, passed_time):
        self.play_animation(passed_time)
    
    def draw(self):
        if self.b_die == True: return
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2
        self.screen.blit(self.images_array[self.current_index], self.rect)
        if self.is_show_hp == True:
            self.hp_show.show_pos(self.show_x_central_pos, self.show_y_central_pos - 30, (self.remain_hp * 100) / self.hp)
        
    def init_data_Sprite(self):
        self.images_array = []
        self.current_index = -1
        self.image_count = 0
        self.fps = 0  
        self.b_animation_loop = False
        self.passed_time = 0
        self.images_array = []
        self.image = None
        self.rect  = Rect(0, 0, 0, 0)
        
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************

#移动的精灵
class Move_Sprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.init_data_Move_Sprite()
        
    def set_speed(self, speed):
       self.speed = speed
    
    #设置移动的方向
    def set_dir(self, dir):
        if dir < global_member.MAX_DIR and dir != self.dir:
            self.dir, self.current_index = dir, 0
    
    def set_action(self, action):
        if action < global_member.MAX_ACTION and action != self.current_action:
            self.current_action, self.current_index = action, 0
    
    def hit_test_other_sprite(self):
        hit_list = []        
        for value in global_member.game_sprites_list:
            if abs(self.show_x_central_pos - value.show_x_central_pos) < (self.width - self.sprite_screen_offest_width*2 + value.width - value.sprite_screen_offest_width*2)/2 and \
                abs(self.show_y_central_pos - value.show_y_central_pos) < (self.height - self.sprite_screen_offest_height*2 + value.height - value.sprite_screen_offest_height*2)/2:
                if value != self and value.b_die == False and value.flag & global_member.OBJ_FLAG_NO_HIT  <= 0:
                    hit_list.append(value)
        if len(hit_list) == 0: return None    
        else: return hit_list
#protect
    def move_up(self):
        self.set_action(global_member.ACTION_TYPE_MOVE)
        if self.dir != global_member.DIR_UP:
            self.move_speed_y, self.move_speed_x = 0, 0
            self.set_dir(global_member.DIR_UP)
        else:
            self.move_speed_y, self.move_speed_x = -self.speed, 0
    
    def move_left(self):
        self.set_action(global_member.ACTION_TYPE_MOVE)
        if self.dir != global_member.DIR_LEFT:
            self.move_speed_x, self.move_speed_y = 0, 0
            self.set_dir(global_member.DIR_LEFT)
        else:
            self.move_speed_x, self.move_speed_y =  -self.speed, 0
    
    def move_down(self):
        self.set_action(global_member.ACTION_TYPE_MOVE)
        if self.dir != global_member.DIR_DOWN:
            self.move_speed_x, self.move_speed_y  = 0, 0
            self.set_dir(global_member.DIR_DOWN)
        else:
            self.move_speed_y, self.move_speed_x =  self.speed, 0
        
        
    def move_right(self):
        self.set_action(global_member.ACTION_TYPE_MOVE)
        if self.dir != global_member.DIR_RIGHT:
            self.move_speed_x, self.move_speed_y =  0, 0
            self.set_dir(global_member.DIR_RIGHT)
        else:
            self.move_speed_x, self.move_speed_y = self.speed, 0

        
    def stop_move(self):
        self.move_speed_x, self.move_speed_y = 0, 0
        
    def move(self, passed_time):
        if self.b_die == True: return
        
        if self.move_speed_x == 0 and self.move_speed_y == 0 :
            if self.current_action == global_member.ACTION_TYPE_FIRE: self.play_animation(passed_time)
            else: return
        
        self.play_animation(passed_time)
        
        self.show_x_central_pos += self.move_speed_x
        self.show_y_central_pos += self.move_speed_y
        
        #是否碰撞了
        if self.hit_test_other_sprite() != None:
            self.show_x_central_pos -= self.move_speed_x
            self.show_y_central_pos -= self.move_speed_y
            return
        
        # 移动范围限制在窗口范围内
        if self.show_x_central_pos <= self.screen_test_width :
        	self.show_x_central_pos = self.screen_test_width
        if self.show_x_central_pos >= global_member.WINDOW_WIDTH - self.screen_test_width:
            self.show_x_central_pos = global_member.WINDOW_WIDTH - self.screen_test_width
        if self.show_y_central_pos <= self.screen_test_height:
            self.show_y_central_pos = self.screen_test_height
        if self.show_y_central_pos >= global_member.WINDOW_HEIGHT - self.screen_test_height:
            self.show_y_central_pos = global_member.WINDOW_HEIGHT - self.screen_test_height
     
    def draw(self):
        if self.b_die == True:
            return
        
    def init_data_Move_Sprite(self):
        self.move_speed_x, self.move_speed_y, self.speed = 0, 0, 0
        self.screen_test_width, self.screen_test_height = 0, 0
        self.current_action = global_member.ACTION_TYPE_STOP
        self.dir = global_member.DIR_UP
        #需要4个方向的surface数组
        
        
 
class Game_Win_Over(Sprite):
    def __init__(self):
       Sprite.__init__(self)
       self.speed_x, self.speed_y = 0, 0
       self.show_des_x_pos, self.show_des_y_pos = 0, 0
       
       
    def move_to_pos(self, des_x_pos, des_y_pos, speed_x, speed_y):
       self.show_des_x_pos = des_x_pos
       self.show_des_y_pos = des_y_pos
       self.speed_x, self.speed_y = speed_x, speed_y
    
    def play_animation(self, passed_time):
       if self.b_die == True: return
       self.passed_time += passed_time
       if self.passed_time >= 1000/self.fps:
           self.current_index += 1
           self.passed_time = self.passed_time % (1000/self.fps)
           self.show_x_central_pos += self.speed_x
           self.show_y_central_pos -= self.speed_y
           if self.show_x_central_pos >  self.show_des_x_pos: self.show_x_central_pos = self.show_des_x_pos
           if self.show_y_central_pos <  self.show_des_y_pos: self.show_y_central_pos = self.show_des_y_pos
           if self.current_index >= self.image_count:
               self.current_index = 0
    
    def render(self, passed_time):
        self.play_animation(passed_time)
        Sprite.draw(self)
        
        
#显示数字和文字
#坦克攻击坦克的时候，有数字伤害冒出来
#普通的伤害 蓝色、 暴击的事红色
class Font(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.font_obj = pygame.font.Font("data\\font\\15.TTF", 20) 
        self.font_arrary = []
        self.life_time = 0
    #毫秒
    def start(self, str_show, stand_sec, x_pos, y_pos, color = (63, 72, 204), speed_x = 0, speed_y = 2):
        self.life_time = stand_sec
        font_surface_obj = self.font_obj.render(str_show, True, color)
        self.show_x_central_pos, self.show_y_central_pos = x_pos, y_pos
        self.images_array.append(font_surface_obj)
        self.image = self.images_array[self.current_index + 1]
        self.rect.w, self.rect.h = self.font_obj.size(str_show)[0], self.font_obj.size(str_show)[1] 
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2   
        self.image_count = 1
        self.fps = 30
        #设置向y轴移动
        self.speed_y, self.speed_x = speed_y, speed_x
        print(self.speed_y)
    
        
    def play_animation(self, passed_time):
       if self.b_die == True: return
       self.passed_time += passed_time
       if self.passed_time >= 1000/self.fps:
           self.life_time -= passed_time
           if self.life_time < 0: self.b_die = True
           self.current_index += 1
           self.show_x_central_pos -= self.speed_x
           self.show_y_central_pos -= self.speed_y
           self.passed_time = self.passed_time % (1000/self.fps)
           if self.current_index >= self.image_count:
               self.current_index = 0
    
    def render(self, passed_time):
        self.play_animation(passed_time)
        Sprite.draw(self)

#显示信息，不过这些信息都是图片，如显示伤害 123，就是3张图片拼接起来的
class Font_Image(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_front_damage = []
    
    #伤害值，存活时间，坐标， 颜色 index, -1每个数字都是随机
    def start(self, damage_int, stand_sec, x_pos, y_pos, color_index, speed_x = 0, speed_y = 6):
        self.life_time = stand_sec
        self.show_x_central_pos, self.show_y_central_pos = x_pos, y_pos
        index = 0
        while damage_int/10 != 0:
            self.image_front_damage.append(global_member.g_number[color_index][damage_int%10 + 1])
            print(damage_int%10 + 1)
            damage_int = damage_int/10
        self.image_front_damage.append(global_member.g_number[color_index][damage_int%10 + 1])
        self.rect.w, self.rect.h = self.image_front_damage[0].get_width(), self.image_front_damage[0].get_height()
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2
        self.fps = 30
        #设置向y轴移动
        self.speed_y, self.speed_x = speed_y, speed_x
        
        
    def play_animation(self, passed_time):
       if self.b_die == True: return
       self.passed_time += passed_time
       if self.passed_time >= 1000/self.fps:
           self.life_time -= passed_time
           if self.life_time < 0: self.b_die = True
           self.current_index += 1
           self.show_x_central_pos -= self.speed_x
           self.show_y_central_pos -= self.speed_y
           self.passed_time = self.passed_time % (1000/self.fps)
           if self.current_index >= self.image_count:
               self.current_index = 0
    
        
    def render(self, passed_time):
        if self.b_die == True: return
        self.play_animation(passed_time)
        #由于每张图片一样的 
        index = 0
        #首先显示的事个位，十位，百位...
        image_count = len(self.image_front_damage)
        for value in self.image_front_damage:
            self.rect.left = self.show_x_central_pos - (index - image_count/2)*self.rect.w/2 
            self.rect.top = self.show_y_central_pos - self.rect.h/2
            self.screen.blit(self.image_front_damage[index], self.rect)
            index += 1
            
#子图管理
class Font_Manager:
    def __init__(self):
        self.font_array = []
        #self.number_frame = []

    def start(self, str_show, stand_sec, x_pos, y_pos, color = (63, 72, 204), speed_x = 0, speed_y = 2):
        font = Font()
        font.start(str_show, stand_sec, x_pos, y_pos, color, speed_x, speed_y)
        self.font_array.append(font)
    
    def start_image(self, damage_int, stand_sec, x_pos, y_pos, color_index, speed_x = 0, speed_y = 6):
        image_damage = Font_Image()
        image_damage.start(damage_int, stand_sec, x_pos, y_pos, color_index, speed_x, speed_y)
        self.font_array.append(image_damage)
        
    def render(self, passed_time):
        for value in self.font_array:
            value.render(passed_time)
    
    def clear(self):
        del self.font_array[:]
            

#显示坦克的血条的和子弟血条
#三种颜色：绿色， 黄色， 红色， 外面的边框
#百分比  100~70  69~40   39~0
class Hp_Process(Base_Object):
    def __init__(self):
        Base_Object.__init__(self)
        self.image_blue = pygame.image.load("data\\HP\\4.png").convert_alpha()
        self.image_gree = pygame.image.load("data\\HP\\3.png").convert_alpha()
        self.imgae_yellow = pygame.image.load("data\\HP\\5.png").convert_alpha()
        self.image_red = pygame.image.load("data\\HP\\6.png").convert_alpha()
        self.image_bk = pygame.image.load("data\\HP\\0.png").convert_alpha()
        self.image_bk_1 = pygame.image.load("data\\HP\\1.png").convert_alpha()
        self.image_bk_2 = pygame.image.load("data\\HP\\2.png").convert_alpha()
        
        self.width, self.height = self.image_gree.get_width(), self.image_gree.get_height()
        self.rect.w, self.rect.h  = self.width, self.height
        self.area_rect = Rect(0, 0, 0, 0)
        self.area_rect.w, self.area_rect.h = self.width, self.height
        
        self.bk_rect = Rect(0, 0, 0, 0)
        self.bg_width, self.bg_height = self.image_bk.get_width(), self.image_bk.get_height()
        self.bk_rect.w, self.bk_rect.h  = self.bg_width, self.bg_height
        
        
        
    def show_pos(self, x_pos, y_pos, percent, hul_index):
        #print("percent=%s rect.w=%s" %(percent, self.rect.w))
        self.show_x_central_pos, self.show_y_central_pos = x_pos, y_pos
        self.rect.left, self.rect.top = self.show_x_central_pos - self.rect.w/2, self.show_y_central_pos - self.rect.h/2
        self.area_rect.w = (self.rect.w * percent)/100
        #print("Later rect.w=%s" %(self.area_rect.w))
        
        self.bk_rect.left, self.bk_rect.top = self.show_x_central_pos - self.bk_rect.w/2, self.show_y_central_pos - self.bk_rect.h/2
        if percent > 70:
            if hul_index == 2: self.image = self.image_blue
            else: self.image = self.image_gree
        elif percent > 40:
            self.image = self.imgae_yellow
        else:
            self.image = self.image_red
        
        if self.b_die == True: return
        if hul_index == 0: #玩家
            global_member.g_screen.blit(self.image_bk_1, self.bk_rect)
        elif hul_index == 0:#敌军
            global_member.g_screen.blit(self.image_bk, self.bk_rect)
        elif hul_index == 2:#基地
            global_member.g_screen.blit(self.image_bk_2, self.bk_rect)
        
        global_member.g_screen.blit(self.image, self.rect, self.area_rect)
        
        
            