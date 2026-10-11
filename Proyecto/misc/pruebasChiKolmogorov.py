from matplotlib.pylab import log10
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from scipy.stats import chi2, norm, expon, binom, geom

def cdf(x, tipo, params):
    if tipo == 'exp':
        return expon.cdf(x, *params)
    if tipo == 'nd':
        return norm.cdf(x, params[0]+0.5, params[1])
    if tipo == 'b':
        return binom.cdf(x, *params)
    if tipo == 'g':
        return geom.cdf(x, *params)
    return 0

def pf(x, tipo, params):
    if tipo == 'exp':
        return expon.pdf(x, *params)
    if tipo == 'nd':
        return norm.pdf(x, *params)
    if tipo == 'b':
        return binom.pmf(x, *params)
    if tipo == 'g':
        return geom.pmf(x, *params)
    return 0

def valCrit(grados):
    alpha = 0.05
    return chi2.ppf(1-alpha, grados)

def obtenerDistri(nombreArchivo):
    with open(nombreArchivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [float(linea.strip()) for linea in lineas]

def mediaDesvi(N, distri):
    media = sum(distri)/N
    varianza = sum((x - media)*(x - media) for x in distri)/(N-1)
    return media, sqrt(varianza)

def grafFrec(N, distri, nomMuestra, bordes):
    _, bordes = np.histogram(distri, bins=bordes)
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.hist(distri, bins=bordes, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.set_title(f"Histograma de Frec.Absoluta\n{nomMuestra}")
    ax1.set_xlabel("Intervalos de datos")
    ax1.set_ylabel("Frecuencia absoluta")
    ax1.grid(axis='y', alpha=0.5)
    ax2.hist(distri, bins=bordes, weights=np.ones_like(distri)/N, color='salmon', edgecolor='black', alpha=0.7)
    ax2.set_title(f"Histograma de Frec.Relativa\n{nomMuestra}")
    ax2.set_xlabel("Intervalos de datos")
    ax2.set_ylabel("Frecuencia relativa")
    ax2.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.show()

def grafComparativa(N, distri, nomMuestra, tipo, params, bordes):
    plt.figure(figsize=(10, 6))
    plt.hist(distri, bins=bordes, density=True, color='lightgreen', edgecolor='black', alpha=0.6, label='Datos Muestra')
    xmin, xmax = plt.xlim()
    paramsTxt = ""

    if tipo == 'exp':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, params) for val in x]
        paramsTxt = f"Exponencial (Lambda $\lambda$={1/params[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')

    if tipo == 'nd':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, params) for val in x]
        paramsTxt = f"Normal (Media $\mu$={params[0]:.2f}, Desv $\sigma$={params[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')

    if tipo == 'b':
        x = np.arange(int(xmin), int(xmax) + 1)
        p = [pf(val, tipo, params) for val in x]
        paramsTxt = f"Binomial (n={params[0]:.2f}, p={params[1]:.4f})"
        plt.plot(x, p, 'ro--', linewidth=2, label='Distribución Teórica')

    if tipo == 'g':
        x = np.arange(int(xmin), int(xmax) + 1)
        p = [pf(val, tipo, params) for val in x]
        paramsTxt = f"Geométrica (p={params[0]:.4f})"
        plt.plot(x, p, 'ro--', linewidth=2, label='Distribución Teórica')

    plt.title(f"Comparación: {nomMuestra}\nDistribución: {paramsTxt}", fontsize=14)
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def calcChiMuestra(N, distri, tipo, params, muestra, bordes):
    if muestra in ['cajas', 'refrescos', 'llegadas']:
        observados, _ = np.histogram(distri, bins=bordes)
        esperados = [(cdf(bordes[i+1], tipo, params)-cdf(bordes[i], tipo, params))*N for i in range(len(observados))]

    if muestra in ['freidora']: 
        observados = np.bincount(np.array(distri, dtype=int))
        observados = np.trim_zeros(observados, 'b') 
        esperados = [((cdf(1, tipo, params) if i == 0 else cdf(i+1, tipo, params) - cdf(i, tipo, params)) * N) for i in range(len(observados))]

    if muestra in ['ordenes', 'pollo', 'postres']:
        maxVal = int(max(distri))
        observados = np.bincount(np.array(distri, dtype=int), minlength=maxVal+1)
        esperados = [pf(i, tipo, params)*N for i in range(len(observados))]

    return observados, esperados

