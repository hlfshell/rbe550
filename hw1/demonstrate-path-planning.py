import sys
from getopt import getopt
from math import floor
from random import randint

from field import Field
from planner import Planner
from queues import BFSQueue, DFSQueue, Dijkstras
from cost_functions import dijkstras_cost, greedy_cost, astar_cost

try:
    opts, args = getopt(sys.argv[1:], "g:w::h::p:")
except Exception as e:
    print("python demonstrate-path-planning.py -w 128 -h 128 -p 30")
    print("Optional:")
    print("\t-g\t:\tcreate a gif of each version - warning: SLOW")
    sys.exit(2)

width = 0
height = 0
percentage = 0
gif = False

for opt, arg in opts:
    if opt == "-w":
        width = int(arg)
    elif opt == "-h":
        height = int(arg)
    elif opt == "-g":
        gif = True
    elif opt == "-p":
        percentage = int(arg)/100

def save_gif(images, path, ending_frame=25):
    for i in range(0, ending_frame):
        images.append(images[-1])
    images[0].save(path, save_all=True, append_images=images[1:], duration=10, loop=0)

field = Field(width, height)
field.fill_field_to_percent(0.3)

# Select a goal position
while True:
    goal_position = (randint(floor(3*width/4), width-1), randint(floor(3*height/4), height-1))
    if not field.is_occupied(goal_position):
        break
field.place_goal(goal_position)

# Select a robot position
while True:
    robot_position = (randint(0, floor(width/4)), randint(0, floor(height/4)))
    if not field.is_occupied(robot_position):
        break
field.place_robot(robot_position)

print("BFS")
bfs = BFSQueue()
planner = Planner(field, bfs)
_, images = planner.search(gif=gif)
if gif:
    save_gif(images, "bfs.gif")
im = field.draw()
im.save("bfs.jpg")

field.reset()

print("DFS")
dfs = DFSQueue()
planner = Planner(field, dfs)
_, images = planner.search(gif=gif)
if gif:
    save_gif(images, "dfs.gif")
im = field.draw()
im.save("dfs.jpg")

field.reset()

print("DIJKSTRAS")
dijkstras = Dijkstras()
planner = Planner(field, dijkstras, cost_fnc=dijkstras_cost)
path, images = planner.search(gif=gif)
if gif:
    save_gif(images, "dijkstras.gif")

im = field.draw()
im.save("dijkstras.jpg")

field.reset()
print("GREEDY")
dijkstras = Dijkstras()
planner = Planner(field, dijkstras, cost_fnc=greedy_cost)
path, images = planner.search(gif=gif)
if gif:
    save_gif(images, "greedy.gif")
im = field.draw()
im.save("greedy.jpg")

field.reset()

print("ASTAR")
dijkstras = Dijkstras()
planner = Planner(field, dijkstras, cost_fnc=astar_cost)
path, images = planner.search(gif=gif)
if gif:
    save_gif(images, "astar.gif")
im = field.draw()
im.save("astar.jpg")