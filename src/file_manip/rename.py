from os import listdir
from os import rename
from os.path import isfile, join

# renomeia as imagens geradas pelo PS depois de salvar a camada como imagem

path = "C:\\Users\\lucas\\Desktop\\Placas\\Minhas\\Crops"

onlyfiles = []
for f in listdir(path):
    if isfile(join(path, f)):
        f = f[::-1]
        f = f[11:]
        f = f[::-1]
        orig_path = join(path,f)
        f = f + ".png"
        rename(orig_path, join(path, f))


