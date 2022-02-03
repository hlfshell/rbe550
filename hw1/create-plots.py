from math import floor
from random import randint, random
from field import Field
from os import makedirs, path
from planner import Planner
from queues import BFSQueue, DFSQueue, Dijkstras, Random
from cost_functions import dijkstras_cost, greedy_cost, astar_cost
from matplotlib import pyplot as plt 

width = 128
height = 128
iterations_per = 500
max_percentage = 75
percentage_range = range(0, max_percentage+5, 5)

if not path.exists("./plots"):
    makedirs("./plots")

def bfs_planner(field: Field):
    bfs = BFSQueue()
    return Planner(field, bfs)

def dfs_planner(field: Field):
    dfs = DFSQueue()
    return Planner(field, dfs)

def dijkstra_planner(field: Field):
    queue = Dijkstras()
    return Planner(field, queue, cost_fnc=dijkstras_cost)

def greedy_planner(field: Field):
    queue = Dijkstras()
    return Planner(field, queue, cost_fnc=greedy_cost)

def astar_planner(field: Field):
    queue = Dijkstras()
    return Planner(field, queue, cost_fnc=astar_cost)

def random_planner(field: Field):
    queue = Random()
    return Planner(field, queue)

planners = {
        bfs_planner: "BFS",
        dfs_planner: "DFS",
        dijkstra_planner: "Dijkstra",
        greedy_planner: "Greedy",
        astar_planner: "A*",
        random_planner: "Random"
    }

# Initialize results storage
steps_taken = {}
path_length = {}
for planner_func in planners:
    planner = planners[planner_func]
    steps_taken[planner] = {}
    path_length[planner] = {}
    for percent in percentage_range:
        steps_taken[planner][percent] = []
        path_length[planner][percent] = []

# Now we move through each chosen percentage fill range
for fill_percentage in percentage_range:
    print(f"Fill percentage {fill_percentage}")
    field_count = 0
    # For each field percentage, we do several run throughts
    while field_count < iterations_per:
        try:
            field = Field(width, height)
            field.fill_field_to_percent(fill_percentage/100)

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

            # Fow each planner has its go on the field
            for planner_fnc in planners:
                field.reset()
                planner = planner_fnc(field)
                path, _ = planner.search()
                steps_taken[planners[planner_fnc]][fill_percentage].append(planner.steps_taken)
                path_length[planners[planner_fnc]][fill_percentage].append(len(path))
                
            field_count += 1
        except Exception as e:
            # We have this in a while loop and a try
            # because some maps are inherently not solvable,
            # which in turns throws an exception - we
            # thus ignore them and retry until we get
            # a map that is solvable.
            continue

# Steps taken figure
plt.figure("iterations_all")
plt.title("Iterations to Solution by Obstacle Percentage") 
plt.xlabel("Percentage of Obstacles") 
plt.ylabel("Steps Taken")
plt.figure("paths_all")
plt.title("Path Length By Obstacle Percentage")
plt.xlabel("Percentage of Obstacles")
plt.ylabel("Path Length")
plt.figure("paths_sans_dfs")
plt.title("Path Length By Obstacle Percentage")
plt.xlabel("Percentage of Obstacles")
plt.ylabel("Path Length")

for planner in steps_taken:
    plt.figure(f"iterations_{planner}")
    plt.title(f"Iterations to Solution for {planner}")
    plt.figure(f"paths_{planner}")
    plt.xlabel("Percentage of Obstacles") 
    plt.ylabel("Steps Taken")

    plt.figure(f"paths_{planner}")
    plt.title(f"Path Lengths for {planner}")
    plt.xlabel("Percentage of Obstacles")
    plt.ylabel("Path Length")

for planner in steps_taken:
    percentages = []
    steps = []
    lengths = []
    for percentage in steps_taken[planner]:
        steps_data = steps_taken[planner][percentage]
        count = len(steps_data)
        steps_average = sum(steps_data) / count
        percentages.append(percentage)
        steps.append(steps_average)
        
        paths_data = path_length[planner][percentage]
        count = len(paths_data)
        path_average = sum(paths_data) / count
        lengths.append(path_average)
    plt.figure(f"iterations_{planner}")
    plt.plot(percentages, steps, label=planner)
    plt.savefig(f"plots/{planner}_iterations.jpg")

    plt.figure(f"paths_{planner}")
    plt.plot(percentages, lengths, label=planner)
    plt.savefig(f"plots/{planner}_paths.jpg")

    if planner != planners[random_planner]:
        plt.figure("iterations_all")
        plt.plot(percentages, steps, label=planner)
        plt.figure("paths_all")
        plt.plot(percentages, lengths, label=planner)
    if planner != planners[dfs_planner] and planner != planners[random_planner]:
        plt.figure("paths_sans_dfs")
        plt.plot(percentages, lengths, label=planner)

plt.figure("iterations_all")
plt.legend(loc="upper right")
plt.savefig("plots/steps_taken.jpg")
plt.figure("paths_all")
plt.legend(loc="upper right")
plt.savefig("plots/path_length.jpg")
plt.figure("paths_sans_dfs")
plt.legend(loc="upper right")
plt.savefig("plots/path_length_sans_dfs.jpg")
