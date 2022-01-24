from grafics import draw_board, draw_target
from calculations import get_expected_value, get_score
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
import config as cfg
 

def main():

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom = 0.2)
    draw_board(ax)
    draw_target(ax, cfg.mu, cfg.sigma)

    ax.axis('square')
    ax.set_xlim(-cfg.radius_of_board - 10, cfg.radius_of_board + 10)
    ax.set_ylim(-cfg.radius_of_board - 10, cfg.radius_of_board + 10)

    # create slider 
    ax_var = plt.axes([0.25, 0.1, 0.65, 0.02])
    Varslider = Slider(ax_var, 'Standardabweichung', 1, 100, valinit = cfg.sigma, valstep = 1)

    # update, if slider is changed
    def update(val):
        cfg.sigma = Varslider.val
        draw_board(ax)
        draw_target(ax, cfg.mu, cfg.sigma)
        plt.show()


    # check if slider is changed
    Varslider.on_changed(update)

    # calculation button setup 
    btnpos = plt.axes([0.4, 0.025, 0.2, 0.05])
    calc_button = Button(btnpos, 'Erwartungswert')
    calc_button.on_clicked(get_expected_value)

    # set new target
    def onclick(event):
        if switch:
            ix, iy = event.xdata, event.ydata
            cfg.mu = [event.xdata, event.ydata]
            print('x = ',ix, ' y = ', iy)

            score = get_score(ix, iy)
            print('Geworfen: ',score)
            draw_board(ax)
            draw_target(ax, cfg.mu, cfg.sigma)
            plt.show()

    # update target, when mouse is clicked on board 
    fig.canvas.mpl_connect('button_press_event', onclick)


    # help functions to handle mouse position on the canvas 
    def join_board(event):
        global switch
        if event.inaxes == ax:
            switch = True


    def leave_board(event):
        global switch
        if event.inaxes == ax:
            switch = False


    fig.canvas.mpl_connect('axes_leave_event', leave_board)
    fig.canvas.mpl_connect('axes_enter_event', join_board)

    plt.show()


if __name__ == '__main__':
    main()