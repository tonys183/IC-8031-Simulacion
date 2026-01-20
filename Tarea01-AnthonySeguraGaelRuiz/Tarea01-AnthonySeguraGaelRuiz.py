from random import random, sample
from math import floor
import numpy as np
import matplotlib.pyplot as plt

SIMULA = 1000000
SIMULA8 = 100000

# Ejercicio 2
def tirarMoneda():
    return floor(random()*2) # 1 Corona, 0 Escudo

def cantCoronas(n, coronas):
    res = 0
    for _ in range(n):
        tirada = tirarMoneda() + tirarMoneda() + tirarMoneda()
        res += tirada == coronas
    return res/n

# Ejercicio 3
def grafBino(n,p):
    res = [sum(random() < p for _ in range(n)) for _ in range(SIMULA)]
    plt.hist(res, bins=range(n+2), align="left", rwidth=0.8, density=True)
    plt.xticks(range(n+1))
    plt.show()

# Ejercicio 4
def dosAses(n):
    #AS -> 0
    mazo = [[i, j] for i in range(13) for j in range(4)]
    res = 0
    for _ in range(n):
        c1, c2 = sample(mazo, 2)
        res += (c1[0] == 0 and c2[0] == 0)
    return res/n

# Ejercicio 5
def trebolEspada(n):
    #Trebol -> 0
    #Espada -> 1
    mazo = [[i, j] for i in range(13) for j in range(4)]
    res = 0
    for _ in range(n):
        c1 = sample(mazo, 1)[0]
        res += (c1[1] == 0 or c1[1] == 1)
    return res/n

# Ejercicio 6
def asesEn5(n):
    #AS -> 0
    mazo = [[i, j] for i in range(13) for j in range(4)]
    res = 0
    for _ in range(n):
        ases = sum(rank == 0 for [rank, _] in sample(mazo, 5)) 
        res += ases >= 2
    return res/n

# Ejercicio 7
def sumaCartas(n):
    #AS -> 0
    mazo = [[i, j] for i in range(13) for j in range(4)]
    res = 0
    for _ in range(n):
        value = sum(min(rank+1,10) for [rank, _] in sample(mazo, 5)) 
        res += value >= 17 and value <= 21
    return res/n

# Ejercicio 8
def winingA(n, p = 0.48):
    res = 0
    for _ in range(n):
        money = 100
        x = 10
        while money > 0:
            money += x if random() <= p else -x
            if money >= 200:
                res+=1
                break
    return res/n

def winingB(n, p = 0.48):
    res = 0
    for _ in range(n):
        money = 100
        x = 10
        lost = False
        while money > 0:
            currentBet = random() <= p
            x = min(2*x, money) if lost else 10
            money += x if currentBet else -x
            lost = not currentBet
            if money >= 200:
                res+=1
                break
    return res/n

# Ejercicio 9
def S1orS2(n, tokyoS1, S1Florida, tokyoS2, S2Florida, link):
    res = 0
    for _ in range(n):
        s1 = random() <= tokyoS1 and random() <= S1Florida
        s2 = random() <= tokyoS2 and random() <= S2Florida
        s1Links2 = random() <= tokyoS1 and random() <= link and random() <= S2Florida
        s2Links1 = random() <= tokyoS2 and random() <= link and random() <= S1Florida
        res += s1 or s2 or s1Links2 or s2Links1
    return res/n


def menuEjercicio2():
    # A)
    """
    Tres posibles combinaciones: (2^3) = 8
    C,C,E - C,E,C - E,C,C
    La probabilidad es: CF/CT -> 3/8
    """
    
    while True:
        print("\n--- Ejercicio 2 ---")
        print("1. B) 0 coronas")
        print("2. C) 1 corona")
        print("3. D) 2 coronas")
        print("4. E) 3 coronas")
        print("0. Volver")
        op = input("Opción: ")
        
        if op == '0':
            break
        elif op in {'1', '2', '3', '4'}:
            n = int(op)-1
            print(f'{n} coronas: {cantCoronas(SIMULA, n)}')

    # F)
    """
    Una distribución binomial
    """

