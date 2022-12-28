sigma = 10          # standard deviation 
mu = [0, 0]         # target (expected value)
switch = False      # switch to check if mouse is at the board or at the slider 
numbers = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]

# lenght of radien
radius_of_board = 170
bullseye = 6.35
singlebull = 15.9
triple_inner = 99
triple_outer = 107
dopple_inner = 162
dopple_outer = radius_of_board

# radius_of_board = 169
# bullseye = 5.35
# singlebull = 14.9
# triple_inner = 98
# triple_outer = 106          
# dopple_inner = 161
# dopple_outer = radius_of_board

radien = [0, bullseye, singlebull, triple_inner, triple_outer, dopple_inner, dopple_outer]
radien_factor = [2, 1, 1, 3, 1, 2, 0]   # factor for each ring (3 --> triple field)

