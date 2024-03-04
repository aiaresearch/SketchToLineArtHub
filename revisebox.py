import tkinter as tk
class ReviseBox(tk.Tk):
   def __init__(self, config_dic = {}):
      self.Label_blur_num =  tk.Label(self, text = 
                        '模糊采点边长')
      self.Label_canny_apply =  tk.Label(self, text = 
                        'Canny算法')
      self.Label_gaussian_wide =  tk.Label(self, text = 
                        '侦测采点边长')
      self.Label_gaussian_decrement =  tk.Label(self, text = 
                        '侦测区域均值减量')
      self.Label_canny_threshold1 = tk.Label(self, text = 
                        'canny边缘确定低阈值')
      self.Label_canny_threshold2 = tk.Label(self, text = 
                        'canny边缘确定高阈值')
      self.Label_canny_wide = tk.Label(self, text = 
                        'canny采点边长')
      
      self.__dict__.update(config_dic)#以加工器为初始属性赋值
      

