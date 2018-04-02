from skimage.transform import rotate
from skimage.io import imread, imsave
from os import listdir
from os.path import join
from random import randrange
from skimage.util import random_noise

path = "/home/lucas/PDI/implementacao/imgs/Placas/Minhas/Crops/caracteres/"
dataset_path = "/home/lucas/PDI/implementacao/imgs/Placas/Minhas/Crops/dataset"
letras = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
          'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T',
          'U', 'V', 'W', 'X', 'Y', 'Z'
         ]

pastas = listdir(dataset_path)
for p in pastas:
    imgs = listdir(join(dataset_path,p))
    qtd_img = len(imgs)
    count = qtd_img
    for i in imgs:
        pImg = join(dataset_path,p,i)
        img = imread(pImg)
        for j in range(0,20):
            ang = randrange(-30,30)
            nimg = rotate(img,ang)
            for k in range(0,4):
                nimg2 = random_noise(nimg,mode='s&p')
                imsave(join(dataset_path,p,p+"_"+str(count)+".png"),nimg2)
                count = count + 1

