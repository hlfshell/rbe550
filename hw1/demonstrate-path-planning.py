from math import sqrt
from field import Field
from planner import Planner
from queues import BFSQueue, DFSQueue, Dijkstras
from math import floor

from random import randint

def save_gif(images, path, ending_frame=25):
    for i in range(0, ending_frame):
        images.append(images[-1])
    images[0].save(path, save_all=True, append_images=images[1:], duration=100, loop=0)

width = 25
height = 25

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
_, images = planner.search(gif=True)
save_gif(images, "bfs.gif")

im = field.draw()
im.save("bfs.jpg")

field.reset()

print("DFS")
dfs = DFSQueue()
planner = Planner(field, dfs)
_, images = planner.search(gif=True)
save_gif(images, "dfs.gif")

im = field.draw()
im.save("dfs.jpg")

field.reset()

print("DIJKSTRAS")
dijkstras = Dijkstras()
def dijkstras_cost(position, parent, field):
    parent_value = field.get_value(parent)
    if parent_value == "R":
        parent_value = 0
    return parent_value + 1
planner = Planner(field, dijkstras, cost_func=dijkstras_cost)
_, images = planner.search(gif=True)
save_gif(images, "dijkstras.gif")

im = field.draw()
im.save("dijkstras.jpg")

field.reset()

print("ASTAR")
dijkstras = Dijkstras()
def astar_cost(position, parent, field : Field):
    goal = field.goal_position
    distance = sqrt(
            (goal[0] - position[0])**2 +
            (goal[1] - position[1])**2
        )
    if distance == 0:
        distance = 1*10^-10
    return distance
planner = Planner(field, dijkstras, cost_func=astar_cost)
_, images = planner.search(gif=True)
save_gif(images, "astar.gif")

im = field.draw()
im.save("astar.jpg")