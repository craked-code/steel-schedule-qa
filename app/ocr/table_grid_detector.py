from pdf2image import convert_from_path
import cv2
import numpy as np
import math
from app.config import settings
from app.models.schemas import Row, GridStructure

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
    hor_kernel = np.ones((1, round(40 * (dpi / 300))), np.uint8)
    ver_kernel = np.ones((round(40 * (dpi / 300)), 1), np.uint8)

    table_grids = []

    for index, image in enumerate(images):
        for table in detected_tables:
            rows = []

            if table.page_number == index:
                cropped_image = table_area_crop(image, table)
                cropped_image_np = np.asarray(cropped_image)
                cropped_image_np = cv2.copyMakeBorder(cropped_image_np, 10, 10, 10, 10, cv2.BORDER_CONSTANT, 0)

                gy_image = cv2.cvtColor(cropped_image_np, cv2.COLOR_RGB2GRAY) # RGB to gray image
                _ , dst = cv2.threshold(gy_image, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU) # convert gray image pixels to pure black or pure white based on threshold
                eroded = cv2.erode(src=dst, kernel=hor_kernel, iterations=1) # errosion
                dilated = cv2.dilate(src=eroded, kernel=hor_kernel, iterations=1) # dilation
                
                dilated_width = dilated.shape[1]
                row_pixel_density = (np.sum(dilated, axis=1))/255
                row_pixel_density_bool = row_pixel_density > (settings.pixel_density_threshold)/100 * dilated_width
                
                flip_coords = np.where(np.diff(row_pixel_density_bool))[0] + 1 #position of flips T-->F and F-->T
                start_coords = flip_coords[0::2]
                end_coords = flip_coords[1::2]
                
                y_coords = (start_coords + end_coords)//2 #normal divison give float outputs, row slicing in dst dose not work on float
                y_coords = list(y_coords)

                #slicing strips as per y_coords in original image
                for start, end in zip(y_coords, y_coords[1:]):
                    cropped_row = dst[start:end:]
                    eroded_row = cv2.erode(src=cropped_row, kernel=ver_kernel, iterations=1)
                    dilated_row = cv2.dilate(src=eroded_row, kernel=ver_kernel, iterations=1)
                    
                    col_height = dilated_row.shape[0]
                    col_pixel_density = (np.sum(dilated_row, axis=0))/255
                    col_pixel_density_bool = col_pixel_density > (settings.pixel_density_threshold)/100 * col_height
                    
                    flip_coords = np.where(np.diff(col_pixel_density_bool))[0] + 1
                    start_coords = flip_coords[0::2]
                    end_coords = flip_coords[1::2]
                    
                    x_coords = (start_coords + end_coords)//2
                    x_coords = x_coords - 10 + table.x_min

                    y1 = start - 10 + table.y_min
                    y2 = end - 10 + table.y_min

                    row = Row(y1=y1, y2=y2, col_pos=list(x_coords))
                    rows.append(row)

                gridstructure = GridStructure(rows=rows)
                table_grids.append((gridstructure, table))

    return table_grids