import matplotlib.pyplot as plt
from grafics import draw_board, draw_target
import config as cfg
import json

def draw_image():

    fig, ax = plt.subplots()
    draw_board(ax)

    draw_target(ax, [0, 0], 50, "green")
    draw_target(ax, [0, 0], 29, "yellow")
    draw_target(ax, [0, 0], 16, "red")

    ax.axis('square')
    ax.set_xlim(-cfg.radius_of_board - 10, cfg.radius_of_board + 10)
    ax.set_ylim(-cfg.radius_of_board - 10, cfg.radius_of_board + 10)

    plt.show()

def draw_results():
    with open("file.json", "r") as f:
        r = json.load(f)

    # print(r[10][f"{20}"])
    fig, ax = plt.subplots()
    var_list = [i for i in range(1, 100)]    
    score_list = [7, 19, 20, "Bull"]
    for key in score_list:
        hist = []
        for var in range(len(r)):
            hist.append(r[var][f"{key}"])
        ax.plot(var_list, hist, label=key)
    
        ax.grid(True)
    ax.legend()
    ax.set_xlabel("standard deviation")
    ax.set_ylabel("expected score")

    # Zeichnen der Übergangsgrenzen
    ax.plot([16, 16], [0, 60], '--', color="gray")
    ax.text(15.5, -1.5, r'16')
    ax.plot([29, 29], [0, 60], '--', color="gray")
    ax.text(28.5, -1.5, r'29')
    ax.plot([50, 50], [0, 60], '--', color="gray")
    ax.text(49.5, -1.5, r'50')
    plt.show()

if __name__ == "__main__":
    # draw_image()
    draw_results()