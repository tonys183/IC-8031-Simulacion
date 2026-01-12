import numpy as np
from scipy import stats

# =======================
# Leer muestra desde archivo
# =======================

def read_sample(filename):
    with open(filename, "r") as f:
        return np.array([float(x.strip()) for x in f if x.strip()])

def subsample(data, n_sub, seed=42):
    rng = np.random.default_rng(seed)
    return rng.choice(data, size=n_sub, replace=False)

# =======================
# KS sobre varias distribuciones
# =======================

def ks_comparison(data):
    data = np.asarray(data)
    results = []

    # -----------------------
    # Normal
    # -----------------------
    mu, sigma = stats.norm.fit(data)
    D, p = stats.kstest(data, "norm", args=(mu, sigma))
    results.append(("normal", D, p, (mu, sigma)))

    # -----------------------
    # Weibull
    # -----------------------
    c, loc, scale = stats.weibull_min.fit(data)
    D, p = stats.kstest(data, "weibull_min", args=(c, loc, scale))
    results.append(("weibull", D, p, (c, loc, scale)))

    # -----------------------
    # Poisson
    # -----------------------
    lam = np.mean(data)
    D, p = stats.kstest(data, stats.poisson.cdf, args=(lam,))
    results.append(("poisson", D, p, (lam,)))

    # -----------------------
    # Binomial Negativa (método de momentos)
    # -----------------------
    mean = np.mean(data)
    var = np.var(data, ddof=1)

    if var > mean:  # condición necesaria
        p_nb = mean / var
        r_nb = mean**2 / (var - mean)

        D, p = stats.kstest(data, stats.nbinom.cdf, args=(r_nb, p_nb))
        results.append(("negative_binomial", D, p, (r_nb, p_nb)))
    else:
        results.append(("negative_binomial", np.inf, 0.0, None))

    results.sort(key=lambda x: x[1])
    return results

# =======================
# USO
# =======================

data_full = read_sample("muestras/m4.txt")

data_sub = subsample(data_full, n_sub=50)

results = ks_comparison(data_sub)

print(f"Tamaño original: {len(data_full)}")
print(f"Tamaño reducido: {len(data_sub)}\n")

for name, D, p, params in results:
    print(f"{name:18s}  D = {D:.5f}   p = {p:.5f}")
