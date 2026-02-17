# Need a 2d grid, Grid[c,r] possiblely.  

# Each block we refer to as a cell. cell can either be one of zero. Alive or dead

# There will be 8 cells around any given cell(Neighbors). If cell is alive and if 2-3 neigbors are alive, it stays alive. anything else, dead.
# When cell is dead and there is exactly three alive neighbors, then it becomes alive.

# have it start randomly and watch it go or make it mannuel start.

# Need a pause feature

# we need to make it wrap around, when it reaches the left side it wraps over to the right side.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
def count_neighbors(r, c):
    
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr = (r + dr) % rows
            cc = (c + dc) % cols
            total += grid[rr][cc]
    return total


def step():
    
    global grid
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            n = count_neighbors(r, c)
            if grid[r][c] == 1:
                new_grid[r][c] = 1 if (n == 2 or n == 3) else 0
            else:
                new_grid[r][c] = 1 if n == 3 else 0

    grid = new_grid



#matplotlib visualization 
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap="binary", interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])

def animate(frame):
    step()
    img.set_data(grid)
    return (img,)

ani = animation.FuncAnimation(fig, animate, interval=200, blit=True)
plt.show()