# Need a 2d grid, Grid[c,r] possiblely.  

# Each block we refer to as a cell. cell can either be one of zero. Alive or dead

# There will be 8 cells around any given cell(Neighbors). If cell is alive and if 2-3 neigbors are alive, it stays alive. anything else, dead.
# When cell is dead and there is exactly three alive neighbors, then it becomes alive.

# have it start randomly and watch it go or make it mannuel start.

# Need a pause feature

# we need to make it wrap around, when it reaches the left side it wraps over to the right side.
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from typing import List


# creates the preset cells to be alive.
def apply_preset(grid, preset_name):
    preset_name = preset_name.strip().lower()
    rows, cols = len(grid), len(grid[0])

    def set_cell(r, c):
        grid[r % rows][c % cols] = 1

    r0, c0 = rows // 2, cols // 2

    if preset_name == "blinker":
        set_cell(r0, c0 - 1)
        set_cell(r0, c0)
        set_cell(r0, c0 + 1)

    elif preset_name == "block":
        set_cell(r0, c0)
        set_cell(r0, c0 + 1)
        set_cell(r0 + 1, c0)
        set_cell(r0 + 1, c0 + 1)

    elif preset_name == "glider":
        set_cell(r0, c0 + 1)
        set_cell(r0 + 1, c0 + 2)
        set_cell(r0 + 2, c0)
        set_cell(r0 + 2, c0 + 1)
        set_cell(r0 + 2, c0 + 2)

    elif preset_name == "empty":
        pass

    else:
        raise ValueError("\n\nRun program again. You did not pick a correct preset!!\n")

# adding in a txt file 
def load_pattern_from_file(path: str) -> List[List[int]]:
    """
    Load a pattern from a text file.
    Accepts rows of 0/1 separated by spaces and/or commas.
    Example file:
        0 1 0
        0 0 1
        1 1 1
    """
    pattern: List[List[int]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # allow commas or spaces
            line = line.replace(",", " ")
            parts = [p for p in line.split() if p]
            row = []
            for p in parts:
                if p not in ("0", "1"):
                    raise ValueError(f"Invalid cell value '{p}' in file. Use only 0 or 1.")
                row.append(int(p))
            if row:
                pattern.append(row)

    if not pattern:
        raise ValueError("File did not contain any 0/1 rows.")

    # Ensure rectangular
    w = max(len(r) for r in pattern)
    for r in pattern:
        if len(r) != w:
            raise ValueError("Pattern file rows have different lengths (must be rectangular).")

    return pattern

def stamp_pattern_center(grid, pattern: List[List[int]]):
    """Center-stamp a smaller pattern onto the main grid."""
    rows, cols = len(grid), len(grid[0])
    ph, pw = len(pattern), len(pattern[0])
    r0 = rows // 2 - ph // 2
    c0 = cols // 2 - pw // 2

    for pr in range(ph):
        for pc in range(pw):
            rr = (r0 + pr) % rows
            cc = (c0 + pc) % cols
            grid[rr][cc] = 1 if pattern[pr][pc] == 1 else 0

# This is where user will select the rules they want.

print("Welcome to cellular automata!\nPlease select the rules you want.\n")
print("  1) Original Conway (1)")
print("  2) HighLife (2)\n")

# Checking the input and applying the rules for the neighbors
while True:
    rule_choice = input("\nEnter 1 or 2: ").strip()
    if rule_choice == "1":
        birth, survive = {3}, {2, 3}      # Conway
        break
    elif rule_choice == "2":
        birth, survive = {3, 6}, {2, 3}   # HighLife
        break
    else:
        print("Please type 1 for Conway or 2 for HighLife.\n")


# ---- PRESET SELECTION ----
print("\nNOW, select the starting board you want!")
print("Type: random, file, empty, blinker, block, or glider")
preset = input("\nChoose: ").strip().lower()


#--------- Code for the actual game

# setup for the grid
rows, cols = 60, 60
grid = [[0 for _ in range(cols)] for _ in range(rows)]

#this sets up the board. Giving 25 percent of them life and leaving 75 percent dead.
if preset == "random":
    cell_alive = 0.25
    for r in range(rows):
        for c in range(cols):
            grid[r][c] = 1 if random.random() < cell_alive else 0
elif preset == "file":
    path = input("Enter the pattern file path (example: pattern.txt): ").strip()
    pattern = load_pattern_from_file(path)
    # start empty then stamp pattern
    stamp_pattern_center(grid, pattern)
else:
    # start empty then apply preset
    apply_preset(grid, preset)



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
                new_grid[r][c] = 1 if n in survive else 0
            else:
                new_grid[r][c] = 1 if n in birth else 0

    grid = new_grid




#matplotlib visualization 
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap="magma", interpolation="bicubic")
ax.set_xticks([])
ax.set_yticks([])

def animate(frame):
    
    step()
    img.set_data(grid)
    return (img,)
hint_text = fig.text(0.02, 0.98, "To pause, (press spacebar). Quit? (press q)", ha="left", va="top")
ani = animation.FuncAnimation(fig, animate, interval=75, blit=True)

# using on_key event to check for keyboard input
paused = False
def on_key(event):
    global paused

    # This checks to see if space and been hit, then it will either stop or start
    if event.key == " " or event.key == "space":
        paused = not paused

        if paused:
            ani.event_source.stop()
        else:
            ani.event_source.start()

fig.canvas.mpl_connect("key_press_event", on_key)


plt.show()




# References --- https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
# https://realpython.com/conway-game-of-life-python/