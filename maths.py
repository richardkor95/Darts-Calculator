import numpy as np


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
