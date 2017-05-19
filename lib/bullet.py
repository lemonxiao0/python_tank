#coding=utf-8

import pygame
from pygame.locals import *

import sprite
import frame
import global_member
from random import randint

class Bullet(sprite.Move_Sprite):
    def __init__(self):
        sprite.Move_Sprite.__init__(self)
        self.init_data_Bullet()
    
    def start(self, frames, x_pos, y_pos, dir, speed, from_sprite):
        self.frames = frames
        self.set_position(x_pos, y_pos)
        self.set_dir(dir)
        self.set_speed(speed)
        self.fps = 60
        self.sprite_screen_offest_width, self.sprite_screen_offest_height = 0, 0
        self.width, self.height = self.frames.get_image_width(self.dir), self.frames.get_image_height(self.dir)
        self.screen_test_width, self.screen_test_height = (self.width - self.sprite_screen_offest_width*2)/2, (self.height - self.sprite_screen_offest_height*2)/2
        self.image_count = self.frames.get_image_count(dir)
        self.b_animation_loop = True
        self.from_sprite = from_sprite
        self.base_damage = 50     #暂时没涉及到
        self.rand_damage = 25
        self.magic_effect = None #正在计划中
    
    def get_bullet_damage(self):
        return self.base_damage + randint(-self.rand_damage, self.rand_damage)
        
    def init_data_Bullet(self):
        self.frames = frame.Bullet_Frame()

        
    #virtual
    def draw(self):
        if self.b_die == True: return
        self.frames.draw(self.dir, self.current_index, self.show_x_central_pos, self.show_y_central_pos)
        
    def play_animation(self, passed_time):
        if self.b_die == True: return
        self.current_index += 1
        if self.current_index >= self.image_count:
            if self.b_animation_loop == False:
                self.b_die = True
            self.current_index = 0
        

    def move(self, passed_time):
        if self.b_die == True: return
        self.passed_time += passed_time
        if self.passed_time >= 1000/self.fps:
            self.passed_time = self.passed_time % (1000/self.fps)
            if self.dir == global_member.DIR_UP:
                self.move_up()
            elif self.dir == global_member.DIR_LEFT:
                self.move_left()
            elif self.dir == global_member.DIR_DOWN:
                self.move_down()
            elif self.dir == global_member.DIR_RIGHT:
                self.move_right()
            
            self.play_animation(passed_time)
            
            self.show_x_central_pos += self.move_speed_x
            self.show_y_central_pos += self.move_speed_y
            
            object_hit_list = self.hit_test_other_sprite()

            if object_hit_list != None:
                for value in object_hit_list:
                    #自己人打自己人无效滴
                    if self.from_sprite.sprite_type == value.sprite_type: continue
                    #子弹不能穿过
                    if value.flag & global_member.OBJ_FLAG_ABLE_THROUGH == 0:
                        self.b_die = True
                        global_member.g_explosion_manager.start_explosion(self.show_x_central_pos, self.show_y_central_pos, 0)
                        #global_member.g_explosion_manager.start_explosion(value.show_x_central_pos, value.show_y_central_pos, 2)
                        #被撞的单位可以摧毁
                        if value.flag & global_member.OBJ_FLAG_ABLE_DESTROY > 0:
                            #也就是说明是别的有意义的单位啦
                            if value.sprite_type != 0:
                                global_member.bullet_hit_tank(self, value)
                                return
                            elif value.flag & global_member.OBJ_FLAG_MILITARYBASE > 0:
                                global_member.bulet_hit_military_base(self, value)
                                return
                            else:
                                value.b_die = True
                        global_member.g_explosion_manager.start_explosion(value.show_x_central_pos, value.show_y_central_pos, 2)
                            
            else:
                if self.show_x_central_pos <= 0 :
                    self.b_die = True
                elif self.show_x_central_pos >= global_member.WINDOW_WIDTH:
                     self.b_die = True
                elif self.show_y_central_pos <= 0:
                     self.b_die = True
                elif self.show_y_central_pos >= global_member.WINDOW_HEIGHT:
                     self.b_die = True
                             
            
                
class Bullet_Manager():
    def __init__(self):
        self.bullet_array = []
        self.bullet_frames = []
        
    def __del__(self):
        del self.bullet_array[:]
        del self.bullet_frames[:]
        
    def start(self, bullet_id, x_pos, y_pos, dir, speed, from_sprite):
        bullet_test = Bullet()
        bullet_test.start(self.bullet_frames[bullet_id], x_pos, y_pos, dir, speed, from_sprite)
        self.bullet_array.append(bullet_test)   
        
    def move(self, passed_time):
        for value in self.bullet_array:
            value.move(passed_time)
            
    def render(self):
        for value in self.bullet_array:
            if value.b_die == True:
                self.bullet_array.remove(value)
                break
        
        for value in self.bullet_array:
            value.draw()
    
    def release(self):
        del self.bullet_array[:]
    
    def init_data_Bullet_Manager(self):
        if len(self.bullet_frames) > 0:
            return
        for index in range(global_member.g_bullet_count):
            frames = frame.Bullet_Frame()
            frames.load_bullet_by_name(str(index))
            self.bullet_frames.append(frames)
    