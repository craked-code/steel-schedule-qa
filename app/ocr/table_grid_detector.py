from pdf2image import convert_from_path
import cv2
import numpy as np
import math

def table_area_crop(image, table):
    #expanding table outward in rounding
    x_min = math.floor(table.x_min)
    x_max = math.ceil(table.x_max)
    y_min = math.floor(table.y_min)
    y_max = math.ceil(table.y_max)
    
    # in image pixels top left is (0,0) and it increases as you move right and down
    image = image.crop((x_min, y_min, x_max, y_max)) 

    return image


def detect_grid_lines(images, dpi, detected_tables):
    kernel = np.ones((1, round(40 * (dpi / 300))), np.uint8)

    for index, image in enumerate(images):
        for table in detected_tables:

            if table.page_number == index:
                cropped_image = table_area_crop(image, table)
                cropped_image_np = np.asarray(cropped_image)
                
                gy_image = cv2.cvtColor(cropped_image_np, cv2.COLOR_RGB2GRAY) # RGB to gray image
                _ , dst = cv2.threshold(gy_image, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU) # convert gray image pixels to pure black or pure white based on threshold
                eroded = cv2.erode(src=dst, kernel=kernel, iterations=1) # errosion
                dilated = cv2.dilate(src=eroded, kernel=kernel, iterations=1) # dilation
                