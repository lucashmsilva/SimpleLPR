from skimage.io import imread
from skimage.exposure import equalize_hist
from skimage.filters import threshold_otsu, threshold_local
from skimage.morphology import binary_closing


def pre_proc(image_pathfile, thresh_method=1, closing=1):
    plate_img = imread(image_pathfile, as_grey=True)
    gray_plate = plate_img * 255

    gray_plate = equalize_hist(gray_plate)
    
    if(thresh_method == 1):
        threshold_value = threshold_otsu(gray_plate, 25)
    else:
        threshold_value = threshold_local(gray_plate, block_size=25)
    binary_plate = gray_plate > threshold_value

    if(closing == 1):
        binary_plate = binary_closing(binary_plate)

    return binary_plate