import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons

class Board:

    numbers = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]

    # lenght of radien
    radius_of_board = 170
    bullseye = 6.35
    singlebull = 15.9
    triple_inner = 99
    triple_outer = 107
    dopple_inner = 162
    dopple_outer = radius_of_board

    radien = [0, bullseye, singlebull, triple_inner, triple_outer, dopple_inner, dopple_outer]
    radien_factor = [2, 1, 1, 3, 1, 2, 0]   # factor for each ring (3 --> triple field)

    def __init__(self, ev=[0, 0], sigma=10):
        self.ev = ev            # expected value 
        self.sigma = sigma      # std
        self.switch = False 

        # init board 
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom = 0.2)
        self.ax.axis('square')
        self.ax.set_xlim(-self.radius_of_board - 10, self.radius_of_board + 10)
        self.ax.set_ylim(-self.radius_of_board - 10, self.radius_of_board + 10)

        # init slider 
        ax_std = plt.axes([0.25, 0.1, 0.65, 0.02])
        self.std_slider = Slider(ax_std, 'Standardabweichung', 2, 100, valinit = self.sigma, valstep = 1)
        self.std_slider.on_changed(self.update_slider)

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('axes_leave_event', self.leave_board)
        self.fig.canvas.mpl_connect('axes_enter_event', self.join_board)

    def draw_board(self):
        Bg = mpatches.Rectangle(xy=(-self.radius_of_board-10,-self.radius_of_board-10), width=2*self.radius_of_board+20, height=2*self.radius_of_board+20, color = 'grey')
        self.ax.add_patch(Bg)
        for i in range(10):
            i *= 18
            Stripes = mpatches.Wedge(center = (0,0), r = self.dopple_outer, theta1 = 2*i-9,theta2 = 2*i+9, color = 'green' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.dopple_inner, theta1 = 2*i-9,theta2 = 2*i+9, color = 'wheat' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.triple_outer, theta1 = 2*i-9,theta2 = 2*i+9, color = 'green' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.triple_inner, theta1 = 2*i-9,theta2 = 2*i+9, color = 'wheat' )
            self.ax.add_patch(Stripes)

            Stripes = mpatches.Wedge(center = (0,0), r = self.dopple_outer, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'red' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.dopple_inner, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'black' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.triple_outer, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'red' )
            self.ax.add_patch(Stripes)
            Stripes = mpatches.Wedge(center = (0,0), r = self.triple_inner, theta1 = 2*(i)+9,theta2 = 2*i+27, color = 'black' )
            self.ax.add_patch(Stripes)

        Singlebull = mpatches.Circle(xy = (0,0), radius=self.singlebull, color = 'green')
        self.ax.add_patch(Singlebull)
        Bullseye = mpatches.Circle(xy = (0,0), radius=self.bullseye, color = 'red')
        self.ax.add_patch(Bullseye)

        # draw numbers 
        rad = (self.dopple_inner + self.triple_outer)/2
        for i in range(20):
            num = self.numbers[i]
            phi = i*2*np.pi/20
            xp = np.cos(phi)*rad
            yp = np.sin(phi)*rad
            self.ax.text(xp, yp, num, ha = 'center', va = 'center',color = 'gray', fontsize = 14)
        
    def update_screen(self):
        self.draw_board()
        self.draw_target()
        plt.show()
    
    def draw_target(self, col='yellow'):
        ziel = mpatches.Circle(xy = (self.ev[0],self.ev[1]), radius=2*self.sigma, color = col, alpha = 0.5)
        self.ax.add_patch(ziel)
        mitte = mpatches.Circle(xy = (self.ev[0],self.ev[1]), radius=2, color = 'blue', alpha = 0.8)
        self.ax.add_patch(mitte)

    def update_slider(self, val):
        self.sigma = self.std_slider.val
        # print(self.sigma)
        self.update_screen()
    
    def onclick(self, event):
        if self.switch:
            ix, iy = event.xdata, event.ydata
            self.ev = [event.xdata, event.ydata]
            print('x = ',ix, ' y = ', iy)

            # score = get_score(ix, iy)
            # print('Geworfen: ',score)
            self.update_screen()
            plt.show()

    def join_board(self, event):
        if event.inaxes == self.ax:
            self.switch = True
            print('joined')
    
    def leave_board(self, event):
        if event.inaxes == self.ax:
            self.switch = False
            print('left')

    def test(self):
        pass


if __name__ == "__main__":
    b = Board(ev=[0, 100])
    b.update_screen()
