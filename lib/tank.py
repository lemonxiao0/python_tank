#!/usr/bin/env python
#coding=utf-8

import pygame
from pygame.locals import *
from random import randint

import global_member
import sprite
import frame
import bullet
import explosion


class Tank(sprite.Move_Sprite):
    def __init__(self):
        sprite.Move_Sprite.__init__(self)
        self.init_data_Tank()
        self.fire_sound_player = pygame.mixer.Sound("data\\sound\\shoot2.ogg")
        self.fire_sound_enemy = pygame.mixer.Sound("data\\sound\\shoot1.wav")
        self.is_show_hp = True
        self.hp_show = sprite.Hp_Process()
        
    def init_tank(self, x_pos, y_pos, tank_index):
        self.flag |= global_member.OBJ_FLAG_ABLE_DESTROY
        self.frames = global_member.g_tank_manager.load_tank_frame_by_index(tank_index)
        self.b_animation_loop = True
        self.show_x_central_pos, self.show_y_central_pos = x_pos, y_pos
        self.sprite_screen_offest_width, self.sprite_screen_offest_height = 40, 40
        self.width, self.height = self.frames.get_image_width(), self.frames.get_image_height()
        self.screen_test_width, self.screen_test_height = (self.width - self.sprite_screen_offest_width*2)/2, (self.height - self.sprite_screen_offest_height*2)/2
        self.speed = 4
    
    def fire(self):
        if self.b_die == True: return
        start_x, start_y = self.show_x_central_pos, self.show_y_central_pos
        if self.dir == global_member.DIR_UP:
            start_y -= self.height/2 
            global_member.g_explosion_manager.start_explosion(start_x, start_y, 0)

        elif self.dir == global_member.DIR_LEFT:
            start_y -= 9
            start_x -= self.width/2
            global_member.g_explosion_manager.start_explosion(start_x, start_y, 0)            

        elif self.dir == global_member.DIR_DOWN:
            start_y += self.height/2 - 10
            global_member.g_explosion_manager.start_explosion(start_x, start_y, 0)
            
        elif self.dir == global_member.DIR_RIGHT:
            start_y -= 9
            start_x += self.width/2 #- 10
            global_member.g_explosion_manager.start_explosion(start_x, start_y, 0)

        self.stop_move()
        self.set_action(global_member.ACTION_TYPE_FIRE)
        self.fps = self.fire_fps
        #global_member.g_explosion_manager.start_explosion(start_x, start_y, "1")
        if self.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK:
            self.fire_sound_player.play(0)
        elif self.sprite_type ==  global_member.SPRITE_TYPE_ENEMY_TANK:
            self.fire_sound_enemy.play(0)
              
        global_member.g_bullet_manager.start(3, start_x, start_y, self.dir, 7, self)

        
    def play_animation(self, passed_time):
        if self.b_die == True: return
        self.passed_time += passed_time
        if self.passed_time >= 1000/self.fps:
            self.passed_time = self.passed_time % (1000/self.fps)
            self.current_index += 1
            if self.current_index >= self.frames.get_image_count(self.current_action, self.dir):
                if self.b_animation_loop == True: self.current_index = 0
                if self.current_action == global_member.ACTION_TYPE_FIRE:
                    self.set_action(global_member.ACTION_TYPE_STOP)
                    self.fps = self.move_fps
    
    def move(self, passed_time):
        if self.b_die == True: return
        sprite.Move_Sprite.move(self, passed_time)
        self.stop_move()
    
    def draw(self):
        if self.b_die == True: return
        self.frames.draw(self.current_action, self.dir, self.current_index, self.show_x_central_pos, self.show_y_central_pos);
        if self.is_show_hp == True:
            hul_index = 0
            if self.flag & global_member.OBJ_FLAG_MILITARYBASE: hul_index = 2
            elif self.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK: hul_index = 1
            elif self.sprite_type == global_member.SPRITE_TYPE_PLAYER_TANK: hul_index = 1             
            self.hp_show.show_pos(self.show_x_central_pos, self.show_y_central_pos - 30, (self.remain_hp * 100) / self.hp, hul_index)

#protect            
    def init_data_Tank(self):
        self.move_fps = 30
        self.fire_fps = 40
        self.fps = self.move_fps

#enemy
class Enemy_Tank(Tank):
    def __init__(self):
        Tank.__init__(self)
        self.sprite_type = global_member.SPRITE_TYPE_ENEMY_TANK
        self.init_data_Enemy_Tank()
        self.rand_move_passed_time = 0
        #敌军的血量
        self.hp, self.remain_hp = 320, 320
        
    def init_data_Enemy_Tank(self):
        pass
    
    def move(self, passed_time):
        if self.b_die == True: return
        if randint(0, 65535)%1000 >= 15:
            sprite.Move_Sprite.move(self, passed_time)
            return
        randNum = randint(0, 100)
        if randNum < 20:
            self.set_action(global_member.ACTION_TYPE_MOVE)
            self.set_dir(global_member.DIR_LEFT)
        elif randNum < 50:
            self.set_action(global_member.ACTION_TYPE_MOVE)
            self.set_dir(global_member.DIR_DOWN)
        elif randNum < 70:
            self.set_action(global_member.ACTION_TYPE_MOVE)
            self.set_dir(global_member.DIR_RIGHT)
        elif randNum < 80:
           self.set_action(global_member.ACTION_TYPE_MOVE)
           self.set_dir(global_member.DIR_UP)
        if randNum < 100 and randNum > 65:
           self.set_action(global_member.ACTION_TYPE_FIRE)
       
        if self.current_action == global_member.ACTION_TYPE_MOVE:
           if self.dir == global_member.DIR_UP: 
                self.move_up() 
                self.move_up()
           elif self.dir == global_member.DIR_LEFT: 
                self.move_left() 
                self.move_left()
           elif self.dir == global_member.DIR_DOWN: 
                self.move_down() 
                self.move_down()
           elif self.dir == global_member.DIR_RIGHT: 
                self.move_right() 
                self.move_right()
        elif self.current_action == global_member.ACTION_TYPE_FIRE:
            self.fire()

        sprite.Move_Sprite.move(self, passed_time)
             
       

#玩家的tank
class Player_Tank(Tank):
    def __init__(self):
        Tank.__init__(self)
        self.init_data_Player_Tank()
        self.sprite_type = global_member.SPRITE_TYPE_PLAYER_TANK
        #玩家的血量
        self.hp, self.remain_hp = 360, 360  #总血量
        #玩家的特有属性
        self.crit = 15   #暴击，百分比
    
    def Is_Crit(self):
        if randint(0, 100) <= 15:
            return True
        return False
        
    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: return QUIT
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    global_member.go_to_scene("Menu")
                elif event.key == K_SPACE:
                    self.fire()
                elif event.key == K_RETURN:
                    if global_member.g_tank_win:
                        global_member.g_active_scene.start_next_chapter()
                    if global_member.g_tank_over:
                        global_member.go_to_scene("Menu")
                elif event.key == K_F1:
                    global_member.screen_shot()	
                
                        
        if self.b_die == True: return None            
        pressed_keys = pygame.key.get_pressed()
        if self.current_action != global_member.ACTION_TYPE_FIRE:            
            if pressed_keys[K_LEFT]:      self.move_left()
            elif pressed_keys[K_DOWN]:  self.move_down()
            elif pressed_keys[K_RIGHT]: self.move_right()
            elif pressed_keys[K_UP]:  self.move_up()
        return None
                               
    
    def init_data_Player_Tank(self):
        pass
        