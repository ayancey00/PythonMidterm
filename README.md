This README is for the ECEN 4293 Midterm, February 20, 2026
Authors: Adam  Yancey, Erica Saenz, Jordan Hackler 

This repository includes:
(1) README
(1) main.py
(1) basic.txt

main.py is our working code for the Cellular Automata Simualtion. 
basix.txt is a sample txt file than can be used in the program when prompted. 

Main.py Functions: 
Upon start up, the program asks if you'd like to play with two different rulesets: Conway's game of life and Highlife. These rule sets determine how cells change state based on the number of live neighbors.

After selecting a rule set, the user chooses an initial board configuration. The options include random initialization, built in presets such as blinker, block, and glider, an empty grid, or loading a pattern from a text file.

If the file option is selected, the program reads a text file such as basic.txt, which contains rows of 0s and 1s by seperate spaces. A value of 1 represents a live cell and 0 represents a dead cell. The program checks that te pattern is rectangular and then centers it onto the main grid before the simulation begins. Any custon pattern file must be places in the same folder as main.py.

The simulation runs on a fixed 60x60 grid. For each generations the program counts the eight neighboring cells of every position. Wrap around boundary conditions are implemented using the modulo indexing, meaning cells that move past one edge of the grid reappear on the opposite side.

Each generation is calculated using a new grid to ensure all cells update simultaneously. The viusaliztion is handled by using matplotlibs "funcAnimation", and the simulaion can be paused or resumed by pressing the spacebar.
