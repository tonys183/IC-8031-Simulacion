from math import sqrt, pow
from random import random
alfa = "0123456789abcdefghijklmnopqrstuvwxyz"

def pruebaPromedio(n, distri, real, a, b):
    print(f"\n--- Prueba de Promedio ---")
    promedio = sum(distri)/n
    media = (b+a)/2
    varianza = 1/12 if real else ((b-a+1)*(b-a+1)-1)/12
    z0 = (promedio - media) / sqrt(varianza/n)
    print(f'Media esperada: {media}')
    print(f'Media obtenida: {promedio} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0)<=1.96 else f'Prueba reprobada'

def pruebaVarianza(n, distri, real, a, b):
    print(f"\n--- Prueba de Varianza ---")
    promedio = sum(distri)/n
    s2 = sum(map(lambda x: (x-promedio)*(x-promedio), distri))/(n-1)
    varianza = 1/12 if real else ((b-a+1)*(b-a+1)-1)/12
    chi = (n-1)*s2 / varianza
    grados = n-1
    limiteI = grados-1.96 * sqrt(2*grados)
    limiteS = grados+1.96 * sqrt(2*grados)
    print(f'Varianza esperada: {varianza}')
    print(f'Varianza obtenida: {s2} - Chi^2: {chi}')
    return f'Prueba aprobada' if limiteI <= chi <=limiteS else f'Prueba reprobada'

def pruebaCorridas(n, distri, real):
    print(f"\n--- Prueba de Corridas ---")
    if not real: distri = [val + random() for val in distri]
    media = (2*n-1) / 3
    varianza = (16*n-29) / 90
    h = 1 + sum([(distri[i-2]<=distri[i-1]) ^ (distri[i-1]<=distri[i]) for i in range(2,n)])
    z0 = (h-media)/sqrt(varianza)
    print(f'Media esperada: {media}')
    print(f'Media obtenida: {h} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0)<=1.96 else f'Prueba reprobada'

def contarHuecos(distri, inf, sup, cond):
    huecos = []
    tam = 0
    dentro = False
    for val in distri:
        if cond(val,inf,sup):
            if dentro: huecos.append(tam)
            dentro = True
            tam = 0
        else:
            tam+=dentro
    return {tamHueco: sum(1 for hueco in huecos if hueco == tamHueco) for tamHueco in set(huecos)}

def pruebaHuecosDig(n, distri, real, b):
    print(f"\n--- Prueba de Huecos de Dígitos ---")
    cadena = ""
    if real: cadena = "".join(map(lambda num: str(int(num * 100000)).zfill(5), distri))
    else: cadena = "".join(map(lambda num: str(alfa[int(num)]), distri))
    huecos = contarHuecos(cadena, cadena[len(cadena)>>1], cadena[len(cadena)>>1], lambda val,i,s: val==s)
    totalH = sum(huecos.values())
    observados = [0]*6
    esperados = [0]*6
    for tam, cant in huecos.items(): observados[min(tam, 5)] += cant
    a = 0
    p = 0.1 if real else 1/b 
    for i in range(5):
        prob = p * pow(1-p, i)
        esperados[i] = totalH * prob
        a += prob
    esperados[5] = totalH*(1-a)
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(observados, esperados) if fe)
    print(f'Observados: {observados}')
    print(f'Esperados:  {[round(x, 1) for x in esperados]}')
    print(f'Chi^2: {chi}')
    return f'Prueba aprobada' if chi <= 11.07 else f'Prueba reprobada'

def pruebaHuecosNums(n, distri, real, b):
    print(f"\n--- Prueba de Huecos de Números ---")
    inf = b/3 if real else int(b/2)+1
    sup = b-inf if real else b
    p = (sup-inf)/b if real else (sup-inf+1)/b
    frecObtenidos = contarHuecos(distri, inf, sup, lambda val,i,s: i<=val<=s)
    totalH = sum(frecObtenidos.values())
    obtenidos = [0]*6
    esperados = [0]*6
    for tam, cant in frecObtenidos.items(): obtenidos[min(tam, 5)] += cant
    for k in range(5): esperados[k] = totalH*p*pow(1-p, k)
    esperados[5] = totalH * pow(1-p, 5)
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(obtenidos, esperados) if fe)
    print(f'Valores esperados: {esperados}')
    print(f'Valores obtenidos: {obtenidos}')
    print(f'Chi^2: {chi}')
    return f'Prueba aprobada' if chi <= 11.07 else f'Prueba reprobada'

def mano(n, b):
    cifras = [0]*(b+1)
    for digit in n:
        cifras[int(alfa.find(digit))]+=1
    if cifras.count(2) == 2: return 2
    if 2 in cifras and 3 in cifras: return 4
    if 4 in cifras: return 5
    if 5 in cifras: return 6
    if 2 in cifras: return 1
    if 3 in cifras: return 3
    return 0

