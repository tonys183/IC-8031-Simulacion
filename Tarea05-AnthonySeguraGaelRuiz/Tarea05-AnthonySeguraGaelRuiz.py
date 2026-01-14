from scipy.stats import  expon, binom, geom, truncnorm
import numpy as np
import os

class Servidor:
    def __init__(self, numEmple):
        self.empleadosLibresHasta = [0.0]*numEmple
        
    def procesar_cliente(self, tiempoLlegada, duracion):
        masCerca = min(self.empleadosLibresHasta)
        inicioAtenc = max(tiempoLlegada, masCerca)
        tiempoEspera = inicioAtenc-tiempoLlegada
        finAtenc = inicioAtenc+duracion
        self.empleadosLibresHasta[self.empleadosLibresHasta.index(masCerca)] = finAtenc
        return tiempoEspera, finAtenc

def genCombi(n, k):
    if k == 1:
        yield (n+1,)
        return
    for i in range(n + 1):
        for resto in genCombi(n - i, k - 1):
            yield (i+1,) + resto

def funNormalDisc(mu, sigma, minVal):
    a = (minVal-mu)/sigma
    return lambda: int(np.round(truncnorm(a, np.inf, loc=mu, scale=sigma).rvs()))

probsWorkflow = {"refrescos": 0.9, "freidora": 0.7, "postres": 0.25, "pollo": 0.3} 
tiempoServiMap = {
    "cajas": lambda: expon(scale=2.5).rvs(),     
    "refrescos": lambda: expon(scale=0.75).rvs(),   
    "freidora": funNormalDisc(mu=3, sigma=0.5, minVal=1),
    "postres": lambda: binom(n=5, p=0.6).rvs(),
    "pollo": lambda: geom(p=0.1).rvs(),
}

def tiempoServi(estacion):
    return tiempoServiMap[estacion]()

def genOrden():
    return [servicio for servicio, prob in probsWorkflow.items() if np.random.random() <= prob]

def exeWorkflow(combServidor):
    nombres = ['cajas','refrescos', 'freidora', 'postres', 'pollo']
    estaciones = {nombres[i]:Servidor(combServidor[i]) for i in range(5)}
    tiempoTotal = 0.0
    esperas = []
    tiempoEntreClientes = lambda: expon(scale=3.0).rvs()
    ordenDist = lambda: binom(n=5, p=0.4).rvs()
    while tiempoTotal < 480:
        tiempoTotal += tiempoEntreClientes()
        tiempoCliente = tiempoTotal
        #print(f'Tiempo actual: {tiempoTotal}')
        _, finCajas = estaciones['cajas'].procesar_cliente(tiempoCliente, tiempoServiMap['cajas']())
        inicioOrden = finCajas
        tiempoSalidaCliente = finCajas
        orden = genOrden()
        for _ in range(ordenDist()):
            for servicio in orden:
                _, fin = estaciones[servicio].procesar_cliente(inicioOrden, tiempoServiMap[servicio]())
                tiempoSalidaCliente = max(fin, tiempoSalidaCliente)

        esperas.append(tiempoSalidaCliente-tiempoCliente)

    if not esperas: return float('inf'), float('inf')
    return np.mean(esperas), np.var(esperas)

def saveFile(combi, mejorMedia, mejorVar, carpeta, nombreArchi):
    ruta = os.path.join(carpeta, nombreArchi)
    with open(ruta, "w") as f:
        f.write("--- REPORTE DE CONFIGURACIÓN ---\n")
        f.write(f"Cajas:     {combi[0]}\n")
        f.write(f"Refrescos: {combi[1]}\n")
        f.write(f"Freidora:  {combi[2]}\n")
        f.write(f"Postres:   {combi[3]}\n")
        f.write(f"Pollo:     {combi[4]}\n")
        f.write("-" * 32 + "\n")
        f.write(f"Tiempo de Espera Promedio (W): {mejorMedia:.4f}\n")
        f.write(f"Varianza (Var): {mejorVar:.4f}\n")

def main():
    gen = genCombi(7, 5)
    gen = sorted(gen, key=np.var)
    globalBestMedia = (float('inf'), (0, 0), None)
    globalBestVar = (float('inf'), (0, 0), None)

    for _, combi in enumerate(gen):
        localMejor = (float('inf'), float('inf'))
        for _ in range(5):
            m, v = exeWorkflow(combi)
            localMejor = min(localMejor, (m, v))

            globalBestMedia = min(globalBestMedia, (m, (m, v), combi))
            globalBestVar = min(globalBestVar, (v, (m, v), combi))

        nombreArchi = f"config_{combi[0]}_{combi[1]}_{combi[2]}_{combi[3]}_{combi[4]}.txt"
        saveFile(combi, localMejor[0], localMejor[1], "configs", nombreArchi)
    
    saveFile(globalBestMedia[2], *globalBestMedia[1], "configs", "config_mejor_media.txt")
    saveFile(globalBestVar[2], *globalBestVar[1], "configs", "config_mejor_varianza.txt")

if __name__ == "__main__":
    main()