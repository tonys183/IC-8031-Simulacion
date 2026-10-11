import numpy as np

def funNormalDisc(mu, sigma, minVal):
    val = np.random.normal(loc=mu, scale=sigma)
    return int(val) if val >= minVal else 0

n = 100000
cajas = np.random.exponential(scale=2.5, size=n)
refrescos = np.random.exponential(scale=0.75, size=n)
llegadas = np.random.exponential(scale=3.0, size=n)
postres = np.random.binomial(n=5, p=0.6, size=n)
ordenes = np.random.binomial(n=5, p=0.4, size=n)
pollo = np.random.geometric(p=0.1, size=n)
freidora = np.array([funNormalDisc(mu=3, sigma=1, minVal=1) for _ in range(n)])

np.savetxt('muestras/cajas.txt', cajas, fmt='%.16f')
np.savetxt('muestras/refrescos.txt', refrescos, fmt='%.16f')
np.savetxt('muestras/freidora.txt', freidora, fmt='%d')
np.savetxt('muestras/postres.txt', postres, fmt='%d')
np.savetxt('muestras/pollo.txt', pollo, fmt='%d')
np.savetxt('muestras/ordenes.txt', ordenes, fmt='%d')
np.savetxt('muestras/llegadas.txt', llegadas, fmt='%.16f')