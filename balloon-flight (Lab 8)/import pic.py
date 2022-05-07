# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:11:27 2022

@author: pc
"""

from PIL import Image 
image = Image.open(r"D:/Spring 2022/EE 104/Lab 8/balloon-flight/images/bg3.png") 
image = image.resize((132,200),Image.ANTIALIAS) 
image.save(fp="4.png") 