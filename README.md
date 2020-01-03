# 2048_AI
A python implementation of the 2048 game with a Monte Carlo Tree Search algorithm 

# game_defs_2048.py
A python class and functions implementing the game - moves, game state, checking whether the game is over or not.

# ai_defs_2048.py
A very basic MCTS alogirthm that tries a number (100) of random plays (10 moves deep) and selects the move with the highest average.

Does an ok job (cracking the 2048) in many cases. 

Improvements to be added include: 1) parallelization 2) more advanced MCTS versions (playouts to be longer) 3) possibly ML/deep learning similar to Alpha Go to limit the search.

# how to run:
download both files; run the first few lines in *ai_defs_2048.py* in a python console and then edit the remaining code to run the mcts with or without printing the individual board states.
