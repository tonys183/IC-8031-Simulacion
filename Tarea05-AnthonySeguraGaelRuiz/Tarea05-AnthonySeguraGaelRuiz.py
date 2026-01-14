from scipy.stats import  expon, binom, geom, truncnorm
import numpy as np
import os

tiempoLimite = 480

class Servidor:
    def __init__(self, numEmple):
        self.empleadosLibresHasta = [0.0]*numEmple
        
    def procesar_cliente(self, tiempoLlegada, duracion):
        masCerca = min(self.empleadosLibresHasta)
        indxEmple = self.empleadosLibresHasta.index(masCerca)
        inicioAtenc = max(tiempoLlegada, masCerca)
        tiempoEspera = inicioAtenc-tiempoLlegada
        finAtenc = inicioAtenc+duracion
        self.empleadosLibresHasta[indxEmple] = finAtenc
        return tiempoEspera, finAtenc, indxEmple

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

def exeWorkflow(combServidor, imprimir):
    nombres = ['cajas','refrescos', 'freidora', 'postres', 'pollo']
    estaciones = {nombres[i]:Servidor(combServidor[i]) for i in range(5)}
    tiempoTotal = 0.0
    esperas = []
    tiempoEntreClientes = lambda: expon(scale=3.0).rvs()
    ordenDist = lambda: binom(n=5, p=0.4).rvs()
    
    if imprimir:
        print("\n" + "="*90)
        print(f"Traza (Config: {combServidor})")
        print(f"{'Num':<4} | {'Estación':<10} | {'Recurso':<10} | {'Llegada':<8} | {'Inicio':<8} | {'Duración':<8} | {'Fin':<8} | {'Espera':<8}")
        print("-" * 90)

    numCliente = 0
    while tiempoTotal < tiempoLimite:
        tiempoTotal += tiempoEntreClientes()
        numCliente += 1
        tiempoCliente = tiempoTotal 
        duracion = tiempoServiMap['cajas']()
        tiempoEspera, finCajas, indxEmple = estaciones['cajas'].procesar_cliente(tiempoCliente, duracion)
        
        if imprimir and tiempoTotal < tiempoLimite:
            print(f"{numCliente:<4} | {'Cajas':<10} | {f'Cajero {indxEmple}':<10} | {tiempoCliente:8.2f} | {tiempoCliente+tiempoEspera:8.2f} | {duracion:8.2f} | {finCajas:8.2f} | {tiempoEspera:8.2f}")

        inicioOrden = finCajas
        tiempoSalidaCliente = finCajas
        orden = genOrden()
        for _ in range(ordenDist()):
            for servicio in orden:
                duracion = tiempoServiMap[servicio]()
                tiempoEspera, fin, indxEmple = estaciones[servicio].procesar_cliente(inicioOrden, duracion)
                tiempoSalidaCliente = max(fin, tiempoSalidaCliente)
                if imprimir and tiempoTotal < tiempoLimite:
                    print(f"{'':<4} | {servicio:<10} | {f'Emp {indxEmple}':<10} | {inicioOrden:8.2f} | {inicioOrden+tiempoEspera:8.2f} | {duracion:8.2f} | {fin:8.2f} | {tiempoEspera:8.2f}")
        
        if imprimir and tiempoTotal < tiempoLimite: print("-"*90)
        esperas.append(tiempoSalidaCliente-tiempoCliente)

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
    n = 5
    for _, combi in enumerate(gen):
        mediaL = varL = 0
        for _ in range(n):
            m, v = exeWorkflow(combi, imprimir=False)
            mediaL += m
            varL +=v

        mediaL/=n
        varL/=n
        globalBestMedia = min(globalBestMedia, (mediaL, (mediaL, varL), combi))
        globalBestVar = min(globalBestVar, (varL, (mediaL, varL), combi))

        nombreArchi = f"config_{combi[0]}_{combi[1]}_{combi[2]}_{combi[3]}_{combi[4]}.txt"
        saveFile(combi, mediaL, varL, "configs", nombreArchi)
    
    saveFile(globalBestMedia[2], *globalBestMedia[1], "configs", "config_mejor_media.txt")
    saveFile(globalBestVar[2], *globalBestVar[1], "configs", "config_mejor_varianza.txt")

if __name__ == "__main__":
    main()