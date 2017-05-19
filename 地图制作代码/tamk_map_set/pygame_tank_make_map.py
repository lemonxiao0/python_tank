#we can make tank map by this
#2012-4-23 14:59:23
#author.Azeal_XiaoJing
#history.
# -*- coding: cp936 -*-
import pygame
from pygame.locals import *

import win32ui
import struct

import pygame_tank_make_map_select

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


pygame.init()
screen_size = (1024, 680)
screen_row = 14
screen_col = 18
screen = pygame.display.set_mode(screen_size,  HWSURFACE | SRCALPHA, 32)
bk_ground_index = 0
#bg_ground = pygame.image.load("tank_map[1]-1.jpg").convert_alpha()

#load all image map ornament
map_images = [] #we can get image surface by select_ui class
map_screen_layout = [[0 for col in range(screen_col)] for row in range(screen_row)]
map_bk_ground = []

#load image to full screen
def show_screen(screen, bk_ground_surface, pos, screen_size, b_fill_screen):
    
    n_width, n_height = bk_ground_surface.get_width(), bk_ground_surface.get_height()
    n_have_fill_width, n_have_fill_height = 0, 0
    if b_fill_screen == False:
        screen.blit(bk_ground_surface, pos)
        return
    n_width_nums = screen_size[0]/n_width
    n_height_nums = screen_size[1]/n_height
    for width_index in range(n_width_nums + 1):
        for height_index in range(n_height_nums + 1):
            screen.blit(bk_ground_surface, (pos[0] + n_width * width_index, pos[1] + n_height * height_index))

#load png images to array current file path
def load_image_to_array(array, file_path, start_index, end_index, interval):
    
    temp_index = start_index
    while temp_index <= end_index:
        temp_file_path = file_path + str(temp_index) + ".png"
        try:
            array.append(pygame.image.load(temp_file_path).convert_alpha())
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
        
        temp_index += interval

#draw rect by mouse pos
def draw_rect_by_mouse_pos(screen, mouse_pos):
    mouse_pos_X, mouse_pos_Y = mouse_pos[0], mouse_pos[1]
    points = []
    x_num, y_num = mouse_pos_X/57, mouse_pos_Y/57
    points.append((x_num*57, y_num * 57))
    points.append((x_num*57, y_num * 57 + 57))
    points.append((x_num*57 + 57, y_num * 57 + 57))
    points.append((x_num*57 + 57, y_num * 57))
    pygame.draw.lines(screen, (0, 255, 0), True, points, 2)

def mouse_image_with_mouse_pos(mouse_pos, image_surface):
    show_pos = (mouse_pos[0] - image_surface.get_width()/2, mouse_pos[1] - image_surface.get_height()/2)
    screen.blit(image_surface, show_pos)

def set_image_by_mouse_pos(mouse_pos, index_image):
    x_pos, y_pos = mouse_pos[0], mouse_pos[1]
    
    #have 6 space which no image
    height_index, width_index =  y_pos/57, x_pos/57
    
    if (height_index ==0 and (width_index == 1 or width_index == 6 or width_index == 11 or width_index == 16)) or \
        (height_index == 12 and width_index == 5):
        return;
    
    map_screen_layout[height_index][width_index] = index_image

def show_map_layout():
    for row_index in range(screen_row):
        for col_index in range(screen_col):
            if map_screen_layout[row_index][col_index] != -1:
                x_pos =col_index*57 - (map_images[map_screen_layout[row_index][col_index]].get_width() - 57)/2
                y_pos =row_index*57 - (map_images[map_screen_layout[row_index][col_index]].get_height() - 57)/2
                screen.blit(map_images[map_screen_layout[row_index][col_index]], (x_pos , y_pos))

def init_map_array_layout():
    for row_index in range(screen_row):
        for col_index in range(screen_col):
            map_screen_layout[row_index][col_index] = -1    

def set_index_none_by_mouse_pos(mouse_pos):
    x_index, y_index= mouse_pos[0]/57, mouse_pos[1]/57
    map_screen_layout[y_index][x_index] = -1

def open_map_from_file():
    global bk_ground_index
    dlg = win32ui.CreateFileDialog(1) 
    dlg.SetOFNInitialDir('.\\map') 
    dlg.DoModal()
    filename = dlg.GetPathName()
    if filename == "": return
    print(filename)
    map_file = open(filename, mode = 'r+b')
    file_buf = str(map_file.read(struct.calcsize("=i")))
    print(file_buf)
    
    bk_ground_index = struct.unpack('i', file_buf)[0]
    print(bk_ground_index)
    
    for row_index in range(screen_row):
        for col_index in range(screen_col):
            file_buf = map_file.read(4)
            map_screen_layout[row_index][col_index]= struct.unpack('i', file_buf)[0]
                      
def save_map_to_file():
    dlg = win32ui.CreateFileDialog(0) 
    dlg.SetOFNInitialDir('.\\map') 
    dlg.DoModal()
    
    filename = dlg.GetPathName() 
    if filename == "": return
    map_file = open(filename, mode = 'wb')
    parsedata_bk_index = struct.pack('i', bk_ground_index)
    map_file.write(parsedata_bk_index)
    
    for row_index in range(screen_row):
        for col_index in range(screen_col):
            data = struct.pack('i', map_screen_layout[row_index][col_index])
            map_file.write(data)


def run():
    global bk_ground_index
    load_image_to_array(map_images, "map_ornament\\", 0, 97, 1)
    load_image_to_array(map_bk_ground, "bk_ground\\", 0, 8, 1)
    init_map_array_layout()
    
    time_clock = pygame.time.Clock()
    
    select_ui = pygame_tank_make_map_select.select_image(screen, screen_size, (128, 128))
    select_ui.load_images("map_ornament\\", 0, 97, 1)

    select_ui.set_append_image("select\\select_append.png")
    select_ui.load_animation_images("animation_image\\tank_common[1]-", 1330, 1348, 2)
    
    loop = True
    while loop:
        time_clock.tick(30)
        for event in  pygame.event.get():
            if event.type == QUIT:
                loop = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    select_ui.run()
                elif event.key == K_F1:
                    bk_ground_index += 1
                    bk_ground_index = bk_ground_index % len(map_bk_ground)
                elif event.key == K_F9:
                    open_map_from_file()
                elif event.key == K_F10:
                    save_map_to_file()
            elif event.type == pygame.MOUSEBUTTONUP:
                if prew_mouse_press == ():
                    break
                if prew_mouse_press[0] == 1:
                    if select_ui.get_current_select_index() != -1:
                        set_image_by_mouse_pos(pygame.mouse.get_pos(), select_ui.get_current_select_index())
                elif prew_mouse_press[2] == 1:
                    set_index_none_by_mouse_pos(pygame.mouse.get_pos())
                prew_mouse_press = ()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                prew_mouse_press = pygame.mouse.get_pressed()
            
            
        #update screen
        show_screen(screen, map_bk_ground[bk_ground_index], (0, 0), screen_size, True)

        #show map ornament
        show_map_layout()

        #get moue pos and draw rect
        mouse_pos = pygame.mouse.get_pos()
        
        #get select image if current_image_index != -1
        if select_ui.get_current_select_index() != -1:
            mouse_image_with_mouse_pos(pygame.mouse.get_pos(), select_ui.get_current_select_image())
            
        draw_rect_by_mouse_pos(screen, mouse_pos)
        
        pygame.display.update()

if __name__ == "__main__":
    run()
    pygame.display.quit()
