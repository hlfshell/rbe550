import inspect
from os import listdir, path
from random import choice, randint
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw

tetrominoe_folder = "tetrominoes"


class Tetrominoe:

    def __init__(self, shape):
        self.shape = shape

    @staticmethod
    def load(path: str):
        # Read the tetrominoe file
        f = open(path, "r")
        data = f.read()
        f.close()

        # Convert the 0's and 1's to an array mapping
        tetrominoe = []
        line = []
        for char in data:
            if char == "0":
                line.append("O")
            elif char == "1":
                line.append("X")
            elif char == "\n":
                tetrominoe.append(line)
                line = []
            else:
                raise Exception("illegal character")
        tetrominoe.append(line)

        return Tetrominoe(tetrominoe)

    def rotate(self, rotation: int):
        '''
        This rotates the tetrominoe. Since we are working in a grid, we only
        perform 90 degree rotations.
        '''
        if rotation == 0:
            return

        if rotation % 90 != 0:
            raise Exception("Illegal rotation amount - must be a multiple of 90")

        rotated_shape = self.shape
        while rotation != 0:
            rotated_shape = np.rot90(rotated_shape, -1)
            rotation -= 90
        self.shape = list(rotated_shape)

    def print(self):
        for row in self.shape:
            for column in row:
                 print(column, end=' ')
            print()

    def get_dimensions(self):
        return (len(self.shape[0]), len(self.shape))

    def clone(self):
        return Tetrominoe(self.shape)

    @staticmethod
    def load_tetrominoes(folder_path: str) -> List['Tetrominoe']:
        files = listdir(folder_path) # Load all files
        files = filter(lambda x: x.endswith(".tet"), files) # pay attention to .tet files only

        tetrominoes = []
        for file in files:
            tetrominoe = Tetrominoe.load(path.join(folder_path, file))
            tetrominoes.append(tetrominoe)

        return tetrominoes


