import pandas
import numpy

def gen_data(size: int):
    columns = [ "Perdita di peso", "Diarrea", "Nausea", "Vomito", "Rigonfiamento", "Acidità di stomaco", "Dolore addominale", "Ciste", "Ulcera", "Malattia" ]
    dataset = pandas.DataFrame(columns=columns, dtype=int)

    malattia = []
    pdp = []
    diarrea = []
    nausea = []
    vomito = []
    rigonfiamento = []
    ads = []
    da = []
    ciste = []
    ulcera = []

    for i in range(0, size):
        m = random_binary(3)
        c = random_binary_mono(10, 500, m)
        n = random_binary_bin(250, 300, 500, 1000, m, c)
        u = random_binary_bin(5, 5, 300, 0, m, c)
        malattia.append(int(m))
        pdp.append(int(random_binary_mono(5, 600, m)))
        diarrea.append(int(random_binary_mono(300, 700, m)))
        nausea.append(int(n))
        vomito.append(int(random_binary_mono(150, 600, n)))
        rigonfiamento.append(int(random_binary_mono(100, 500, c)))
        ads.append(int(random_binary_mono(300, 1000, u)))
        da.append(int(random_binary_bin(200, 1000, 300, 1000, c, u)))
        ciste.append(int(c))
        ulcera.append(int(u))

    dataset["Perdita di peso"] = pdp
    dataset["Diarrea"] = diarrea
    dataset["Nausea"] = nausea
    dataset["Vomito"] = vomito
    dataset["Rigonfiamento"] = rigonfiamento
    dataset["Acidità di stomaco"] = ads
    dataset["Dolore addominale"] = da
    dataset["Ciste"] = ciste
    dataset["Ulcera"] = ulcera
    dataset["Malattia"] = malattia

    return dataset

def load_dataset(path: str) -> pandas.DataFrame:
    return pandas.read_csv(path)

def random_binary(chance: int) -> int:
    value = random_int()
    return value <= chance

def random_binary_mono(lchance: int, hchance: int, active: bool) -> int:
    value = random_int()
    if active:
        return value <= hchance
    else:
        return value <= lchance

def random_binary_bin(llchance: int, lhchance: int, hlchance: int, hhchance: int, act1: bool, act2: bool) -> int:
    value = random_int()
    if act1:
        if act2:
            return value <= hhchance
        else:
            return value <= hlchance
    elif act2:
        return value <= lhchance
    else:
        return value <= llchance


def random_int() -> int: return numpy.random.randint(0, 1000)