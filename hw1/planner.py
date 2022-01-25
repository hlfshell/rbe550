from typing import Dict, List, Optional, Tuple
from field import Field
from queue import Queue


class Planner():

    def __init__(self, field: Field, queue: Queue):
        self.field = field
        self.queue = queue
        self.parents: Dict[Tuple[int, int], Tuple[int, int]] = {}

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

        # Mark that node as currently visited, unless it's the robot
        # cell (for drawing purposes we don't mark it)
        if current_value != 'R':
            self.field.set_value(current, 'V')

        # Get each neighbor and queue them. Ignore obstacles and
        # visited cells to prevent backtracking. For each of these
        # nodes, mark the current node as the parent.
        neighbors = self.field.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in self.parents:
                self.parents[neighbor] = current
                self.queue.push(neighbor)

    def search(self) -> Optional[List[Tuple[int, int]]]:
        path = None
        self.queue.push(self.field.robot_position)
        while path == None:
            path = self.step()

        return path