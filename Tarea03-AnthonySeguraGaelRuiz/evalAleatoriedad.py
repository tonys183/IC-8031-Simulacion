from math import sqrt

def pruebaPromedio(n, distri):
    print(f"\n--- Prueba de Promedio ---")
    promedio = sum(distri)/n
    media = 0.5
    z0 = (promedio - media) / sqrt((1/12)/n)
    print(f'Promedio: {promedio} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0)<=1.96 else f'Prueba reprobada'

def pruebaVarianza(n, distri):
    print(f"\n--- Prueba de Varianza ---")
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
    print(f"\n--- Prueba de Corridas ---")
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
    print(f"\n--- Prueba de Poker ---")
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
    print(f"\n--- Prueba de Series ---")
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

def obtenerDistri(nombreArchivo):
    with open(nombreArchivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [float(linea.strip()) for linea in lineas]

def exePruebas(n, distri):
    print(pruebaPromedio(n, distri))
    print(pruebaVarianza(n, distri))
    print(pruebaCorridas(n, distri))
    print(pruebaPoker(n, distri))
    print(pruebaSeries(n, distri, 10))

def main():
    files = {'1': 'java/java.txt', '2': 'erlang/erlang.txt', '3': 'python/pythonuno.txt', 
             '4': 'python/pythonseis.txt', '5': 'c/ccuatro.txt', '6': 'c/cocho.txt', 
             '7': 'scheme/scheme.txt', '8': 'extra'}
    tests = {'1': 'java.txt', '2': 'erlang.txt', '3': 'pythonuno.txt', 
             '4': 'pythonseis.txt', '5': 'ccuatro.txt', '6': 'cocho.txt', 
             '7': 'scheme.txt', '8': 'extra'}
    
    while True:
        print("\n---------- MENÚ ----------")
        print("1. Pruebas para Java")
        print("2. Pruebas para Erlang")
        print("3. Pruebas para Python [0,1[")
        print("4. Pruebas para Python {1,2,3,4,5,6}")
        print("5. Pruebas para C {1,2,3,4}")
        print("6. Pruebas para C {1,2,3,4,5,6,7,8}")
        print("7. Pruebas para Scheme [1,20]")
        print("0. Salir")
        op = input("Opción: ")

        if op == '0':
            break

        if op in files:
            print(f'Pruebas para archivo: {tests[op]}')
            distri = obtenerDistri(files[op])
            n = 1000000
            exePruebas(n, distri)  

if __name__ == "__main__":
    main()