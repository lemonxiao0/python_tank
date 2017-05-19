#coding=utf-8 
'''
场景类
'''

class Scene(object):
    def __init__(self):
            pass
    #获取输入
    def get_input(self):
        pass
    
    #帧移动
    def frame_move(self, passed_time):
        pass
    
    #渲染
    def render(self, passed_time):
        pass
    
    #释放资源，没有析构函数就是苦
    def release(self):
        pass
    