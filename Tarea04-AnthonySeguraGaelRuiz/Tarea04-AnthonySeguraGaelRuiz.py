from matplotlib.pylab import log10
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from scipy.stats import chi2, norm, nbinom, beta, uniform

def cdf(x, tipo, params, spicyParams):
    if tipo == 'n':
        return norm.cdf(x, *params)
    if tipo == 'nb':
        return nbinom.cdf(x, *params)
    if tipo == 'b':
        return beta.cdf(x, *(params+spicyParams))
    if tipo == 'ub':
        w, a, b = params
        l, r = spicyParams
        uniCDF = uniform.cdf(x, 0, 1)
        betaCDF = beta.cdf(x, a, b, loc=l, scale=r)
        return w * uniCDF + (1-w) * betaCDF
    return 0

def pf(x, tipo, params, spicyParams):
    if tipo == 'n':
        return norm.pdf(x, *params)
    if tipo == 'nb':
        return nbinom.pmf(int(x), *params)
    if tipo == 'b':
        return beta.pdf(x, *(params+spicyParams))
    if tipo == 'ub':
        w, a, b, = params
        l, r = spicyParams
        uniPDF = uniform.pdf(x, 0, 1)
        betaPDF = beta.pdf(x, a, b, loc=l, scale=r)
        return w * uniPDF + (1-w) * betaPDF
    return 0

def valCrit(grados, muestra):
    alpha = 0.05 if muestra in ['m3', 'm16'] else 0.01
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

def grafComparativa(N, distri, nomMuestra, tipo, params, bordes, spicyParams):
    plt.figure(figsize=(10, 6))
    plt.hist(distri, bins=bordes, density=True, color='lightgreen', edgecolor='black', alpha=0.6, label='Datos Muestra')
    xmin, xmax = plt.xlim()
    paramsTxt = ""
    if tipo == 'n':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, params, spicyParams) for val in x]
        paramsTxt = f"Normal (Media $\mu$={params[0]:.2f}, Desv $\sigma$={params[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')
        
    elif tipo == 'nb':
        x = np.arange(int(xmin), int(xmax) + 1)
        p = [pf(val, tipo, params, spicyParams) for val in x]
        paramsTxt = f"Neg.Binom (n={params[0]:.2f}, p={params[1]:.4f})"
        plt.plot(x, p, 'ro--', linewidth=2, label='Distribución Teórica')

    elif tipo == 'b':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, params, spicyParams) for val in x]
        paramsTxt = f"Beta (a={params[0]:.2f}, b={params[1]:.2f}, L={spicyParams[0]:.2f}, R={spicyParams[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')

    elif tipo == 'ub':
        x = np.linspace(xmin, xmax, 1000)
        p = [pf(val, tipo, params, spicyParams) for val in x]
        paramsTxt = f"Uniforme-Beta: 50% Unif(0,1) + 50% Beta (a={params[1]:.2f}, b={params[2]:.2f}, L={spicyParams[0]:.2f}, R={spicyParams[1]:.2f})"
        plt.plot(x, p, 'r', linewidth=3, label='Distribución Teórica')

    plt.title(f"Comparación: {nomMuestra}\nDistribución: {paramsTxt}", fontsize=14)
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def calcChiMuestra(N, distri, tipo, params, muestra, bordes, spicyParams):
    if muestra == 'm3' or muestra == 'm4':
        observados, _ = np.histogram(distri, bins=bordes)
        esperados = [(cdf(bordes[i+1], tipo, params, spicyParams)-cdf(bordes[i], tipo, params, spicyParams))*N for i in range(len(observados))]
        obs, esp = [], []
        sumObs, sumEps = 0, 0
        for o, e in zip(observados, esperados):
            sumObs += o
            sumEps += e
            if sumEps >= 5:
                obs.append(sumObs)
                esp.append(sumEps)
                sumObs, sumEps = 0, 0
        if sumEps > 0:
            if obs:
                obs[-1] += sumObs
                esp[-1] += sumEps
            else:
                obs.append(sumObs)
                esp.append(sumEps)
        observados, esperados = obs, esp
    
    elif muestra == 'm4':
        observados, _ = np.histogram(distri, bins=bordes)
        esperados = [(cdf(bordes[i+1], tipo, params, spicyParams)-cdf(bordes[i], tipo, params, spicyParams))*N for i in range(len(observados))]
        
    elif muestra == 'm16' or muestra == 'm15':
        observados, bordes = np.histogram(distri, bins=bordes)
        esperados = [(cdf(bordes[i+1], tipo, params, spicyParams)-cdf(bordes[i], tipo, params, spicyParams))*N for i in range(len(observados))]

    return observados, esperados

