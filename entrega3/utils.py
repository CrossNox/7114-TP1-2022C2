import math
import os
import random

import requests
from tqdm.notebook import tqdm as tqdm

def download_file(url, dest, override=False, chunksize=4096):
    if os.path.exists(dest) and not override:
        return
    with requests.get(url, stream=True) as r:
        try:
            file_size = int(r.headers["Content-Length"])
        except KeyError:
            file_size = 0

        with open(dest, "wb") as f, tqdm(
            total=file_size, unit="iB", unit_scale=True
        ) as t:
            for chunkdata in r.iter_content(chunksize):
                f.write(chunkdata)
                t.update(len(chunkdata))


def parsear_archivo(fname):
    with open(fname) as f:
        capacidad = int(f.readline().split(":")[1].strip())
        dimension = int(f.readline().split(":")[1].strip())
        try:
            line = f.readline()
            assert line.strip() == "DEMANDAS"
        except AssertionError:
            raise ValueError(f"Was expecting DEMANDAS but got {line}")
        demandas = {}
        line = f.readline().strip()
        while line != "FIN DEMANDAS":
            k, v = line.split()
            demandas[int(k)] = int(v)
            line = f.readline()
        tipo_arista = f.readline().split(":")[1].strip()
        f.readline()

        coords = {}
        for _ in range(dimension):
            i, x, y = f.readline().split()
            coords[int(i)] = {"x": float(x), "y": float(y)}

        assert f.readline().strip() == "EOF"

    return capacidad, dimension, demandas, tipo_arista, coords


def dist(a, b, coords):
    x0, y0 = coords[a]["x"], coords[a]["y"]
    x1, y1 = coords[b]["x"], coords[b]["y"]
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def calcular_distancias(l, coords):
    total = 0
    for actual, prox in zip(l, l[1:]):
        total += dist(actual, prox, coords)
    total += dist(l[-1], l[0], coords)
    return total


def cumple_capacidad(l, demandas, capacidad):
    capacidad_actual = 0
    for n in l:
        demanda = demandas[n]
        capacidad_actual += demanda
        if capacidad_actual < 0 or capacidad_actual > capacidad:
            return False
    return True


def random_path(p):
    l = list(p)
    random.shuffle(l)
    return l