def probas(k):
    total = k*k*k*k*k
    td = (k * (k-1) * (k-2) * (k-3) * (k-4)) / total
    par = (10 * k * (k-1) * (k-2) * (k-3)) / total if k >= 4 else 0
    pares = (15 * k * (k-1) * (k-2)) / total if k >= 3 else 0
    trio = (10 * k * (k-1) * (k-2)) / total if k >= 3 else 0
    full = (10 * k * (k-1)) / total if k >= 2 else 0
    poker = (5 * k * (k-1)) / total if k >= 2 else 0
    quintilla = k / total
    return [td, par, pares, trio, full, poker, quintilla]

def agruparDigitos(distri):
    distri = [str(int(distri[i])) for i in range(len(distri))]
    digitos = [alfa[int(num)] for num in distri]
    digitos = [digitos[i:i+5] for i in range(0,len(digitos),5)]
    return ["".join(grupos) for grupos in digitos]

def pruebaPoker(n, distri, real, b): 
    print(f"\n--- Prueba de Poker ---")
    k = 10
    if not real: 
        distri = agruparDigitos(distri)
        n = len(distri)
        k = b
    freq = [0]*7
    proba = list(map(lambda p: n*p, probas(k)))
    if real: distri = list(map(lambda n: str(int(n * 100000)).zfill(5), distri))
    obteni = [mano(num, k) for num in distri]
    for valor in obteni: freq[valor]+=1
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(freq, proba) if fe)
    print(f'Esperados: {[int(x) for x in proba]}')
    print(f'Obtenidos: {freq}')
    print(f'Chi^2: {chi}')
    return f'Prueba aprobada' if chi <= (11.0705 if (not real and k == 4) else 12.5916) else f'Prueba reprobada'

def pruebaSeries(n, distri, c, real, a, b): 
    print(f"\n--- Prueba de Series ---")
    c = b if not real and b < c else c
    freq = [0]*(c*c)
    for i in range(n-1):
        if real:
            fi = min(int(distri[i]*c), c-1)
            col = min(int(distri[i+1]*c), c-1)
        else:
            fi = min(int((distri[i]-a)*c/b), c-1)
            col = min(int((distri[i+1]-a)*c/b), c-1)
        freq[fi*c+col]+=1
    fe = (n-1)/(c*c)
    chi = sum(((fo-fe)*(fo-fe))/fe for fo in freq)
    grados = (c*c)-1
    z0 = (chi-grados) / sqrt(2*grados)
    print(f'Media esperada: {grados}')
    print(f'Chi^2: {chi} - z0: {z0}')
    return f'Prueba aprobada' if abs(z0) <= 1.96 else f'Prueba reprobada'

def obtenerDistri(nombreArchivo):
    with open(nombreArchivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [float(linea.strip()) for linea in lineas]

def exePruebas(n, distri, real, rango):
    print(pruebaPromedio(n, distri, real, rango[0], rango[1]))
    print(pruebaVarianza(n, distri, real, rango[0], rango[1]))
    print(pruebaCorridas(n, distri, real))
    print(pruebaHuecosNums(n, distri, real, rango[1]))
    print(pruebaHuecosDig(n, distri, real, rango[1]))
    print(pruebaPoker(n, distri, real, rango[1]))
    print(pruebaSeries(n, distri, 10, real, rango[0], rango[1]))

def main():
    files = {'1': 'java/java.txt', '2': 'erlang/erlang.txt', '3': 'python/pythonuno.txt', 
             '4': 'python/pythonseis.txt', '5': 'c/ccuatro.txt', '6': 'c/cocho.txt', 
             '7': 'scheme/scheme.txt', '8': 'javascript/javascript.txt'}
    rangos = {'1': [0,1], '2': [0,1], '3': [0,1], '4': [1,6], 
              '5': [1,4], '6': [1,8], '7': [1,20], '8': [1,30]}
    
    while True:
        print("\n---------- MENÚ ----------")
        print("1. Pruebas para Java")
        print("2. Pruebas para Erlang")
        print("3. Pruebas para Python [0,1[")
        print("4. Pruebas para Python {1,2,3,4,5,6}")
        print("5. Pruebas para C {1,2,3,4}")
        print("6. Pruebas para C {1,2,3,4,5,6,7,8}")
        print("7. Pruebas para Scheme [1,20]")
        print("8. Pruebas para JavaScript [1,30]")
        print("0. Salir")
        op = input("Opción: ")

        if op == '0':
            break

        if op in files:
            real = op in ['1','2','3']
            print(f'Pruebas para archivo: {files[op].split("/")[1]}')
            distri = obtenerDistri(files[op])
            n = 1000000
            exePruebas(n, distri, real, rangos[op])  

if __name__ == "__main__":
    main()