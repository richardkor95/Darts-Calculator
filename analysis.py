from webbrowser import get
import numpy as np
from calculations import get_expected_value
import config as cfg
from tqdm import tqdm 

# berechnen hier die Erwartungswerte der verschieden Ziele

# TODO: Translate polar to 
def translate_polar_to_kart(r, phi):
    x, y = r*np.cos(phi), r*np.sin(phi)
    return x, y

def print_dict(d):
    for i, val in d.items():
        print(f"{i} \t = {val} ")

def main():
    result = {}

    # Bullseye
    r = 0
    phi = 0
    cfg.sigma = 10
    cfg.mu = translate_polar_to_kart(r, phi)
    result["Bull"] = get_expected_value(None)

    r = (cfg.triple_inner + cfg.triple_outer)/2
    for i in tqdm(range(20)):
        phi = i*(18/360*2*np.pi)
        cfg.mu = translate_polar_to_kart(r, phi)
        result[cfg.numbers[i]] = get_expected_value(None) 

    print_dict(result)

    print(max(result, key=result.get))

    # x, y = translate_polar_to_kart(r, phi)
    # for i in range(2):
    #     cfg.mu = [0, i*((cfg.triple_inner+cfg.triple_outer) / 2)]
    #     get_expected_value(None)


if __name__ == "__main__":
    main()