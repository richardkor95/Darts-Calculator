import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import config as cfg
from matplotlib.widgets import Slider, Button, RadioButtons


def draw_board(ax):
    Bg = mpatches.Rectangle(xy=(-cfg.radius_of_board-10,-cfg.radius_of_board-10), width=2*cfg.radius_of_board+20, height=2*cfg.radius_of_board+20, color = 'grey')
    ax.add_patch(Bg)
    for i in range(10):
        i *= 18
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.dopple_outer, theta1 = 2*i-9,theta2 = 2*i+9, color = 'green' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.dopple_inner, theta1 = 2*i-9,theta2 = 2*i+9, color = 'wheat' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.triple_outer, theta1 = 2*i-9,theta2 = 2*i+9, color = 'green' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.triple_inner, theta1 = 2*i-9,theta2 = 2*i+9, color = 'wheat' )
        ax.add_patch(Stripes)

        Stripes = mpatches.Wedge(center = (0,0), r = cfg.dopple_outer, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'red' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.dopple_inner, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'black' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.triple_outer, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'red' )
        ax.add_patch(Stripes)
        Stripes = mpatches.Wedge(center = (0,0), r = cfg.triple_inner, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'black' )
        ax.add_patch(Stripes)

    Singlebull = mpatches.Circle(xy = (0,0), radius=cfg.singlebull, color = 'green')
    ax.add_patch(Singlebull)
    Bullseye = mpatches.Circle(xy = (0,0), radius=cfg.bullseye, color = 'red')
    ax.add_patch(Bullseye)

    # draw numbers 
    rad = (cfg.dopple_inner + cfg.triple_outer)/2
    for i in range(20):
        num = cfg.numbers[i]
        phi = i*2*np.pi/20
        xp = np.cos(phi)*rad
        yp = np.sin(phi)*rad
        ax.text(xp, yp, num, ha = 'center', va = 'center',color = 'gray', fontsize = 14)


def draw_target(ax, mu, sigma):
    ziel = mpatches.Circle(xy = (mu[0],mu[1]), radius=2*sigma, color = 'yellow', alpha = 0.5)
    ax.add_patch(ziel)
    mitte = mpatches.Circle(xy = (mu[0],mu[1]), radius=2, color = 'blue', alpha = 0.8)
    ax.add_patch(mitte)



