import numpy as np
import os

randomGen = np.random.default_rng()
tiempoLimite = 480

class Servidor:
    def __init__(self, numEmple):
        self.empleadosLibresHasta = [0.0]*numEmple

    def atender(self, tiempoLlegada, duracion):
        masCerca = min(self.empleadosLibresHasta)
        indxEmple = self.empleadosLibresHasta.index(masCerca)
        inicioAtenc = max(tiempoLlegada, masCerca)
        tiempoEspera = inicioAtenc-tiempoLlegada
        finAtenc = inicioAtenc+duracion
        self.empleadosLibresHasta[indxEmple] = finAtenc
        return tiempoEspera, finAtenc, indxEmple

def elegirObjetos(mapaObjetos, capacidad):
    if capacidad < min(mapaObjetos.values()):
        yield ()
        return

    for servicio,precio in mapaObjetos.items():
        if precio>capacidad: 
            continue
        for resto in elegirObjetos(mapaObjetos, capacidad-precio):
            yield (servicio,) + resto

def genCombi(mapaObjetos, capacidad):
    servicios = list(mapaObjetos.keys())
    vistos = set()
    capacidad -= sum(mapaObjetos.values())
    for combi in elegirObjetos(mapaObjetos, capacidad):
        tupla = tuple(combi.count(s)+1 for s in servicios)
        if tupla not in vistos:
            vistos.add(tupla)
            yield tupla

def compararPar(esperasPorEstacion, a, b):
    dataA = np.array(esperasPorEstacion[a])
    dataB = np.array(esperasPorEstacion[b])
    _, indxA, indxB = np.intersect1d(dataA[:, 0], dataB[:, 0], return_indices=True)
    if len(indxA) < 2:
        return np.nan
    return float(np.cov(dataA[:, 1][indxA], dataB[:, 1][indxB])[0, 1])

def covarianzas(esperasPorEstacion, nombres):
    out = {}
    for i in range(len(nombres)):
        for j in range(i+1, len(nombres)):
            a, b = nombres[i], nombres[j]
            out[f"{a}-{b}"] = compararPar(esperasPorEstacion, a, b)
    return out

def estadisticas(esperas, esperasPorEstacion, nombres):
    x = np.array(esperas)
    resultado = {
        "media": float(np.mean(x)),
        "mediana": float(np.median(x)),
        "varianza": float(np.var(x, ddof=0)),
        "moda": int(np.bincount(np.floor(x).astype(int)).argmax()) if len(x) else 0,
        "minimo": float(np.min(x)) if len(x) else float("nan"),
        "maximo": float(np.max(x)) if len(x) else float("nan"),
        "rango": float(np.max(x)-np.min(x)) if len(x) else float("nan"),
        "cuartiles": {
            "Q1": float(np.percentile(x, 25)) if len(x) else float("nan"),
            "Q2": float(np.percentile(x, 50)) if len(x) else float("nan"),
            "Q3": float(np.percentile(x, 75)) if len(x) else float("nan"),
        },
        "percentiles": {
            "P10": float(np.percentile(x, 10)) if len(x) else float("nan"),
            "P25": float(np.percentile(x, 25)) if len(x) else float("nan"),
            "P50": float(np.percentile(x, 50)) if len(x) else float("nan"),
            "P75": float(np.percentile(x, 75)) if len(x) else float("nan"),
            "P90": float(np.percentile(x, 90)) if len(x) else float("nan"),
        }
    }
    resultado["covarianzas"] = covarianzas(esperasPorEstacion, nombres)
    resultado["muestra"] = {
        "orden_estaciones": list(nombres),
        "tiempos_totales": [float(v) for v in esperas],
        "tiempos_por_estacion": {
            nombre: [float(row[1]) for row in esperasPorEstacion.get(nombre, [])]
            for nombre in nombres
        }
    }
    return resultado

def funNormalDisc(mu, sigma, minVal):
    val = randomGen.normal(loc=mu, scale=sigma)
    return int(val) if val >= minVal else 0

ordenDist = lambda: randomGen.binomial(n=5, p=0.4)
tiempoEntreClientes = lambda: randomGen.exponential(scale=3.0)
tiempoServiMap = {
    "cajas": lambda: randomGen.exponential(scale=2.5),
    "refrescos": lambda: randomGen.exponential(scale=0.75),
    "freidora": lambda: funNormalDisc(mu=3, sigma=1, minVal=1),
    "postres": lambda: randomGen.binomial(n=5, p=0.6),
    "pollo": lambda: randomGen.geometric(p=0.1),
}

def tiempoServi(estacion):
    return tiempoServiMap[estacion]()

def genOrden(probsWorkflow):
    return [servicio for servicio, prob in probsWorkflow.items() if randomGen.random() <= prob]

