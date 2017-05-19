#select map index by this
#2012-4-23 15:42:37
#author. Azeal_Xiaojinf
#history.

import pygame
from pygame.locals import *

#import other class
import pygame_sprite_common

class select_image(object):
    def __init__(self, screen, screen_size, interval_size, image_size=(57, 57)):
        self.images_ornament = []
        self.current_pages_index = 0 #one page is x_nums * y_numss
        self.current_index_select = -1
        self.current_select_x = -1
        self.current_select_y = -1
        self.screen = screen
        self.screen_size = screen_size
        self.interval_size = interval_size
        self.image_size = image_size
        self.x_nums = 0
        self.y_nums = 0
        self.animation_image = pygame_sprite_common.sprite_common(self.screen)
        self.animation_image.set_tun_times(0)
        self.menu_cursor_image = pygame.image.load("select\\MenuCursor.png")
        
    def draw_gridding(self):
        x_line_nums = self.screen_size[0]/self.interval_size[0]
        y_line_nums = self.screen_size[1]/self.interval_size[1]
        self.x_nums, self.y_nums = x_line_nums, y_line_nums

        for x_index in range(x_line_nums+1):
            if x_index == 0: continue
            point_from = (x_index * self.interval_size[0], 0)
            point_to =(x_index * self.interval_size[0], self.screen_size[1])
            pygame.draw.aaline(self.screen, (125, 125, 125), point_from, point_to)
            
        for y_index in range(y_line_nums+1):
            if y_index == 0: continue
            point_from = (0, y_index * self.interval_size[1])
            point_to =(self.screen_size[0], y_index * self.interval_size[0])
            pygame.draw.aaline(self.screen, (125, 125, 125), point_from, point_to)
    
    def add_image(self, file_path):
        try:
            self.images_ornament.append(pygame.image.load(file_path).convert_alpha())
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    
            
    def load_images(self, file_path, start_index, end_index, interval):
        temp_index = start_index
        while temp_index <= end_index:
            temp_file_path = file_path + str(temp_index) + ".png"
            self.add_image(temp_file_path)
            temp_index += interval
    
    def load_animation_images(self, file_path, start_index, end_index, interval):
        self.animation_image.load_images(file_path, start_index, end_index, interval)

            
    def set_append_image(self, file_path):
        try:
            self.image_append = pygame.image.load(file_path).convert_alpha()
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
        
        
    def show_images(self):
        n_image_count = len(self.images_ornament)
        for y_index in range(self.y_nums):
             for x_index in range(self.x_nums):
                if (x_index  + y_index * self.x_nums + 1) > n_image_count:
                    break
                select_index = self.current_pages_index * self.x_nums *self.y_nums + x_index  + y_index * self.x_nums
                if select_index >=len(self.images_ornament): return
                self.screen.blit(self.images_ornament[select_index], \
                    (x_index * self.interval_size[0] + (self.interval_size[0] - self.images_ornament[select_index].get_width())/2, y_index * self.interval_size[1] + (self.interval_size[1] - self.images_ornament[select_index].get_height())/2))
    
    def set_index_by_mouse_pos(self, mouse_pos):
        if mouse_pos[0] > (self.x_nums * self.interval_size[0]) or mouse_pos[1] > (self.y_nums * self.interval_size[1]):
            return -1
        x_temp = mouse_pos[0]/self.interval_size[0]
        y_temp = mouse_pos[1]/self.interval_size[1]
        select_index = y_temp * self.x_nums + x_temp
        if select_index + 1 > len(self.images_ornament):
            return            
        self.current_index_select = select_index + self.current_pages_index * self.x_nums * self.y_nums
        self.current_select_x, self.current_select_y = x_temp, y_temp
    
    def get_current_select_index(self):
        return self.current_index_select
    
    def get_current_select_image(self):
        return self.images_ornament[self.current_index_select]
     
    def show_select_append_image(self):
        if self.current_index_select == -1: return
        if self.current_index_select / (self.x_nums * self.y_nums) != self.current_pages_index:
            return;
        image_size = self.image_append.get_size()
        show_pos = ((self.current_select_x + 1)*self.interval_size[0] - self.image_size[0] + 10, \
                     (self.current_select_y + 1)*self.interval_size[1] - self.image_size[1] + 10)
        self.screen.blit(self.image_append, show_pos)
    
    def calculate_animation_start_pos_by_mouse_pos(self, mouse_pos, image_size):
        show_pos = ((self.current_select_x + 1)*self.interval_size[0] - image_size[0] + 24, \
                     (self.current_select_y + 1)*self.interval_size[1] - image_size[1] + 24)
        return show_pos
    
    def draw_rect_by_mouse_pos(self, mouse_pos):
        if self.x_nums * self.interval_size[0] < mouse_pos[0] or self.y_nums * self.interval_size[1] < mouse_pos[1]:
            return
        mouse_pos_X, mouse_pos_Y = mouse_pos[0], mouse_pos[1]
        points = []
        x_num, y_num = mouse_pos_X/self.interval_size[0], mouse_pos_Y/self.interval_size[1]
        points.append((x_num*self.interval_size[0], y_num * self.interval_size[1]))
        points.append((x_num*self.interval_size[0], y_num * self.interval_size[1] + self.interval_size[1]))
        points.append((x_num*self.interval_size[0] + self.interval_size[0], y_num * self.interval_size[1] + self.interval_size[1]))
        points.append((x_num*self.interval_size[0] + self.interval_size[0], y_num * self.interval_size[1]))
        pygame.draw.lines(self.screen, (190, 161, 255), True, points, 4)
    
    def draw_image_by_mouse_pos(self, mouse_pos):
        if self.x_nums * self.interval_size[0] < mouse_pos[0] or self.y_nums * self.interval_size[1] < mouse_pos[1]:
            return
        mouse_pos_X, mouse_pos_Y = mouse_pos[0], mouse_pos[1]
        points = []
        x_num, y_num = mouse_pos_X/self.interval_size[0], mouse_pos_Y/self.interval_size[1]
        self.screen.blit(self.menu_cursor_image, (x_num * self.interval_size[0], y_num * self.interval_size[1]))        
        
    def run(self):
        loop = True
        time_clock = pygame.time.Clock()
        
        while loop:
            pass_time = time_clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    loop = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        loop = False
                    elif event.key == K_F2:
                        if (self.current_pages_index + 1) * self.x_nums * self.y_nums  > len(self.images_ornament):
                            pass
                        else:
                            self.current_pages_index += 1
                    elif event.key == K_F3:
                        if self.current_pages_index - 1 < 0:
                            pass
                        else:
                            self.current_pages_index -= 1
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if prew_mouse_press == ():
                        break
                    if prew_mouse_press[0] == 1:
                        self.animation_image.set_tun_times(1)
                        self.set_index_by_mouse_pos(pygame.mouse.get_pos())
                        self.animation_image.set_attribute(91, 91, self.calculate_animation_start_pos_by_mouse_pos(pygame.mouse.get_pos(), (91, 91)), 60)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    prew_mouse_press = pygame.mouse.get_pressed()
                    
            self.screen.fill((152, 214, 173))
            self.draw_gridding()
            self.show_images()
            self.show_select_append_image()
            self.animation_image.show(pass_time)
            
            self.draw_rect_by_mouse_pos(pygame.mouse.get_pos())
            self.draw_image_by_mouse_pos(pygame.mouse.get_pos())
            
            pygame.display.update()        

