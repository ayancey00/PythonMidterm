# Need a 2d grid, Grid[c,r] possiblely.  

# Each block we refer to as a cell. cell can either be one of zero. Alive or dead

# There will be 8 cells around any given cell(Neighbors). If cell is alive and if 2-3 neigbors are alive, it stays alive. anything else, dead.
# When cell is dead and there is exactly three alive neighbors, then it becomes alive.

# have it start randomly and watch it go or make it mannuel start.

# Need a pause feature

# we need to make it wrap around, when it reaches the left side it wraps over to the right side.

import random

#setup for the grid
rows, cols = 20, 20
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# This is so 25% of cells start alive
p_alive = 0.25 

#this sets up the board. Giving 25 percent of them life and leaving 75 percent dead.
for r in range(rows):
    for c in range(cols):
        grid[r][c] = 1 if random.random() < p_alive else 0


# This prints our grid with 1's and 0's
for row in grid:
        line = "".join("1" if cell else "." for cell in row)
        print(line)


# now we need the neighbors to be counted