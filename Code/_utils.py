"""Utilidades compartidas de Visa-R."""
import numpy as np
import pandas as pd


def wls_cluster(y, x, w, cl):
    """Minimos cuadrados ponderados con errores agrupados (cluster). Devuelve (beta, ee, n)."""
    m = y.notna() & x.notna().all(axis=1) & w.notna()
    y, x, w, cl = y[m].to_numpy(float), x[m].to_numpy(float), w[m].to_numpy(float), cl[m].to_numpy()
    xtwx = (x * w[:, None]).T @ x
    inv = np.linalg.pinv(xtwx)
    beta = inv @ (x * w[:, None]).T @ y
    e = y - x @ beta
    S = x * (w * e)[:, None]
    g = pd.DataFrame(S).groupby(cl).sum().to_numpy()
    k, n = x.shape[1], len(y)
    G = g.shape[0]
    V = inv @ (g.T @ g) @ inv * (G / (G - 1)) * ((n - 1) / (n - k))
    return beta, np.sqrt(np.diag(V)), n
