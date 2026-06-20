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
# <<<<<<< HEAD
        plt.imshow(img, cmap=cmap)
        plt.axis('off')
    plt.show()

#convert images in gray and find the line of the roads
def find_lane_lines(img):
    # convert the imgags to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #blur the images
    img_gauss = cv2.GaussianBlur(gray, (11,11), 0)

    # draw the lines (dont know what does the numbers mean)
    thresh_low = 150
    tresh_high = 200
    img_canny = cv2.Canny(img_gauss, thresh_low, tresh_high)

    return img_canny

# list with new converted images
list_img_lines = []

#add modified images to the list and display them
for img in roads:
    img_lines = find_lane_lines(img)
    list_img_lines.append(img_lines)

show_images(list_img_lines)


# vehicle control using a land detection function

# birdview function

def birdview_transform(img):
    image_height = img.shape[0] 
    image_width = img.shape[1]
    
    src = np.float32([[0, image_height], [image_height, image_height], [0, image_height//3], [image_width, image_height//3]])

    dst = np.float32([[90, image_height], [230, image_height], [-10, 0], [image_width + 10, 0]])

    #transformation matrix
    M = cv2.getPerspectiveTransform(src, dst)

    warped_img = cv2.warpPerspective(img, M, (image_width, image_height))

    return warped_img

birdview_images = [birdview_transform(img) for img in list_img_lines]

show_images(birdview_images, cmap='gray')
#=======
        if cmap != 'gray':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img, cmap=cmap)
        plt.axis('off')
        plt.show()


show_images(roads)

#>>>>>>> 69d042671ba8d53208a1f54e4f00f6b81df497ac