def pruebaChi(N, distri, tipo, params, muestra, bordes, spicyParams):
    print("\n--- Prueba de Chi^2 ---")
    observados, esperados = calcChiMuestra(N, distri, tipo, params, muestra, bordes, spicyParams)
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(observados, esperados) if fe)
    crit = valCrit(len(observados)-1-len(params), muestra)
    print(f"Chi^2: {chi}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if chi <= crit else f'Prueba reprobada')

def pruebaKS(N, distri, tipo, params, ksCrit, spicyParams):
    print("\n--- Prueba de Kolmogorov-Smirnov ---")
    distriOrd = sorted(distri)
    observados = [(i/N) for i in range(1, N+1)]
    esperados = [cdf(x, tipo, params, spicyParams) for x in distriOrd]
    d = max(abs(o - e) for o, e in zip(observados, esperados))
    crit = ksCrit/sqrt(N)
    print(f"D: {d:.6f}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if d <= crit else f'Prueba reprobada')

def main():
    muestras = {'1': 'muestras/m3.txt', '2': 'muestras/m4.txt', '3': 'muestras/m15.txt', '4': 'muestras/m16.txt'}
    nomMuestras = {'1': 'Muestra 1 (m3)', '2': 'Muestra 2 (m4)', '3': 'Muestra 3 (m15)', '4': 'Muestra 4 (m16)'}
    tipo = {'1': 'n', '2': 'nb', '3': 'ub', '4': 'b'}
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
            N = len(distri)
            promedio, desvi = mediaDesvi(N, distri)
            spicyParams = None

            if tipo[op] == 'n':
                params = (promedio, desvi)
                ksCrit = 1.73

            elif tipo[op] == 'nb':
                p = promedio/(desvi*desvi)
                r = (promedio*p)/(1-p)
                params = (r, p)
                ksCrit = 1.36
            
            elif tipo[op] == 'b':
                L = min(distri)    
                R = max(distri)-L
                promedioB = (promedio-L)/R
                varianzaB = (desvi*desvi)/(R * R)
                a = promedioB*((promedioB*(1-promedioB)) / varianzaB-1)
                b = a*(1-promedioB)/promedioB
                params, spicyParams = (a, b), (L, R)
                ksCrit = 1.36

            elif tipo[op] == 'ub':
                umbral = 1.25
                uniDatos = [x for x in distri if x < umbral]
                betaDatos = [x for x in distri if x >= umbral]
                w = len(uniDatos)/N
                L = min(betaDatos)
                R = max(betaDatos)-L
                betaMedia, betaVar = np.mean(betaDatos), np.var(betaDatos, ddof=1)
                betaPromN = (betaMedia-L)/R
                betaVarN = betaVar/(R*R)
                a = betaPromN * ((betaPromN*(1-betaPromN))/betaVarN-1)
                b = a * (1-betaPromN)/betaPromN
                params, spicyParams = (w, a, b), (L, R)
                ksCrit = 1.63

            bordes = int(1+3.322*log10(N)) if tipo[op] == 'ub' else [x-0.5 for x in range(int(min(distri)), int(max(distri))+2)]
            print(f"\n--- Muestra: {nomMuestras[op]} ---")
            print(f'Promedio: {promedio:.4f}')
            print(f'Varianza: {desvi*desvi:.4f}')
            print(f'Desviación estándar: {desvi:.4f}')
            grafFrec(N, distri, nomMuestras[op], bordes)
            grafComparativa(N, distri, nomMuestras[op], tipo[op], params, bordes, spicyParams)
            pruebaChi(N, distri, tipo[op], params, muestras[op].split('/')[-1].split('.')[0], bordes, spicyParams)
            pruebaKS(N, distri, tipo[op], params, ksCrit, spicyParams)

if __name__ == "__main__":
    main()