from os.path import join
from os import mkdir

# cria as pastas para cada caractere

path = "C:\\Users\\lucas\\Desktop\\Placas\\Minhas\\Crops\\caracteres"

for i in range(65,91):
    mkdir(join(path,str(chr(i))))
for i in range(0,10):
    mkdir(join(path,str(i)))
