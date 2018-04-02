from os import listdir, rename
from os.path import join, splitext
from shutil import copy
from random import shuffle

# caminho para pasta "raiz", com as subpastas que contem as imagens das placas cortadas
path = "C:\\Users\\lucas\\Desktop\\Placas\\Minhas\\Crops"

# lista com o caminho para cada subpasta de imagens (so pra evitar um loop)
pastas = [join(path, "040603 (algumas placas diferentes)"),join(path, "070603 (OK)"),join(path, "141002 (camera com angulo)"),join(path, "170902 (OK)")]

# caminho para pasta "raiz" onde cada caractere terá uma subpasta para guardar as imagens cortadas de cada caaractere
destino = join(path, "caracteres")

# gera um lista com todos os caracteres (0-9 e A-Z)
caracteres=[]
for i in range(0,10):
    caracteres = caracteres + [str(i)]
for i in range(65,91):
    caracteres = caracteres + [str(chr(i))]

# gera uma lista de listas com os nomes dos arquivos de cada pasta
files = []
for pasta in pastas:
    f = listdir(pasta)
    f = [splitext(x)[0] for x in f]
    shuffle(f)
    files = files + [f]

# para cada caractere, busca os arquivos que comtem este caractere em seu nome e copia para a sua subpasta no destino
ocorr = []
for caractere in caracteres:
    print("OCORRENCIAS DE ",caractere)
    i = 0
    for f in files: 
        for x in f:
            if caractere in x:
                x = x + ".png"
                ocorr = ocorr + [join(pastas[i],x)]
        i = i + 1
    print(len(ocorr))

    for o in ocorr:
        copy(o,join(destino,caractere))
    
    i = 0    
    for f in (listdir(join(destino,caractere))):
        rename(join(join(destino,caractere),f),join(join(destino,caractere),caractere+"_"+str(i)+".png"))
        i = i + 1
    ocorr = []
    
