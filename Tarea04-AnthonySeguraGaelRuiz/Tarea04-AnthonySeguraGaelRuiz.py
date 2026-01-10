import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, log10
from scipy.stats import chi2, norm, nbinom
from random import uniform

def cdf(x, tipo, params):
    if tipo == 'n':
        return norm.cdf(x, *params)
    if tipo == 'nb':
        return nbinom.cdf(x, *params)
    return 0

def pf(x, tipo, params):
    if tipo == 'n':
        return norm.pdf(x, *params)
    if tipo == 'nb':
        return nbinom.pmf(int(x), *params)
    return 0

def valCrit(grados):
    #t = 1-2/(9*grados)+1.28*sqrt(2/(9*grados))
    #return grados*t*t*t
    alpha = 0.05
    return chi2.ppf(1-alpha, grados)

def obtenerDistri(nombreArchivo):
    with open(nombreArchivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [float(linea.strip()) for linea in lineas]

def mediaDesvi(n, distri):
    promedio = sum(distri)/n
    varianza = sum(map(lambda x: (x-promedio)*(x-promedio), distri))/(n-1)
    return promedio, sqrt(varianza)

def grafFrec(n, distri, nomMuestra):
    numBins = int(1+3.322*log10(n)) 
    conteo, bordes = np.histogram(distri, bins=numBins)
    print(f"{'Intervalo':<20} | {'Frec.Abs.':<10} | {'Frec.Rel.':<10}")
    print("-"*46)
    for i in range(len(conteo)):
        intervalo = f"[{bordes[i]:.2f} - {bordes[i+1]:.2f}]"
        print(f"{intervalo:<20} | {conteo[i]:<10} | {conteo[i]/n:.4f}")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.hist(distri, bins=numBins, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.set_title(f"Histograma de Frec.Absoluta\n{nomMuestra}")
    ax1.set_xlabel("Intervalos de datos")
    ax1.set_ylabel("Frecuencia absoluta")
    ax1.grid(axis='y', alpha=0.5)
    ax2.hist(distri, bins=numBins, weights=np.ones_like(distri)/n, color='salmon', edgecolor='black', alpha=0.7)
    ax2.set_title(f"Histograma de Frec.Relativa\n{nomMuestra}")
    ax2.set_xlabel("Intervalos de datos")
    ax2.set_ylabel("Frecuencia relativa")
    ax2.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.show()

def grafComparativa(n, distri, nomMuestra, tipo, paramsEx):
    numBins = int(1+3.322*log10(n))
    plt.figure(figsize=(10, 6))
    plt.hist(distri, bins=numBins, density=True, color='lightgreen', edgecolor='black', alpha=0.6, label='Datos Muestra')
    xmin, xmax = plt.xlim()
    params = ""
    if tipo == 'n':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, paramsEx) for val in x]
        params = f"Normal (Media $\mu$={paramsEx[0]:.2f}, Desv $\sigma$={paramsEx[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')
        
    elif tipo == 'nb':
        x = np.arange(int(xmin), int(xmax) + 1)
        p = [pf(val, tipo, paramsEx) for val in x]
        params = f"Neg.Binom (n={paramsEx[0]:.2f}, p={paramsEx[1]:.4f})"
        plt.plot(x, p, 'ro--', linewidth=2, label='Distribución Teórica')

    plt.title(f"Comparación: {nomMuestra}\nDistribución: {params}", fontsize=14)
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def pruebaChi(n, distri, tipo, params, muestra):
    print("\n--- Prueba de Chi^2 ---")
    numBins = int(1+3.322*log10(n))
    distri = [x + uniform(-0.5, 0.5) for x in distri] if muestra == 'm3' else distri
    observados, bordes = np.histogram(distri, bins=numBins)
    esperados = [(cdf(bordes[i+1], tipo, params)-cdf(bordes[i], tipo, params))*n for i in range(len(observados))]
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(observados, esperados) if fe)
    crit = valCrit(len(observados)-1-len(params))
    print(f'Esperados: {[int(fe) for fe in esperados]}')
    print(f'Observados: {observados.tolist()}')
    print(f"Chi^2: {chi}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if chi <= crit else f'Prueba reprobada')

def pruebaKS(n, distri, tipo, params, muestra):
    print("\n--- Prueba de Kolmogorov-Smirnov ---")
    distri = [x + uniform(-0.5, 0.5) for x in distri] if muestra == 'm3' else distri
    distriOrd = sorted(distri)
    d = max(abs((i/n) - cdf(x, tipo, params)) for i, x in enumerate(distriOrd, 1))
    crit = 1.36/sqrt(n)
    print(f"D: {d:.6f}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if d <= crit else f'Prueba reprobada')

def main():
    muestras = {'1': 'muestras/m3.txt', '2': 'muestras/m4.txt', '3': 'muestras/m15.txt', '4': 'muestras/m16.txt'}
    nomMuestras = {'1': 'Muestra 1 (m3)', '2': 'Muestra 2 (m4)', '3': 'Muestra 3 (m15)', '4': 'Muestra 4 (m16)'}
    tipo = {'1': 'n', '2': 'nb', '3': 'n', '4': 'n'}
    while True:
        print("\n---------- MENÚ ----------")
        print("1. Muestra m3")
        print("2. Muestra m4")
        print("3. Muestra m15")
        print("4. Muestra m16")
        print("0. Salir")
        op = input("Opción: ")

        if op == '0':
            break

        if op in muestras:
            distri = obtenerDistri(muestras[op])
            N = 100000
            promedio, desvi = mediaDesvi(N, distri)
            
            if tipo[op] == 'n':
                params = (promedio, desvi)
            elif tipo[op] == 'nb':
                p = promedio/(desvi*desvi)
                n = (promedio*p)/(1-p)
                params = (n,p)

            print(f"\n--- Muestra: {nomMuestras[op]} ---")
            print(f'Promedio: {promedio:.4f}')
            print(f'Desviación estándar: {desvi:.4f}')
            grafFrec(N, distri, nomMuestras[op])
            grafComparativa(N, distri, nomMuestras[op], tipo[op], params)
            pruebaChi(N, distri, tipo[op], params, muestras[op].split('/')[-1].split('.')[0])
            pruebaKS(N, distri, tipo[op], params, muestras[op].split('/')[-1].split('.')[0])

if __name__ == "__main__":
    main()