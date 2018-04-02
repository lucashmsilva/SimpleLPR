import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops

# import matplotlib.patches as patches
import matplotlib.pyplot as plt

import pre_proc

from os.path import splitext, join

def find_chars(image_pathfile, thresh_method, closing=1):
    binary_plate = pre_proc.pre_proc(image_pathfile,thresh_method,closing)
    license_plate = np.invert(binary_plate)

    character_dimensions = (0.45*license_plate.shape[0], 0.80*license_plate.shape[0], 0.01*license_plate.shape[1], 0.25*license_plate.shape[1])
    min_height, max_height, min_width, max_width = character_dimensions
    # fig, ax1 = plt.subplots(1)
    # ax1.imshow(license_plate, cmap="gray")
    labelled_plate = measure.label(license_plate)
    characters = []
    column_list = []
    i = 0
    for regions in regionprops(labelled_plate):
        y0, x0, y1, x1 = regions.bbox
        region_height = y1 - y0
        region_width = x1 - x0

        if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
            roi = license_plate[y0:y1, x0:x1]

            resized_char = resize(roi, (30, 20),mode="reflect")
            characters.append(resized_char)
            column_list.append(x0)

            # roi = np.invert(roi)
            # plt.imsave(fname=str(i)+".png",arr=roi,cmap="gray")
            # # rect_border = patches.Rectangle((x0-1.3, y0-1.3), x1+1 - x0+1, y1+1 - y0+1, edgecolor="red", linewidth=1, fill=False)
            # ax1.add_patch(rect_border)
            i += 1
    return (characters, column_list)

def segment(image_path,filename):
    image_pathfile = join(image_path,filename)
    n_chars = len(splitext(filename)[0])
    characters, column_list = find_chars(image_pathfile, thresh_method=1)
    if(len(characters) == n_chars):
        print ("Otsu Thresholding, with closing")
        return (characters, column_list)

    characters, column_list = find_chars(image_pathfile, thresh_method=2)
    if(len(characters) == n_chars):
        print ("Local Thresholding, with closing")
        return (characters, column_list)

    characters, column_list = find_chars(image_pathfile, thresh_method=1, closing=0)
    if(len(characters) == n_chars):
        print ("Otsu Thresholding, no closing")
        return (characters, column_list)

    characters, column_list = find_chars(image_pathfile, thresh_method=2, closing=0)
    if(len(characters) == n_chars):
        print ("Local Thresholding, no closing")
        return (characters, column_list)
    else:
        print ("Can't segment image:", filename, "Check the image....")
        return (None,None)

def disp_img():
    plt.show()  
