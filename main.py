import matplotlib.pyplot as plt
import matplotlib.image as mimg
#from imutils import paths
import numpy as np
import os
import glob
import cv2
import math

road1 = cv2.imread("road_images/road1.png")
road2 = cv2.imread("road_images/road2.png")
road3 = cv2.imread("road_images/road3.png")
road4 = cv2.imread("road_images/road4.png")
road5 = cv2.imread("road_images/road5.png")
road6 = cv2.imread("road_images/road6.png")

roads = [road1, road2, road3, road4, road5, road6]


def show_images(images, cmap='viridis'):
    column = 3
    row = int(math.ceil(len(images)/column))
    
    for i, img in enumerate(images):
        plt.subplot(row, column, i+1) # 2 rows, 3 columns, position of img
        if cmap != 'gray':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img, cmap=cmap)
        plt.axis('off')
        plt.show()


show_images(roads)