def exeWorkflow(combServidor, probsWorkflow, imprimir):
    nombres = ["cajas"] + list(probsWorkflow.keys())
    estaciones = {nombres[i]: Servidor(combServidor[i]) for i in range(len(combServidor))}
    tiempoTotal = 0.0
    esperas = []

    if imprimir:
        print("\n" + "="*90)
        print(f"Traza (Config: {combServidor})")
        print(f"{'Num':<4} | {'Estación':<10} | {'Recurso':<10} | {'Llegada':<8} | {'Inicio':<8} | {'Duración':<8} | {'Fin':<8} | {'Espera':<8}")
        print("-" * 90)

    numCliente = 0
    tiempoPorEstacion = {nombre: 0.0 for nombre in nombres}
    esperasPorEstacion = {nombre: [] for nombre in nombres}

    while True:
        tiempoTotal += tiempoEntreClientes()
        if tiempoTotal > tiempoLimite:
            break

        numCliente += 1
        tiempoCliente = tiempoTotal

        duracion = tiempoServiMap['cajas']()
        tiempoEspera, finCajas, indxEmple = estaciones['cajas'].atender(tiempoCliente, duracion)
        esperasPorEstacion['cajas'].append([numCliente, finCajas - tiempoCliente])

        if imprimir:
            print(f"{numCliente:<4} | {'Cajas':<10} | {f'Cajero {indxEmple}':<10} | {tiempoCliente:8.2f} | {tiempoCliente+tiempoEspera:8.2f} | {duracion:8.2f} | {finCajas:8.2f} | {tiempoEspera:8.2f}")

        inicioOrden = finCajas
        tiempoSalidaCliente = finCajas
        orden = genOrden(probsWorkflow)

        for _ in range(ordenDist()):
            for servicio in orden:
                duracion = tiempoServiMap[servicio]()
                tiempoEspera, fin, indxEmple = estaciones[servicio].atender(inicioOrden, duracion)

                tiempoSalidaCliente = max(fin, tiempoSalidaCliente)


                tiempoPorEstacion[servicio] = max((fin - inicioOrden), tiempoPorEstacion[servicio])

                if imprimir:
                    print(f"{'':<4} | {servicio:<10} | {f'Emp {indxEmple}':<10} | {inicioOrden:8.2f} | {inicioOrden+tiempoEspera:8.2f} | {duracion:8.2f} | {fin:8.2f} | {tiempoEspera:8.2f}")

        esperaTotal = tiempoSalidaCliente - tiempoCliente

        for servicio in nombres:
            if not tiempoPorEstacion[servicio]:
                continue
            esperasPorEstacion[servicio].append([numCliente, tiempoPorEstacion[servicio]])
            tiempoPorEstacion[servicio] = 0.0

        if imprimir:
            print(
                f"{'':<4} | {'TOTAL':<10} | {'Cliente':<10} | "
                f"{tiempoCliente:8.2f} | {'':>8} | {'':>8} | {tiempoSalidaCliente:8.2f} | {esperaTotal:8.2f}"
            )
            if tiempoTotal <= tiempoLimite:
                print("-"*90)

        esperas.append(esperaTotal)

    return estadisticas(esperas, esperasPorEstacion, nombres)

def _write_values_csv_like(f, valores, per_line=12, decimals=5):
    if not valores:
        f.write("(sin datos)\n")
        return
    fmt = "{:." + str(decimals) + "f}"
    for i, v in enumerate(valores, start=1):
        f.write(fmt.format(float(v)))
        if i != len(valores):
            f.write(", ")
        if i % per_line == 0:
            f.write("\n")
    if len(valores) % per_line != 0:
        f.write("\n")

def escribirEstadisticas(f, stats, incluir_datos_crudos=True):
    f.write("\n--- Estadísticas de la muestra simulada ---\n")
    f.write(f"Media:    {stats['media']:.4f}\n")
    f.write(f"Mediana:  {stats['mediana']:.4f}\n")
    f.write(f"Varianza: {stats['varianza']:.4f}\n")
    f.write(f"Moda:     {stats['moda']}\n")
    f.write(f"Mínimo:   {stats['minimo']:.4f}\n")
    f.write(f"Máximo:   {stats['maximo']:.4f}\n")
    f.write(f"Rango:    {stats['rango']:.4f}\n")

    cu = stats.get('cuartiles', {})
    if cu:
        f.write("Cuartiles:\n")
        f.write(f"  Q1: {cu.get('Q1', float('nan')):.4f}\n")
        f.write(f"  Q2: {cu.get('Q2', float('nan')):.4f}\n")
        f.write(f"  Q3: {cu.get('Q3', float('nan')):.4f}\n")

    pe = stats.get('percentiles', {})
    if pe:
        f.write("Percentiles:\n")
        for k in ['P10','P25','P50','P75','P90']:
            if k in pe:
                f.write(f"  {k}: {pe[k]:.4f}\n")

    covs = stats.get('covarianzas', {})
    if covs:
        f.write("Covarianzas (por par de estaciones):\n")
        for par, val in covs.items():
            if np.isnan(val):
                f.write(f"  {par}: NaN\n")
            else:
                f.write(f"  {par}: {val:.4f}\n")

    if incluir_datos_crudos and 'muestra' in stats:
        raw = stats['muestra']
        f.write("\n--- Datos crudos (tiempos de servicio) ---\n")
        totales = raw.get('tiempos_totales', [])
        f.write(f"Clientes simulados (total): {len(totales)}\n\n")

        f.write("Tiempos de servicio (total por cliente, en minutos):\n")
        _write_values_csv_like(f, totales)

        estaciones = raw.get('orden_estaciones', list(raw.get('tiempos_por_estacion', {}).keys()))
        por_est = raw.get('tiempos_por_estacion', {})

        for nombre in estaciones:
            vals = por_est.get(nombre, [])
            f.write(f"\nTiempos de servicio - estación '{nombre}' (min) | N={len(vals)}:\n")
            _write_values_csv_like(f, vals)

