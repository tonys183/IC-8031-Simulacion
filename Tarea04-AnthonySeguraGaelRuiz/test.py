from fitter import Fitter

def obtenerDistri(nombreArchivo):
    with open(nombreArchivo, 'r') as archivo:
        return [float(linea.strip()) for linea in archivo]

def detectar_distribucion(nombreArchivo):
    distri = obtenerDistri(nombreArchivo)

    f = Fitter(distri)
    f.fit()

    mejor = f.get_best()
    
    print("Distribución más ajustada:")
    for nombre, params in mejor.items():
        print(f"- {nombre}")
        print(f"  Parámetros: {params}")

    return mejor

detectar_distribucion("muestras/m4.txt")