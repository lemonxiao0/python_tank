#coding=utf-8 
import pygame

'''
加载路径下面的从 start_index 到 end_index 的全部.png图片到数组array
'''
def load_image_to_array(array, file_path, start_index, end_index, interval):
    temp_index = start_index
    while temp_index <= end_index:
        temp_file_path = file_path + str(temp_index) + ".png"
        try:
            array.append(pygame.image.load(temp_file_path).convert_alpha())
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
        
        temp_index += interval

def load_image_to_array_(array, file_path, start_index, end_index, interval):
    temp_index = start_index
    while temp_index <= end_index:
        temp_file_path = file_path + str(temp_index) + ".png"
        try:
            array.append(pygame.image.load(temp_file_path).convert())
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
        
        temp_index += interval


def load_all_image_to_array(array, file_path, start_index, interval):
    temp_index = start_index
    load_images_nums = 0
    while True:
        temp_file_path = file_path + str(temp_index) + ".png"
        try:
            array.append(pygame.image.load(temp_file_path).convert_alpha())
        except pygame.error:
            return load_images_nums
        load_images_nums += 1
        temp_index += interval

