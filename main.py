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



def the_rules(rule_str):
    rule_str = rule_str.strip().upper()
    
    # if nothing put, it does the defult conway
    if rule_str == "":
        return {3}, {2, 3}  

    # Makes sure it is correct format, 
    if "B" not in rule_str or "S" not in rule_str:
        raise ValueError("\n\n\nYou MUST look like B3/S23\n\nTry again")



# this function makes a preset board. where cells will be alive. 
# need to find cooler presets!!!

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

    # If unknown preset, it kicks them out prompting to try again
    else:
        raise ValueError("\n\n\n\nRun program again. You did not pick a correct preset!!\n\n")


# This prints a screen for the user to select the type of rules they want
print("Welcome to cellular atomany!\n Please select the Style you want. \n")
print("  1) Oringal Conway: B3/S23\n")
print("  2) HighLife:         B36/S23\n")

rule_in = input("Please Enter rule like ( B3/S23 ): ")

birth, survive = the_rules(rule_in)

print("\n\nNOW, select the starting board you want!\n Type: random, empty, blinker, block, or glider")
preset = input("\nChoose: ").strip().lower()



#--------- Code for the acutally game------


# setup for the grid
rows, cols = 75, 75
grid = [[0 for _ in range(cols)] for _ in range(rows)]


#this sets up the board. Giving 25 percent of them life and leaving 75 percent dead.
if preset == "random":
    p_alive = 0.25
    for r in range(rows):
        for c in range(cols):
            grid[r][c] = 1 if random.random() < p_alive else 0
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
                new_grid[r][c] = 1 if (n == 2 or n == 3) else 0
            else:
                new_grid[r][c] = 1 if n == 3 else 0

    grid = new_grid



#matplotlib visualization 
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap="plasma", interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])

def animate(frame):
    
    step()
    img.set_data(grid)
    return (img,)

ani = animation.FuncAnimation(fig, animate, interval=50, blit=True)

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