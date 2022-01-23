# Obstacle Field

As part of HW0, this code base creates an obstacle field - a two dimensional array map of 0's and 1's, where 1's denote occupied spaces and 0's denote open space. This is for future path planning assignments.

The generator is ran via `create-field.py`, which provides a rudimentary CLI.

Note to make the image larger, we increase the size of a singular cell in this map to 5 pixels by 5 pixels.

## Example:
`python create-field.py -w 128 -h 128 -o out.jpg -p 30`

...where

* `-w` - *required* - the width of the map in pixels
* `-h` - *required* - the height of the map in pixels
* `-o` - *required* - the output file to save the resulting image of the map to.
* `-p` - *required* - the percentage coverage for the map you wish to achieve. May not be possible depending on size of map and tetrominoe choice.
* `-g` - with a filename afterward, creates a gif of the map being populated. Note that this slows down creation of the map generation significantly.
* `-f` - Askew the boring tetris tetrominoes and utilize better video game art for the object map.
