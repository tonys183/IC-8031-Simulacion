import os
from random import random, randint

def genNums(n, nombreArchivo, tipo):
    dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(dir, nombreArchivo)
    if tipo == 'cerouno':
        with open(root, 'w') as archivo: [archivo.write(f"{random()}\n") for _ in range(n)]
    elif tipo == 'seis':
        with open(root, 'w') as archivo: [archivo.write(f"{randint(1, 6)}\n") for _ in range(n)]

if __name__ == "__main__":
    n = 1000000
    genNums(n, 'pythonuno.txt', 'cerouno')
    genNums(n, 'pythonseis.txt', 'seis')