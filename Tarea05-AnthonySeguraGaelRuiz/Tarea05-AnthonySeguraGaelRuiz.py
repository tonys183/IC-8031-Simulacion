from scipy.stats import  expon, binom, geom, truncnorm
import numpy as np
import os

probsWorkflow = {"refrescos": 0.9, "freidora": 0.7, "postres": 0.25, "pollo": 0.3} 
tiempoLimite = 480 

class Servidor:
    def __init__(self, num_empleados):
        self.empleados_libres_hasta = [0.0] * num_empleados
        
    def procesar_cliente(self, tiempo_llegada, duracion_servicio):
        turno_mas_pronto = min(self.empleados_libres_hasta)
        idx_empleado = self.empleados_libres_hasta.index(turno_mas_pronto)
        inicio_atencion = max(tiempo_llegada, turno_mas_pronto)
        
        tiempo_espera = inicio_atencion - tiempo_llegada
        fin_atencion = inicio_atencion + duracion_servicio
        self.empleados_libres_hasta[idx_empleado] = fin_atencion
        
        return tiempo_espera, fin_atencion

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
    tiempoEntreClientes = lambda: expon(scale=1/3).rvs()
    ordenDist = lambda: binom(n=5, p=0.4).rvs()
    while tiempoTotal < tiempoLimite:
        tiempoTotal += tiempoEntreClientes()
        tiempoCliente = tiempoTotal
        #print(f'Tiempo actual: {tiempoTotal}')
        _, fin = estaciones['cajas'].procesar_cliente(tiempoCliente, tiempoServiMap['cajas']())
        tiempoSalidaCliente = fin
        
        orden = genOrden()
        for _ in range(ordenDist()):
            for servicio in orden:
                _, fin = estaciones[servicio].procesar_cliente(tiempoCliente, tiempoServiMap[servicio]())
                tiempoSalidaCliente = max(fin, tiempoSalidaCliente)

        if (tiempoSalidaCliente<tiempoLimite): esperas.append(tiempoSalidaCliente-tiempoCliente)

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
    mediaCombiOptima = varCombiOptima = (float('inf'),float('inf'))
    bestMediaCombi = ()
    bestVarComb = ()
    for i, combi in enumerate(gen):
        mejorMedia = float('inf')
        mejorVar = float('inf')
        for _ in range(5):
            m, v = exeWorkflow(combi)
            mejorMedia, mejorVar = min(mejorMedia, m), min(mejorVar, v)

        if (mejorMedia>mediaCombiOptima[0]):
            bestMediaCombi = combi
            mediaCombiOptima = (mejorMedia,mejorVar)

        if (mejorVar>varCombiOptima[1]):
            bestVarComb = combi
            varCombiOptima = (mejorMedia,mejorVar)

        nombreArchi = f"config_{combi[0]}_{combi[1]}_{combi[2]}_{combi[3]}_{combi[4]}.txt"
        saveFile(combi, mejorMedia, mejorVar, "configs", nombreArchi)
    
    saveFile(bestMediaCombi, *mediaCombiOptima, "configs", "config_mejor_media.txt")
    saveFile(bestVarComb, *varCombiOptima, "configs", "config_mejor_varianza.txt")

if __name__ == "__main__":
    main()