import config as cfg
import numpy as np
import matplotlib.pyplot as plt


def get_score(x, y):
    r = np.sqrt(x**2 + y**2)
    score = 0
    if r < cfg.radien[1]:       #   Bullseye
        score = 50
    elif r > cfg.radien[1] and r < cfg.radien[2]:   #   Singlebull
        score = 25
    elif r > cfg.radien[-1]:
        score = 0
    else:
        score = get_number(x, y)*get_factor(r)
    return score


def get_factor(r):
    for k in range(2, len(cfg.radien)):
        if r > cfg.radien[k] and r < cfg.radien[k+1]:
            factor = cfg.radien_factor[k]
            break
    return factor


def get_number(x, y):       
    phi = np.arctan(y/x)
    ang = 18/360*2*np.pi
    if x < 0:
        phi += np.pi 
    else:
        if y < 0:
            phi += 2*np.pi
    print(phi)
    for i in range(20):
        ang1 = ang*(i-1/2)
        ang2 = ang*(i+1/2)
        num = 6  # to define the first value 
        if phi > ang1 and phi < ang2:
            num = cfg.numbers[i]
            break
    return num
        

def prob_density_polar(r, phi):
    factor = r/(2*np.pi*cfg.sigma**2)
    ev = (np.cos(phi)*r - cfg.mu[0])**2 + (np.sin(phi)*r - cfg.mu[1])**2
    return factor*np.exp(-ev/(2*cfg.sigma**2))


def get_expected_value(event):
    e = 0

    # integrate bull and single bull
    for i in range(2):
        e += adaptiv_integral(prob_density_polar, cfg.radien[i], cfg.radien[i+1], 0, 2*np.pi)*25*cfg.radien_factor[i]

    for i in range(2, len(cfg.radien)-1):
        r1 = cfg.radien[i]
        r2 = cfg.radien[i+1]
        for k in range(20):
            phi1 = 18/360*2*np.pi * (k - 1/2) 
            phi2 = 18/360*2*np.pi * (k + 1/2) 
            e += adaptiv_integral(prob_density_polar, r1, r2, phi1, phi2)*cfg.numbers[k]*cfg.radien_factor[i]

    print(f'Erwartungswert = {e}') 
    

def adaptiv_integral(f, x1, x2, y1, y2, e=1e-5): 
    # global counter
    # adaptive Funktion for calculation an 2D integral
    # --> x2 > x1 and y2 > y1
    area = (x2 - x1)*(y2 - y1)
    trapez = trapez_rule(f, x1, x2, y1, y2)
    simpson = simpson_rule(f, x1, x2, y1, y2)
    err = np.abs(trapez - simpson)

    if err > e:                 # Abhängig von der größer des Feldes? 
        mx = (x2 + x1) / 2
        my = (y2 + y1) / 2

        integral = adaptiv_integral(f, x1, mx, y1, my) + adaptiv_integral(f, mx, x2, y1, my) + \
            adaptiv_integral(f, x1, mx, my, y2) + adaptiv_integral(f, mx, x2, my, y2)

    else:
        integral = simpson

    return integral


def trapez_rule(f, x1, x2, y1, y2):
    area = (x2 - x1)*(y2 - y1)

    return area*(f(x1, y1) + f(x1, y2) + f(x2, y1) + f(x2, y2))/4


def simpson_rule(f, x1, x2, y1, y2):
    x = np.linspace(x1, x2, 3)
    y = np.linspace(y1, y2, 3)
    hx = x[1] - x[0]
    hy = y[1] - y[0]
    singles = f(x[0], y[0]) + f(x[2], y[0]) + f(x[0], y[2]) + f(x[2], y[2])
    fours = f(x[1], y[0]) + f(x[2], y[1]) + f(x[1], y[2]) + f(x[0], y[1])

    return hx*hy*(singles + 4*fours + 16*f(x[1], y[1]))/9
