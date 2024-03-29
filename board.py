import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
from matplotlib.widgets import Slider, Button, RadioButtons
from maths import adaptiv_integral

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

    def __init__(self, target=[0, 0], sigma=10):
        self.target = target                    # expected value 
        self.sigma = sigma              # std
        self.r = np.linalg.norm(target)     # distance to the center 

    def get_score(self):
        return self.get_number()*self.get_factor()
    
    def get_factor(self):
        for k in range(len(self.radien) - 1):
            if self.r > self.radien[k] and self.r < self.radien[k+1]:
                factor = self.radien_factor[k]
                break
        return factor

    def get_number(self):
        x, y = self.target
        if self.r <= self.radien[2]:
            num = 25
        elif self.r > self.radien[-1]:
            num = 0
        else:
            try:
                phi = np.arctan(y/x)
            except ZeroDivisionError:
                phi = np.sign(y)*np.pi/2
            ang = 18/360*2*np.pi
            if x < 0:
                phi += np.pi 
            else:
                if y < 0:
                    phi += 2*np.pi
            for i in range(20):
                ang1 = ang*(i-1/2)
                ang2 = ang*(i+1/2)
                num = 6  # to define the first value 
                if phi > ang1 and phi < ang2:
                    num = self.numbers[i]
                    break
        return num

    def get_ev(self, event=None):
        e = 0
        # integrate bull and single bull
        for i in range(2):
                e += adaptiv_integral(self.prob_density_polar, self.radien[i], self.radien[i+1], 0, 2*np.pi)*25*self.radien_factor[i]

        # integrate the rest
        for i in range(2, len(self.radien)-1):
            r1 = self.radien[i]
            r2 = self.radien[i+1]
            for k in range(20):
                phi1 = 18/360*2*np.pi * (k - 1/2) 
                phi2 = 18/360*2*np.pi * (k + 1/2) 
                e += adaptiv_integral(self.prob_density_polar, r1, r2, phi1, phi2)*self.numbers[k]*self.radien_factor[i]

        if e < self.get_score()/self.sigma and np.linalg.norm(self.target) < self.radius_of_board:
            warnings.warn("Calculation failed! \n Sigma to small for Adaptive Integration")
        if event == None:
            return e
        else:
            print(f'Erwartungswert = {e}') 

    # vielleicht noch überarbeiten 
    def prob_density_polar(self, r, phi):
        factor = r/(2*np.pi*self.sigma**2)
        ev = (np.cos(phi)*r - self.target[0])**2 + (np.sin(phi)*r - self.target[1])**2
        return factor*np.exp(-ev/(2*self.sigma**2))


class GuiBoard:

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

    def __init__(self, target=[0, 0], sigma=10):
        self.target = target                    # expected value 
        self.sigma = sigma              # std
        self.r = np.linalg.norm(target)     # distance to the center 
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

        # init button 
        btnpos = plt.axes([0.25, 0.025, 0.65, 0.05])
        self.button = Button(btnpos, 'Calculate expected value')
        self.button.on_clicked(self.get_ev)

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
        ziel = mpatches.Circle(xy = (self.target[0],self.target[1]), radius=2*self.sigma, color = col, alpha = 0.5)
        self.ax.add_patch(ziel)
        mitte = mpatches.Circle(xy = (self.target[0],self.target[1]), radius=2, color = 'blue', alpha = 0.8)
        self.ax.add_patch(mitte)

    def update_slider(self, val):
        self.sigma = self.std_slider.val
        # print(self.sigma)
        self.update_screen()
    
    def onclick(self, event):
        if self.switch:
            ix, iy = event.xdata, event.ydata
            self.target = [event.xdata, event.ydata]
            self.r = np.linalg.norm(self.target)
            print('x = ',ix, ' y = ', iy)

            self.update_screen()
            print(self.get_score())
            plt.show()

    def join_board(self, event):
        if event.inaxes == self.ax:
            self.switch = True
    
    def leave_board(self, event):
        if event.inaxes == self.ax:
            self.switch = False

    def get_score(self):
        return self.get_number()*self.get_factor()
    
    def get_factor(self):
        for k in range(len(self.radien) - 1):
            if self.r > self.radien[k] and self.r < self.radien[k+1]:
                factor = self.radien_factor[k]
                break
        return factor

    def get_number(self):
        x, y = self.target
        if self.r <= self.radien[2]:
            num = 25
        elif self.r > self.radien[-1]:
            num = 0
        else:
            try:
                phi = np.arctan(y/x)
            except ZeroDivisionError:
                phi = np.sign(y)*np.pi/2
            ang = 18/360*2*np.pi
            if x < 0:
                phi += np.pi 
            else:
                if y < 0:
                    phi += 2*np.pi
            for i in range(20):
                ang1 = ang*(i-1/2)
                ang2 = ang*(i+1/2)
                num = 6  # to define the first value 
                if phi > ang1 and phi < ang2:
                    num = self.numbers[i]
                    break
        return num

    def get_ev(self, event=None):
        e = 0
        # integrate bull and single bull
        for i in range(2):
                e += adaptiv_integral(self.prob_density_polar, self.radien[i], self.radien[i+1], 0, 2*np.pi)*25*self.radien_factor[i]

        # integrate the rest
        for i in range(2, len(self.radien)-1):
            r1 = self.radien[i]
            r2 = self.radien[i+1]
            for k in range(20):
                phi1 = 18/360*2*np.pi * (k - 1/2) 
                phi2 = 18/360*2*np.pi * (k + 1/2) 
                e += adaptiv_integral(self.prob_density_polar, r1, r2, phi1, phi2)*self.numbers[k]*self.radien_factor[i]

        if e < self.get_score()/self.sigma and np.linalg.norm(self.target) < self.radius_of_board:
            warnings.warn("Calculation failed! \n Sigma to small for Adaptive Integration")
        if event == None:
            return e
        else:
            print(f'Erwartungswert = {e}') 

    # vielleicht noch überarbeiten 
    def prob_density_polar(self, r, phi):
        factor = r/(2*np.pi*self.sigma**2)
        ev = (np.cos(phi)*r - self.target[0])**2 + (np.sin(phi)*r - self.target[1])**2
        return factor*np.exp(-ev/(2*self.sigma**2))


if __name__ == "__main__":
    # b = Board(target=[0, 100])
    b = GuiBoard(target=[0, 100])
    b.update_screen()