def saveFile(combi, media, var, carpeta, nombreArchi, modo, spaceStr, i, stats_muestra=None):
    ruta = os.path.join(carpeta, nombreArchi)
    with open(ruta, modo) as f:
        f.write(f"---- {i}) Datos Configuración {combi} ----\n")
        f.write(f"Cajas:     {combi[0]}\n")
        f.write(f"Refrescos: {combi[1]}\n")
        f.write(f"Freidora:  {combi[2]}\n")
        f.write(f"Postres:   {combi[4]}\n")
        f.write(f"Pollo:     {combi[3]}\n")
        f.write(f"\nTiempo de Espera Promedio (W): {media:.4f}\n")
        f.write(f"Varianza (Var): {var:.4f}\n")

        if stats_muestra is not None:
            escribirEstadisticas(f, stats_muestra, incluir_datos_crudos=True)

        f.write("-"*49 + spaceStr)

def saveTop3Configs(top3, probsWorkflow, carpeta="configs", nombreArchi="config_mejor_trio.txt"):
    ruta = os.path.join(carpeta, nombreArchi)
    with open(ruta, "w") as f:
        for i, (media, var, combi) in enumerate(top3, start=1):
            f.write(f"==== TOP {i} (menor W promedio) ====\n")
            f.write(f"Configuración: {combi}\n")
            f.write(f"Cajas:     {combi[0]}\n")
            f.write(f"Refrescos: {combi[1]}\n")
            f.write(f"Freidora:  {combi[2]}\n")
            f.write(f"Pollo:     {combi[3]}\n")
            f.write(f"Postres:   {combi[4]}\n")
            f.write(f"\nTiempo de Espera Promedio (W): {media:.4f}\n")
            f.write(f"Varianza (Var): {var:.4f}\n")

            stats_muestra = exeWorkflow(combi, probsWorkflow, imprimir=False)
            escribirEstadisticas(f, stats_muestra, incluir_datos_crudos=True)

            if i != len(top3):
                f.write("\n" + "="*55 + "\n\n")

def main():
    servicios = {"cajas": 500, "refrescos": 750, "freidora": 200, "pollo": 100}
    precio, n = 2000, 1000
    os.makedirs("configs", exist_ok=True)
    gen = genCombi(servicios, precio)
    globalBestBal   = (float('inf'), None, None)
    globalBestMedia = (float('inf'), (0, 0), None)
    globalBestVar   = (float('inf'), (0, 0), None)
    open(os.path.join("configs", "config_all.txt"), "w").close()
    probsWorkflow = {"refrescos": 0.9, "freidora": 0.7, "pollo": 0.3, "postres": 0.25}
    top3 = []
    postres = (5,)

    for i, combi in enumerate(gen):
        combi += postres
        mediaL = 0.0
        varL = 0.0
        res_last = None

        for _ in range(n):
            res_last = exeWorkflow(combi, probsWorkflow, imprimir=False)
            mediaL += res_last["media"]
            varL += res_last["varianza"]

        mediaL /= n
        varL /= n
        balance = mediaL + 2 * np.sqrt(varL)

        globalBestBal = min(globalBestBal, (balance, (mediaL, varL), combi))
        globalBestMedia = min(globalBestMedia, (mediaL, (mediaL, varL), combi))
        globalBestVar = min(globalBestVar, (varL, (mediaL, varL), combi))
        saveFile(combi, mediaL, varL, "configs", "config_all.txt", "a", "\n\n", i + 1, stats_muestra=res_last)
        top3.append((mediaL, varL, combi))
        top3.sort(key=lambda t: t[0])
        top3 = top3[:3]

    saveTop3Configs(top3, probsWorkflow, "configs", "config_mejor_trio.txt")

if __name__ == "__main__":
    main()