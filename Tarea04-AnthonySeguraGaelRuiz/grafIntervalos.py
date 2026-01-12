from matplotlib.pylab import log10
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from scipy.stats import chi2, norm, nbinom, beta, uniform

def graficarObsvsEsp(observados, esperados, intervalos):
    plt.figure(figsize=(10, 6))
    MAX_BARRAS = 15 
    n_datos = len(observados)
    if n_datos <= MAX_BARRAS:
        obs_graf = observados
        esp_graf = esperados
        etiq_graf = intervalos
        rotacion = 45 
        fontsize = 9
    else:
        import math
        tamano_grupo = math.ceil(n_datos / MAX_BARRAS)
        obs_graf, esp_graf, etiq_graf = [], [], []
        
        for i in range(0, n_datos, tamano_grupo):
            # Sumar el bloque de Observados
            bloque_o = observados[i : i + tamano_grupo]
            obs_graf.append(sum(bloque_o))
            
            # Sumar el bloque de Esperados
            bloque_e = esperados[i : i + tamano_grupo]
            esp_graf.append(sum(bloque_e))
            
            # Crear etiqueta del rango (Desde el primero del grupo hasta el último)
            if intervalos:
                # Tomamos la parte inicial del primer intervalo y final del último
                # Asumiendo formato "[num, num)"
                inicio = intervalos[i].split(",")[0] # "[370"
                # Cuidado con el índice final si es el último bloque
                idx_fin = min(i + tamano_grupo - 1, n_datos - 1)
                fin = intervalos[idx_fin].split(",")[1] # " 405)"
                etiq_graf.append(f"{inicio}, {fin}")
            else:
                etiq_graf.append(f"G{len(obs_graf)}")
                
        rotacion = 45
        fontsize = 9

    # --- GRAFICACIÓN ---
    n_grupos = len(obs_graf)
    indice = np.arange(n_grupos)
    ancho_barra = 0.35

    # Barras Observadas (Azul)
    plt.bar(indice, obs_graf, ancho_barra, label='Observados ($O_i$)', 
            color='#5DA5DA', edgecolor='white', linewidth=0.5, alpha=0.9)
    
    # Barras Esperadas (Naranja)
    plt.bar(indice + ancho_barra, esp_graf, ancho_barra, label='Esperados ($E_i$)', 
            color='#FAA43A', edgecolor='white', linewidth=0.5, alpha=0.9)

    plt.xlabel('Intervalos Agrupados', fontsize=11)
    plt.ylabel('Frecuencia Acumulada', fontsize=11)
    plt.title('Bondad de Ajuste: Observados vs. Esperados (Agrupado)', fontsize=13)
    
    # Ajustar etiquetas eje X
    plt.xticks(indice + ancho_barra / 2, etiq_graf, rotation=rotacion, ha='right', fontsize=fontsize)
    
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

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
    # Calcular histograma inicial
    observados_raw, _ = np.histogram(distri, bins=bordes)
    
    # Calcular esperados iniciales
    esperados_raw = []
    for i in range(len(observados_raw)):
        # Probabilidad acumulada superior menos inferior
        p_sup = cdf(bordes[i+1], tipo, params, spicyParams)
        p_inf = cdf(bordes[i], tipo, params, spicyParams)
        esperados_raw.append((p_sup - p_inf) * N)

    # Agrupación (pooling) para asegurar frecuencias esperadas >= 5
    obs_final, esp_final, inter_final = [], [], []
    sumObs, sumEps = 0, 0
    start_bound = bordes[0] # Inicio del intervalo actual
    
    for i in range(len(observados_raw)):
        sumObs += observados_raw[i]
        sumEps += esperados_raw[i]
        
        # Si acumulamos suficiente frecuencia esperada, cerramos el intervalo
        # (O si es el último bucket y no hemos llegado, se sumará al anterior después)
        if sumEps >= 5:
            obs_final.append(sumObs)
            esp_final.append(sumEps)
            
            # Formato de etiqueta para la tabla
            end_bound = bordes[i+1]
            label = f"[{start_bound:.2f}, {end_bound:.2f})"
            inter_final.append(label)
            
            # Resetear acumuladores
            sumObs, sumEps = 0, 0
            start_bound = end_bound # El siguiente empieza donde terminó este

    # Manejo del remanente (si lo último sumó < 5)
    if sumEps > 0:
        if obs_final:
            obs_final[-1] += sumObs
            esp_final[-1] += sumEps
            # Actualizar la etiqueta del último intervalo existente
            last_label = inter_final[-1]
            # Tomamos el inicio del ultimo intervalo y el fin del remanente
            inicio = last_label.split(",")[0][1:] # Quitar corchete
            inter_final[-1] = f"[{inicio}, {bordes[-1]:.2f}]"
        else:
            # Caso raro: N total es muy pequeño
            obs_final.append(sumObs)
            esp_final.append(sumEps)
            inter_final.append(f"[{bordes[0]:.2f}, {bordes[-1]:.2f}]")

    return obs_final, esp_final, inter_final

def pruebaChi(N, distri, tipo, params, muestra, bordes, spicyParams):
    print("\n--- Prueba de Chi^2 ---")
    observados, esperados, intervalos = calcChiMuestra(N, distri, tipo, params, muestra, bordes, spicyParams)
    chi = sum((fo-fe)*(fo-fe)/fe for fo, fe in zip(observados, esperados) if fe)
    crit = valCrit(len(observados)-1-len(params), muestra)
    print(f"Chi^2: {chi}")
    print(f"Valor crítico: {crit:.6f}")
    print(f'Prueba aprobada' if chi <= crit else f'Prueba reprobada')
    graficarObsvsEsp(observados, esperados, intervalos)

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

            elif tipo[op] == 'b':
                L = min(distri)    
                R = max(distri)-L
                promedioB = (promedio-L)/R
                varianzaB = (desvi*desvi)/(R*R)
                a = promedioB*((promedioB*(1-promedioB)) / varianzaB-1)
                b = a*(1-promedioB)/promedioB
                params, spicyParams = (a, b), (L, R)
                ksCrit = 1.36

            if tipo[op] == 'ub':
                # 1. Calculamos la cantidad de intervalos (Regla de Sturges)
                num_bins = int(1 + 3.322 * log10(N))
                # 2. Generamos la LISTA de bordes exactos usando linspace
                # Esto crea una lista desde el min hasta el max con 'num_bins' divisiones
                bordes = np.linspace(min(distri), max(distri), num_bins + 1)
            else:
                # Lógica para las otras distribuciones (enteros centrados)
                bordes = [x-0.5 for x in range(int(min(distri)), int(max(distri))+2)]
            
            # -----------------------
            bordesFrec = bordes if tipo[op] == 'nb' else int(sqrt(N))
            bordesGraf = bordes if tipo[op] == 'n' or tipo[op] == 'nb' else int(sqrt(N))
            print(f"\n--- Muestra: {nomMuestras[op]} ---")
            print(f'Promedio: {promedio:.4f}')
            print(f'Varianza: {desvi*desvi:.4f}')
            print(f'Desviación estándar: {desvi:.4f}')
            grafFrec(N, distri, nomMuestras[op], bordesFrec)
            grafComparativa(N, distri, nomMuestras[op], tipo[op], params, bordesGraf, spicyParams)
            pruebaChi(N, distri, tipo[op], params, muestras[op].split('/')[-1].split('.')[0], bordes, spicyParams)
            pruebaKS(N, distri, tipo[op], params, ksCrit, spicyParams)

if __name__ == "__main__":
    main()