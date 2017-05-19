import pygame
from pygame.locals import *

#wo use mang png images to cartoon
#so the all of pic's width must be same
#my english is poor, please
class sprite_common(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.images = []    #load all images surface
        self.image_width = 0
        self.image_height = 0
        self.order = 0      #show index image by order
        self.rate = 0       #Animation frequency by rate
        self.passed_time = 0
        self.image_nums = 0
        self.image = None
        #hostory add run times
        self.run_times = -1 #-1 is unlimited, o is stop
        #central point
        

    def set_tun_times(self, times):
        self.run_times = times
        self.order, self.passed_time = 0, 0 
    
    def set_attribute(self, image_width, image_height, show_pos, rate):
        self.image_width = image_width
        self.image_height = image_height
        self.rate = rate
        self.rect = Rect(show_pos[0], show_pos[1], self.image_width, self.image_height)
        #
        self.central_point = show_pos
    
    def modify_shou_mid_pos(self, mid_show_pos):
        self.central_point = mid_show_pos
    
    def add_image(self, file_path):
        try:
            self.images.append(pygame.image.load(file_path).convert_alpha())
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
        
    def update(self, passed_time):
        if self.image_nums == 0:
            self.image_nums = len(self.images)
        self.passed_time += passed_time
        self.order = ( self.passed_time / self.rate ) % self.image_nums
        if self.order == 0 and self.passed_time > self.rate:
            self.passed_time = 0
            if self.run_times > 0 : self.run_times -= 1
        self.image = self.images[self.order]
        
    def show(self, passed_time):
        if self.run_times == 0: return
        if self.image == None: self.image = self.images[0]
#       self.update(passed_time)
#        if self.run_times == 0: return
        if self.image_height == 0 and self.image_width == 0:
            self.rect.w, self.rect.h = self.image.get_width(), self.image.get_height()
            self.rect.left = self.central_point[0] - self.image.get_width()/2
            self.rect.top  = self.central_point[1] - self.image.get_height()/2
        self.screen.blit(self.image, self.rect)
        self.update(passed_time)
        
    def load_images(self, file_path, start_index, end_index, interval):
        temp_index = start_index
        while temp_index <= end_index:
            temp_file_path = file_path + str(temp_index) + ".png"
            self.add_image(temp_file_path)
            temp_index += interval

        