def pruebaChi(N, distri, tipo, params, muestra, bordes):
    print("\n--- Prueba de Chi^2 ---")
    observados, esperados = calcChiMuestra(N, distri, tipo, params, muestra, bordes)
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(observados, esperados) if fe)
    crit = valCrit(len(observados)-1-len(params))
    print(f"Chi^2: {chi}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if chi <= crit else f'Prueba reprobada')

def pruebaKS(N, distri, tipo, params, ksCrit):
    print("\n--- Prueba de Kolmogorov-Smirnov ---")
    if tipo in ['b', 'g', 'nd']:
        valores, conteos = np.unique(distri, return_counts=True)
        observados = np.cumsum(conteos) / N
        esperados = [((cdf(val + 1, tipo, params) if tipo == 'nd' else cdf(val, tipo, params))) for val in valores]
        d = np.max(np.abs(observados - esperados))
    else:
        distriOrd = sorted(distri)
        observados = [(i/N) for i in range(1, N+1)]
        esperados = [cdf(x, tipo, params) for x in distriOrd]
        d = max(abs(o - e) for o, e in zip(observados, esperados))
        
    crit = ksCrit/sqrt(N)
    print(f"D: {d:.6f}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if d <= crit else f'Prueba reprobada')

def main():
    muestras = {'1': 'muestras/cajas.txt', '2': 'muestras/refrescos.txt', '3': 'muestras/llegadas.txt', 
                '4': 'muestras/postres.txt', '5': 'muestras/ordenes.txt', '6': 'muestras/pollo.txt', '7': 'muestras/freidora.txt'}
    nomMuestras = {'1': 'Cajas', '2': 'Refrescos', '3': 'Llegadas', 
                   '4': 'Postres', '5': 'Órdenes', '6': 'Pollo', '7': 'Freidora'}
    tipo = {'1': 'exp', '2': 'exp', '3': 'exp', 
            '4': 'b', '5': 'b', '6': 'g', '7': 'nd'}
    while True:
        print("\n---------- MENÚ ----------")
        print("1. Muestra cajas")
        print("2. Muestra refrescos")
        print("3. Muestra llegadas")
        print("4. Muestra postres")
        print("5. Muestra ordenes")
        print("6. Muestra pollo")
        print("7. Muestra freidora")
        print("0. Salir")
        op = input("Opción: ")

        if op == '0':
            break

        if op in muestras:
            distri = obtenerDistri(muestras[op])
            N = len(distri)
            promedio, desvi = mediaDesvi(N, distri)
            bordes, bordesFrec, bordesGraf = None, None, None
            ksCrit = 1.36

            if tipo[op] == 'exp':
                params = (0, promedio)
                bordes = [x-0.5 for x in range(int(min(distri)), int(max(distri))+2)]
                bordesFrec = int(sqrt(N))
                bordesGraf = int(sqrt(N))

            if tipo[op] == 'nd':
                params = (3.0-0.5, 1.0)
                bordes = int(1+3.322*log10(N))
                bordesFrec = np.arange(int(min(distri))-0.5, int(max(distri))+1.5, 1)
                bordesGraf = bordesFrec

            if tipo[op] == 'b':
                params = (5, promedio/5) if op == '5' else (5, promedio/5)
                bordes = np.arange(int(min(distri))-0.5, int(max(distri))+1.5, 1)
                bordesFrec, bordesGraf = bordes, bordes

            if tipo[op] == 'g':
                params = (1/promedio,)
                bordes = np.arange(int(min(distri))-0.5, int(max(distri))+1.5, 1)
                bordesFrec, bordesGraf = bordes, bordes

            print(f"\n--- Muestra: {nomMuestras[op]} ---")
            print(f'Promedio: {promedio:.4f}')
            print(f'Varianza: {desvi*desvi:.4f}')
            print(f'Desviación estándar: {desvi:.4f}')
            grafFrec(N, distri, nomMuestras[op], bordesFrec)
            grafComparativa(N, distri, nomMuestras[op], tipo[op], params, bordesGraf)
            pruebaChi(N, distri, tipo[op], params, muestras[op].split('/')[-1].split('.')[0], bordes)
            pruebaKS(N, distri, tipo[op], params, ksCrit)

if __name__ == "__main__":
    main()