def menuEjercicio8():
    while True:
        print("\n--- Ejercicio 8 ---")
        print("1. A) Estrategia A")
        print("2. B) Estrategia B")
        print("0. Volver")
        op = input("Opción: ")

        if op == '1':
            print(f'Estrategia A: {winingA(SIMULA8)}')
        elif op == '2':
            print(f'Estrategia B: {winingB(SIMULA8)}')
        elif op == '0':
            break

def menuEjercicio9():
    while True:
        print("\n--- Ejercicio 9 ---")
        print("1. Caso A")
        print("2. Caso B")
        print("3. Caso C")
        print("0. Volver")
        op = input("Opción: ")

        if op == '1':
            # A)
            """
            P(S1): 0.90 * 0.80 = 0.72
            P(S2): 0.90 * 0.70 = 0.63
            Entonces la P(Total): 0.72 + 0.63 - (0.72*0.63) = 0.8964
            """
            print(f'Caso A: {S1orS2(SIMULA, 0.8, 0.9, 0.8, 0.7, 0)}')

        elif op == '2':
            # B)
            """
            P(S1): 0.90 * 0.80 = 0.72
            P(S2): 0.90 * 0.80 = 0.72
            Entonces la P(Total): 0.72 + 0.72 - (0.72*0.72) = 0.9216
            """
            print(f'Caso B: {S1orS2(SIMULA, 0.8, 0.9, 0.8, 0.9, 0)}')

        elif op == '3':
            # C)
            """
            Ya que ahora existen muchos casos debido a que se pueden generar ciclos,  
            no es tan sencillo calcular la probabilidad manualmente
            La alternativa sería usar simulación
            """
            print(f'Caso C: {S1orS2(SIMULA, 0.8, 0.9, 0.8, 0.7, 0.8)}')

        elif op == '0':
            break

def main():
    while True:
        print("\n=================")
        print("      MENÚ")
        print("=================")
        print("2. Ejercicio 2")
        print("3. Ejercicio 3")
        print("4. Ejercicio 4")
        print("5. Ejercicio 5")
        print("6. Ejercicio 6")
        print("7. Ejercicio 7")
        print("8. Ejercicio 8")
        print("9. Ejercicio 9")
        print("0. Salir")
        op = input("Opción: ")

        if op == '2':
            menuEjercicio2()

        elif op == '3':
            print("\n--- Ejercicio 3 ---")
            grafBino(3, 0.5)    

        elif op == '4':
            print("\n--- Ejercicio 4 ---")
            # A)
            """
            Ya que hay 4 ases, la probabilidad de sacar un As al inicio es de 4/52
            Al sacar la segunda carta dado que ya se sacó un As, 
            en el mazo ahora hay 51 cartas y 3 ases, entonces la probabilidad es de 3/51
            La probabilidad es de (4/52) * (3/51) aprox 0.004524
            """
            # B)
            print(f'Par de Ases: {dosAses(SIMULA)}')   

        elif op == '5':
            print("\n--- Ejercicio 5 ---")
            # A)
            """
            Ya que hay 13 treboles y 13 espadas, la probabilidad de sacar 
            un trebol o una espada es de (13 + 13) / 52
            La probabilidad es de 26/52 aprox 0.500
            """
            # B)
            print(f'1 Trebol o Espada: {trebolEspada(SIMULA)}') 

        elif op == '6':
            print("\n--- Ejercicio 6 ---")
            # A)
            """
            Una hipergeométrica de parámetros X∼H(n=5, M=4, N=52)
            P = Σ{i=2}{4} C(4,i) * C(48,3) / C(52,5) aprox 0.04168
            """
            # B)
            print(f'Par de Ases en 5: {asesEn5(SIMULA)}')
            
        elif op == '7':
            print("\n--- Ejercicio 7 ---")
            print(f'Suma entre [17,21] en 5: {sumaCartas(SIMULA)}')
    
        elif op == '8':
            menuEjercicio8()
        
        elif op == '9':
            menuEjercicio9()
            
        elif op == '0':
            break

if __name__ == "__main__":
    main()