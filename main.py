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

#>>>>>>> 69d042671ba8d53208a1f54e4f00f6b81df497ac

# Find the left/right points

def find_left_right_points(image, draw = False):

    #taking only widths and heights
    im_height, im_width = image.shape[:2]
    if draw:
        viz_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
    #locate the line in 70% from bottom of the image
    interested_line_y = int(im_height *0.7)

    #indicate the second line of the road
    if draw:
        cv2.line(viz_img, (0, interested_line_y), (im_width, interested_line_y), (0, 0, 255), 2)
    interested_line = image[interested_line_y, :]

    left_point = -1
    right_point = -1
    lane_width = 175
    center = im_width//2

    #finding the left and right points by traversing outward from the center
    for x in range(center, 0, -1):
        if interested_line[x] >0:
            left_point = x
            break
    for x in range(center +1, 0, -1):
        if interested_line[x] < 0:
            right_point = x
            break

    #prediction the point on the right when inly the point on the left is known
    if left_point != -1 and right_point == -1:
        right_point = left_point + lane_width

    #prediction the point on the left when inly the point on the right is known
    if right_point != -1 and left_point == -1:
        left_point = right_point + lane_width

    #draw two points
    if draw:
        if left_point != -1:
            viz_img = cv2.circle(viz_img, (left_point, interested_line_y), 7, (255, 255, 0), -1)
        if right_point != -1:
            viz_img = cv2.circle(viz_img, (right_point, interested_line_y), 7, (255, 255, 0), -1)

        return left_point, right_point, viz_img

viz_images = []

for img in birdview_images:
    left_point, right_point, viz_img = find_left_right_points(img, draw=True)
    viz_images.append(viz_img)

show_images(viz_images)

def calculate_control_signal(img):
    # Calclulate speed and streering angle

    img_lines = find_lane_lines(img)
    img_birdview = birdview_transform(img_lines)
    left_point, right_point, viz_img = find_left_right_points(img_birdview, False)

    #show image
    cv2.imshow('Result', viz_img)
    cv2.waitKey(1)

    #Calclulate speed and angle
    #The speed is fixed to 50% of the max speed 
    throttle = 0.5 #limit
    steerring_angle = 0
    im_center = img.shape[1]//2

    if left_point != -1 and right_point != -1:
        center_point = (right_point + left_point) //2
        center_diff = im_center - center_point


        steerring_angle = -float(center_diff * 0.01)

    return throttle, steerring_angle