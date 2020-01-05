# 2048_AI
A python implementation of the 2048 game with a Monte Carlo Tree Search algorithm. Requires sys, os numpy, copy, random, tkinter, and PIL modules. All of these are usually pre-installed.

# game_defs_2048.py
A python class and functions implementing the game - moves, game state, checking whether the game is over or not.

# ai_defs_2048.py
A very basic MCTS alogirthm that tries a number (100) of random plays (10 moves deep) and selects the move with the highest average.

Does an ok job (cracking the 2048) in many cases. 

Improvements to be added include: 1) parallelization 2) more advanced MCTS versions (playouts to be longer) 3) possibly ML/deep learning similar to Alpha Go to limit the search.

# How to run:
1) Download all files to a folder of your choice
2) Start a terminal in that folder
3) Make sure all python modules are installed
4) Type *python mcts_2048_run.py* and a window will appear playing the 2048 game. Achieved game score will be printed to the terminal console.
