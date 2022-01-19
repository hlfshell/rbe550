from turtle import *
from time import sleep

L = 9
alpha = 180/L

color('green', 'purple')
begin_fill()

for i in range(0, L):
    forward(200)
    right(180 - alpha)
end_fill()
done()
