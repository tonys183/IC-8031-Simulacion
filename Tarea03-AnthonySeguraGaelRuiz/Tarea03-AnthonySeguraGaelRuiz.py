from math import sqrt

def congruMixMulti(n,a,c,m):
    return (n*a+c) % m

# Ejercicio 4

# Ejercicio 10
def pruebaPromedio(n, distri):
    promedio = sum(distri)/n
    media = 0.5
    z0 = (promedio - media) / sqrt((1/12)/n)
    print(f'Promedio: {promedio} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0)<=1.96 else f'Prueba reprobada'

def pruebaVarianza(n, distri):
    promedio = sum(distri)/n
    s2 = sum(map(lambda x: (x-promedio)*(x-promedio), distri))/(n-1)
    varianza = 1/12
    chi = (n-1)*s2 / varianza

    grados = n-1
    limiteI = grados-1.96 * sqrt(2*grados)
    limiteS = grados+1.96 * sqrt(2*grados)

    print(f'Varianza: {s2} - Chi^2: {chi}')
    print(f'Límite inferior: {limiteI} - Límite superior: {limiteS}')
    return f'Prueba aprobada' if limiteI <= chi <=limiteS else f'Prueba reprobada'

def pruebaCorridas(n, distri):
    esperanza = (2*n -1) / 3
    varianza = (16*n-29) / 90
    h = 1 + sum([(distri[i-2]<=distri[i-1]) ^ (distri[i-1]<=distri[i]) for i in range(2,n)])
    z0 = (h-esperanza)/sqrt(varianza)
    print(f'h: {h} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0)<=1.96 else f'Prueba reprobada'
    
def pruebaHuecosDig(n, distri):
    pass

def pruebaHuecosNums(n, distri): 
    pass

def mano(n):
    cifras = [0]*10
    for digit in n:
        cifras[int(digit)]+=1
    if cifras.count(2) == 2: return 2
    if 2 in cifras and 3 in cifras: return 4
    if 4 in cifras: return 5
    if 5 in cifras: return 6
    if 2 in cifras: return 1
    if 3 in cifras: return 3
    return 0

def pruebaPoker(n, distri): 
    freq = [0]*7
    proba = list(map(lambda p: n*p, [0.30240, 0.50400, 0.10800, 0.07200, 0.00900, 0.00450, 0.00010]))
    distri = list(map(lambda n: str(int(n * 100000)).zfill(5), distri))
    obteni = [mano(num) for num in distri]
    for valor in obteni:
        freq[valor]+=1

    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(freq, proba))
    print(f'Obtenidos: {freq}')
    print(f'Chi^2: {chi}')
    return f'Prueba aprobada' if chi <= 12.5916 else f'Prueba reprobada'

def pruebaSeries(n, distri, c): 
    freq = [0]*(c*c)
    for i in range(n-1):
        fi = min(int(distri[i]*c), c-1)
        col = min(int(distri[i+1]*c), c-1)
        freq[fi*c+col]+=1

    fe = (n-1)/(c*c)
    chi = sum(((fo-fe)*(fo-fe))/fe for fo in freq)
    grados = (c*c)-1
    z0 = (chi-grados) / sqrt(2*grados)
    print(f'Chi^2: {chi} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0) <= 1.96 else f'Prueba reprobada'


def menuEjercicio10():
    """
    1. Método congruencial binario

    2. Método de los cuadrados medios

    3. Método congruencial mixto

    4. Método congruencial multiplicativo

    5. Método congruencial aditivo

    6. Método congruencial polinomial

    """
    while True:
        print("\n--- Ejercicio 10 ---")
        print("1. Prueba de Promedio")
        print("2. Prueba de Varianza")
        print("3. Prueba de Corridas")
        print("4. Prueba de Huecos de dígitos")
        print("5. Prueba de Huecos de números")
        print("6. Prueba de Poker")
        print("7. Prueba de Series")
        print("0. Volver")
        op = input("Opción: ")
        pruebas = ['Promedio', 'Varianza', 'Corridas', 'Huecos de dígitos', 'Huecos de números', 'Poker', 'Series']

        if op == '0':
            break

        if op in ['1','2', '3', '4', '5', '6', '7']:
            print(f"\n--- Prueba de {pruebas[int(op)-1]} ---")
            n, x0, m = int(1e6), 15318679, 4567234902
            distri = list(map(lambda x: x/m, 
                    [(x0 := congruMixMulti(x0, 100485, (1<<27)-1, m)) for _ in range(n)]))

            if op == '1':
                print(pruebaPromedio(n, distri))

            elif op == '2':
                print(pruebaVarianza(n, distri))

            elif op == '3':
                print(pruebaCorridas(n, distri))

            elif op == '6':
                print(pruebaPoker(n, distri))

            elif op == '7':
                c = int(input("Celdas: "))
                print(pruebaSeries(n, distri, c))

def main():
    while True:
        print("\n=================")
        print("      MENÚ")
        print("=================")
        print("1. Ejercicio 4")
        print("2. Ejercicio 10")
        print("0. Salir")
        op = input("Opción: ")

        if op == '1':
            pass

        elif op == '2':
            menuEjercicio10()

        elif op == '0':
            break

if __name__ == "__main__":
    main()
