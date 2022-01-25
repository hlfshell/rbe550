from field import Field
from planner import Planner
from queue import BFSQueue, DFSQueue

from random import randint

width = 128
height = 128

field = Field(width, height)
field.fill_field_to_percent(0.7)

# Select a goal position
while True:
    goal_position = (randint(0, width), randint(0, height))
    if not field.is_occupied(goal_position):
        break
field.place_goal(goal_position)

# Select a robot position
while True:
    robot_position = (randint(0, width), randint(0, height))
    if not field.is_occupied(robot_position):
        break
field.place_robot(robot_position)

bfs = BFSQueue()
planner = Planner(field, bfs)
planner.search()

im = field.draw()
im.save("bfs.jpg")

field.reset()
field.place_goal(goal_position)
field.place_robot(robot_position)

dfs = DFSQueue()
planner = Planner(field, dfs)
planner.search()

im = field.draw()
im.save("dfs.jpg")