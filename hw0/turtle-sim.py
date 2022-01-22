from turtle import *
from time import sleep

def draw_star(sides: int):
    alpha = 180/sides

    color('green', 'purple')
    begin_fill()
    sleep(3)

    for i in range(0, sides):
        forward(200)
        right(180 - alpha)
    end_fill()
    done()

if __name__ == "__main__":
    draw_star(9)