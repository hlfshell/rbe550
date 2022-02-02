from math import sqrt
from typing import Tuple
from planner import Planner

def dijkstras_cost(position: Tuple[int, int], planner: Planner):
    parent = planner.parents[position]
    cost = planner.field.get_value(parent)
    if cost == "R":
        cost = 0
    return cost + 1

def greedy_cost(position: Tuple[int, int], planner: Planner):
    goal = planner.field.goal_position
    distance = sqrt(
            (goal[0] - position[0])**2 +
            (goal[1] - position[1])**2
        )
    if distance == 0:
        distance = 1*10^-10
    return distance

def astar_cost(position: Tuple[int, int], planner: Planner):
    parent = planner.parents[position]
    cost = planner.field.get_value(parent)
    if cost == 'R':
        cost = 0
    cost += 1
    goal = planner.field.goal_position
    distance = sqrt(
            (goal[0] - position[0])**2 +
            (goal[1] - position[1])**2
        )
    if distance == 0:
        distance = 1*10^-10
    return distance + cost