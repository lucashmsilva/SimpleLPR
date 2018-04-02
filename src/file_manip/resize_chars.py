from skimage.transform import resize
from skimage.io import imread, imsave
from os import listdir, mkdir
from os.path import join, isfile, exists
from shutil import rmtree, move

path = "/home/lucas/PDI/implementacao/imgs/Placas/Minhas/Crops/caracteres/"
dataset_path = "/home/lucas/PDI/implementacao/imgs/Placas/Minhas/Crops/dataset"

pastas = listdir(path)
pastas.sort()
for p in pastas:
    cortadas = join(join(path,p),"cortadas")
    pasta_char = join(cortadas,p[0])
    if exists(pasta_char):
        rmtree(pasta_char)
        mkdir(pasta_char)
    else:
        mkdir(pasta_char)
    count = 0
    for i in listdir(cortadas):
        if isfile(join(cortadas,i)):
            img = imread(join(cortadas,i))
            fname = i[0]+"_"+str(count)+".png"
            imsave(pasta_char+"/"+fname,resize(img, (30, 20,3)))
            print("redimencionou e salvou")
            count = count + 1
    if exists(join(dataset_path,p[0])):
        rmtree(join(dataset_path,p[0]))
        move(pasta_char,dataset_path)
    else:
        move(pasta_char,dataset_path)