class Field:

    def __init__(self, width: int, height: int, tetrominoes: Optional[List[Tetrominoe]] = None):
        self.field = []
        for _ in range(0, height):
            row = []
            for _ in range(0, width):
                row.append("O")
            self.field.append(row)

        if tetrominoes is None:
            tetrominoes = Tetrominoe.load_tetrominoes(tetrominoe_folder)
        self.tetrominoes = tetrominoes

        self.obstacle_fields = 0

        self.robot_position = None
        self.goal_position = None
        self.path = None

    def print(self):
        for row in self.field:
            for column in row:
                 print(column, end=' ')
            print()

    def draw(self, cell_size=5) -> Image:
        rows = len(self.field[0])
        columns = len(self.field)
        width =  rows * cell_size
        height = columns * cell_size
        
        im = Image.new(mode="RGB", size=(width, height))
        draw = ImageDraw.Draw(im)

        for row in range(0, rows):
            for column in range(0, columns):
                upper_left = (row * cell_size, column * cell_size)
                bottom_right = (upper_left[0] + cell_size, upper_left[1] + cell_size)
                color = "white"
                value = self.get_value((row, column))
                if value == "X":
                    color = "black"
                elif value == "R":
                    color = "red"
                elif value == "G":
                    color = "green"
                elif type(value) == int:
                    color = "lightblue"
                elif value == "P":
                    color = "blue"
                draw.rectangle([upper_left, bottom_right], fill = color)

        return im

    def is_occupied(self, position: Tuple[int, int]) -> bool:
        if position[0] >= len(self.field[0]) \
                or position[1] >= len(self.field):
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)

        return self.field[position[1]][position[0]] not in ["O", "R", "G"]

    def coverage_percentage(self) -> float:
        return self.obstacle_fields / (len(self.field)*len(self.field[0]))

    def place_tetrominoe(self, tetrominoe: Tetrominoe, x, y, allow_overhang=False):
        width, height = tetrominoe.get_dimensions()
        obstacle_fields = 0
        
        # First we check to see if the tetrominoe will fit
        # within the boundaries of our field, but only if
        # overhang is not allowed
        if not allow_overhang and (x + width >= len(self.field[0]) or y + height >= len(self.field)):
            raise Exception("Can not place tetrominoe - would be out of bounds")

        # Then we check to see if there are any spots within the given space that
        # is already occupied.
        for row in range(y, y + height):
            tetrominoe_row = row - y
            for column in range(x, x + width):
                tetrominoe_column = column - x
                # Is it a 1 in the tetrominoe?
                if tetrominoe.shape[tetrominoe_row][tetrominoe_row]:
                    # If we allow overhangs and this does overhang, continue
                    if allow_overhang and (column >= len(self.field[0]) or \
                        row >= len(self.field)):
                        continue
                    # then check if it's 1 in the field
                    if self.is_occupied((row, column)):
                        raise Exception("Can not place tetrominoe - space occupied")
                    obstacle_fields += 1
                        

        # We can place the tetrominoe now!
        for row in range(y, y + height):
            tetrominoe_row = row - y
            for column in range(x, x + width):
                tetrominoe_column = column - x
                if tetrominoe.shape[tetrominoe_row][tetrominoe_column]:
                    if row > len(self.field) or column > len(self.field[0]):
                        continue

                    self.field[row][column] = "X"

        # increment the number of fields that are covered
        self.obstacle_fields += obstacle_fields

    def place_random_tetrominoe(self, attempts=1000, allow_overhang=True):
        while attempts > 0:
            try:
                x = randint(0, len(self.field[0]) - 1)
                y = randint(0, len(self.field) - 1)
                rotation = choice([0, 90, 180, 270])
                tetrominoe = choice(self.tetrominoes)
                tetrominoe.rotate(rotation)

                self.place_tetrominoe(tetrominoe, x, y, allow_overhang=allow_overhang)
                return
            except:
                # If we have attempts leftover, ignore the exception
                attempts -= 1
                if attempts <= 0:
                    raise Exception("Could not place random tetronimoe - field might be full")

    def fill_field_to_percent(self, target_percentage):
        try:
            while self.coverage_percentage() < target_percentage:
                self.place_random_tetrominoe()
        except:
            # Ignore exception for now, as we expect it might happen when
            # placing obstacles and our field is overflooded
            return

    def place_robot(self, position: Tuple[int, int]):
        if self.is_occupied(position):
            raise Exception("Can not set robot to an occupied space")

        if self.robot_position is not None:
            self.set_value(self.robot_position, "O")

        self.set_value(position, 'R')
        self.robot_position = position

    def place_goal(self, position: Tuple[int, int]):
        if self.is_occupied(position):
            raise Exception("Can not set goal to an occupied space")

        if self.goal_position is not None:
            self.set_value(self.goal_position, "O")

        self.set_value(position, 'G')
        self.goal_position = position

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        # rm, cm (row move, column move) - if you can, move in that direction
        # If, however, we are near a border, ignore that neighbor
        for rm in [-1, 1]:
            row_current = position[1] + rm # row current
            if row_current < 0 or row_current >= len(self.field):
                continue
            
            if not self.is_occupied((position[0], row_current)):
                neighbors.append((position[0], row_current))

        for cm in [-1, 1]:
            column_current = position[0] + cm # column current
            if column_current < 0 or column_current >= len(self.field[0]):
                continue

            if not self.is_occupied((column_current, position[1])):
                neighbors.append((column_current, position[1]))

        return neighbors


    def get_value(self, position: Tuple[int, int]) -> Union[int, str]:
        return self.field[position[1]][position[0]]

    def set_value(self, position: Tuple[int, int], value: Union[int, str]):
        self.field[position[1]][position[0]] = value

    def reset(self):
        for row, columns in enumerate(self.field):
            for column, value in enumerate(columns):
                if value not in ["X", "O"]:
                    self.field[row][column] = "O"
            
            self.place_goal(self.goal_position)
            self.place_robot(self.robot_position)