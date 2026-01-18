import numpy as np
import os

tiempoLimite = 480
randomGen = np.random.default_rng()

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
    for i in range(n+1):
        for resto in genCombi(n-i, k-1):
            yield (i+1,) + resto

def funNormalDisc(mu, sigma, minVal):
    val = randomGen.normal(loc=mu, scale=sigma)
    return int(val) if val >= minVal else 0

probsWorkflow = {"refrescos": 0.9, "freidora": 0.7, "postres": 0.25, "pollo": 0.3} 
tiempoServiMap = {
    "cajas": lambda: randomGen.exponential(scale=2.5),     
    "refrescos": lambda: randomGen.exponential(scale=0.75),   
    "freidora": lambda: funNormalDisc(mu=3, sigma=1, minVal=1),
    "postres": lambda: randomGen.binomial(n=5, p=0.6),
    "pollo": lambda: randomGen.geometric(p=0.1),
}

def tiempoServi(estacion):
    return tiempoServiMap[estacion]()

def genOrden():
    return [servicio for servicio, prob in probsWorkflow.items() if randomGen.random() <= prob]

def exeWorkflow(combServidor, imprimir):
    nombres = ['cajas','refrescos', 'freidora', 'postres', 'pollo']
    estaciones = {nombres[i]:Servidor(combServidor[i]) for i in range(5)}
    tiempoTotal = 0.0
    esperas = []
    tiempoEntreClientes = lambda: randomGen.exponential(scale=3.0)
    ordenDist = lambda: randomGen.binomial(n=5, p=0.4)
    
    if imprimir:
        print("\n" + "="*90)
        print(f"Traza (Config: {combServidor})")
        print(f"{'Num':<4} | {'Estación':<10} | {'Recurso':<10} | {'Llegada':<8} | {'Inicio':<8} | {'Duración':<8} | {'Fin':<8} | {'Espera':<8}")
        print("-" * 90)

    numCliente = 0
    while 1:
        tiempoTotal += tiempoEntreClientes()
        if (tiempoTotal>tiempoLimite): break
        numCliente += 1
        tiempoCliente = tiempoTotal 
        duracion = tiempoServiMap['cajas']()
        tiempoEspera, finCajas, indxEmple = estaciones['cajas'].procesar_cliente(tiempoCliente, duracion)
        
        if imprimir:
            print(f"{numCliente:<4} | {'Cajas':<10} | {f'Cajero {indxEmple}':<10} | {tiempoCliente:8.2f} | {tiempoCliente+tiempoEspera:8.2f} | {duracion:8.2f} | {finCajas:8.2f} | {tiempoEspera:8.2f}")

        inicioOrden = finCajas
        tiempoSalidaCliente = finCajas
        orden = genOrden()
        for _ in range(ordenDist()):
            for servicio in orden:
                duracion = tiempoServiMap[servicio]()
                tiempoEspera, fin, indxEmple = estaciones[servicio].procesar_cliente(inicioOrden, duracion)
                tiempoSalidaCliente = max(fin, tiempoSalidaCliente)
                if imprimir:
                    print(f"{'':<4} | {servicio:<10} | {f'Emp {indxEmple}':<10} | {inicioOrden:8.2f} | {inicioOrden+tiempoEspera:8.2f} | {duracion:8.2f} | {fin:8.2f} | {tiempoEspera:8.2f}")
        esperaTotal = tiempoSalidaCliente-tiempoCliente
        if imprimir: 
            print(
                f"{'':<4} | {'TOTAL':<10} | {'Cliente':<10} | "
                f"{tiempoCliente:8.2f} | {'':>8} | {'':>8} | {tiempoSalidaCliente:8.2f} | {esperaTotal:8.2f}"
            )
            if tiempoTotal <= tiempoLimite: print("-"*90)

        esperas.append(esperaTotal)
    return np.mean(esperas), np.var(esperas)

def saveFile(combi, media, var, carpeta, nombreArchi, modo, spaceStr, i):
    ruta = os.path.join(carpeta, nombreArchi)
    with open(ruta, modo) as f:
        f.write(f"---- {i}) Datos Configuración {combi} ----\n")
        f.write(f"Cajas:     {combi[0]}\n")
        f.write(f"Refrescos: {combi[1]}\n")
        f.write(f"Freidora:  {combi[2]}\n")
        f.write(f"Postres:   {combi[3]}\n")
        f.write(f"Pollo:     {combi[4]}\n")
        f.write(f"\nTiempo de Espera Promedio (W): {media:.4f}\n")
        f.write(f"Varianza (Var): {var:.4f}\n")
        f.write("-"*49+spaceStr)

def main():
    gen = genCombi(7, 5)
    globalBestBal   = (float('inf'), None, None) 
    globalBestMedia = (float('inf'), (0, 0), None)
    globalBestVar = (float('inf'), (0, 0), None)
    n = 1000
    open(os.path.join("configs", "config_all.txt"), "w").close()
    for i, combi in enumerate(gen):
        mediaL = varL = 0
        for a in range(n):
            show = not (a%(n//3))
            if show: print(f'Dia número {a}')
            m, v = exeWorkflow(combi, imprimir=show)
            mediaL += m
            varL +=v

        mediaL/=n
        varL/=n
        balance = mediaL+2*np.sqrt(varL)
        globalBestBal = min(globalBestBal, (balance, (mediaL, varL), combi))
        globalBestMedia = min(globalBestMedia, (mediaL, (mediaL, varL), combi))
        globalBestVar = min(globalBestVar, (varL, (mediaL, varL), combi))
        saveFile(combi, mediaL, varL, "configs", "config_all.txt", "a", "\n\n", i+1)
    
    saveFile(globalBestMedia[2], *globalBestMedia[1], "configs", "config_mejor_media.txt", "w", "", 1)
    saveFile(globalBestVar[2], *globalBestVar[1], "configs", "config_mejor_varianza.txt", "w", "", 1)
    saveFile(globalBestBal[2], *globalBestBal[1], "configs", "config_mejor_equilibrada.txt", "w", "", 1)

if __name__ == "__main__":
    main()