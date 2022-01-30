from typing import Callable, Dict, List, Optional, Tuple
from field import Field
from queue import Queue


class Planner():

    def __init__(self, field: Field, queue: Queue, cost_fnc: Optional[Callable] = None):
        self.field = field
        self.queue = queue
        self.parents: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.cost_fnc = cost_fnc

    def step(self) -> Optional[List[Tuple[int, int]]]:
        # If the queue is empty, there is no path :-(
        if len(self.queue) == 0:
            raise Exception("No path to the goal exists")

        # Get the next candidate for our current position in planning
        current = self.queue.pop()

        current_value = self.field.get_value(current)

        # Is this the goal? If so, hooray! Let's generate a path!
        if current_value == 'G':
            path = [current]
            while True:
                # If the cell is not the goal or robot, paint the path
                if current_value != 'G' and current_value != 'R':
                    self.field.set_value(current, 'P')

                # Set the "current" to the parent cell
                current = self.parents[current]
                current_value = self.field.get_value(current)
                path.append(current)

                # If we've reached the robot, we did it! We have our path!
                if current_value == 'R':
                    return path

        # # Mark that node as currently visited, unless it's the robot
        # # cell (for drawing purposes we don't mark it)
        if current_value == 'R':
            current_value = 0
        else:
            # get the parent's value
            parent_value = self.field.get_value(self.parents[current])
            if parent_value == "R":
                parent_value = 0
            current_value = parent_value + 1
            self.field.set_value(current, current_value)

        # Get each neighbor and queue them. Ignore obstacles and
        # visited cells to prevent backtracking. For each of these
        # nodes, mark the current node as the parent.
        neighbors = self.field.get_neighbors(current)
        for neighbor in neighbors:
            # If we've seen this neighbor before, see
            # if we have reached this neighbor with a shorter
            # cost / path than before. This is only applicable
            # if we have a cost function though.
            if neighbor in self.parents and self.cost_fnc is not None:
                parent_value = self.field.get_value(self.parents[neighbor])

                if parent_value == "R":
                    parent_value = 0
                if current_value < parent_value:
                    self.parents[neighbor] = current
            # Otherwise, just add it to the parents list
            elif neighbor not in self.parents:
                self.parents[neighbor] = current
                # If we've never seen it before, add it to the 
                # queue
                if self.cost_fnc is None:
                    self.queue.push(neighbor)
                else:
                    cost = self.cost_fnc(neighbor, self)
                    self.queue.push(neighbor, cost)

    def search(self, gif=False):
        path = None
        self.queue.push(self.field.robot_position)
        if gif:
            images = [self.field.draw()]
        else:
            images = None

        while path == None:
            path = self.step()
            if gif:
                images.append(self.field.draw())

        return path, images