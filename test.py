import numpy as np
from scipy.integrate import dblquad
'''
Was lernen wir daraus: 
    Die Funktion dblquad ist anscheinend berechnet anscheinend nicht das richtige Integral 
    --> erhalten Werte, die Absolut unrealistisch sind

    Vielleicht noch mal einen genaueren Blick in die Dokumentation werfen...
    Bin mir aber ziemlich sicher, dass es so funktionieren wird.

'''
mu = [1, 1]
sigma = 1

def prob_density_polar(r, phi):
    global mu, sigma 
    factor = r/(2*np.pi*sigma**2)
    ev = (np.cos(phi)*r - mu[0])**2 + (np.sin(phi)*r - mu[1])**2
    return factor*np.exp(-ev/(2*sigma**2))

def density(r, phi):
    global mu, sigma 
    factor = 1/(2*np.pi*sigma**2)
    ev = (np.cos(phi)*r - mu[0])**2 + (np.sin(phi)*r - mu[1])**2
    return factor*np.exp(-ev/(2*sigma**2))

def normal_density(x, y):
    factor = 1/(2*np.pi*sigma**2)
    ev = (x - mu[0])**2 + (y - mu[1])**2
    return factor*np.exp(-ev/(2*sigma**2))


# normal_integral = dblquad(lambda x, y: normal_density(x, y), -10, 10, -10, 10)
# polar_integral = dblquad(lambda r, phi: density(r, phi), 0, 10, 0, np.pi)
# polar_2_integral = dblquad(lambda r, phi: prob_density_polar(r, phi), 0, 10, 0, 2*np.pi)

def calc_integral_fast(f, a, b, c, d):
    # Machen hier ein Verfahren für mit additiver Integralberechnung
    x = np.linspace(a, b, 201)
    y = np.linspace(c, d, 201)
    vol = 0
    for i in range(len(x)-1):
        for k in range(len(y)-1):
            vol += integral(f, x[i], x[i+1], y[k], y[k+1]) 
    return vol

def integral(f, r1, r2, w1, w2):
    p1 = f(r1, w1)
    p2 = f(r2, w1)
    p3 = f(r1, w2)
    p4 = f(r2, w2)
    area = (r2 - r1)*(w2 - w1)
    return area*(p1 + p2 + p3 + p4)/4


def adaptiv_integral(f, x1, x2, y1, y2, e=1e-8): # ToDo: hier weitermachen
    '''
    VORSICHT: Haben die Intervallgrenzen annähernd den selben Wert, so kann es zu Abweichungen kommen  
    '''
    # global counter
    # adaptive Funktion for calculation an 2D integral
    # --> x2 > x1 and y2 > y1
    area = (x2 - x1)*(y2 - y1)
    trapez = trapez_rule(f, x1, x2, y1, y2)
    simpson = simpson_rule(f, x1, x2, y1, y2)
    err = np.abs(trapez - simpson)

    if err > e:                 # 
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


# --> hier nachher weitermachen --> adaptiver Verfahren implementieren 

def testfkt(x, y):
     return x**2 + y**2


def main():
    # print(fast_integral(normal_density, -10, 10, -10, 10))
    # print(calc_integral_fast(normal_density,-10, 10, -10, 10))
    print(adaptiv_integral(testfkt, -1, 1, -1, 1))
    print(adaptiv_integral(normal_density, -10, 10, -10, 10))
    print(adaptiv_integral(prob_density_polar, 0, 20, 0, 2*np.pi))

if __name__ == '__main__':
    main()