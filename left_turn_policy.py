# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    value = [[[99 for row in range(len(grid[0]))] for col in range(len(grid))],
            [[99 for row in range(len(grid[0]))] for col in range(len(grid))],
            [[99 for row in range(len(grid[0]))] for col in range(len(grid))],
            [[99 for row in range(len(grid[0]))] for col in range(len(grid))]]
    
    closed = []
    opened = []
    opened.append(init)
    
    while len(opened) > 0:
        toAdd = []
        for a in range(len(action)):
            prev_dir = opened[-1][2]
            prev_row = opened[-1][0]
            prev_col = opened[-1][1]
            next_dir = (prev_dir + action[a]) % len(forward)
            next_row = prev_row + forward[next_dir][0]
            next_col = prev_col + forward[next_dir][1]
            next_ = [next_row, next_col, next_dir]
   
            if next_row >=0 and next_row < len(grid): #check row co-ordinate valid
                if next_col >=0 and next_col < len(grid[0]): #check col co-ordinate valid
                    if grid[next_row][next_col] == 0: #check cell occupiable
                        next_val = value[prev_dir][prev_row][prev_col] - cost[a]
                        if value[next_dir][next_row][next_col] == 99 or next_val > value[next_dir][next_row][next_col]:
                            value[next_dir][next_row][next_col] = next_val
                            toAdd.append(next_)

        closed.append(opened.pop())

        for i in toAdd:
            opened.append(i)
    
    max = 0
    max_dir = -1    
    for dir in range(len(value)):
        goal_value = value[dir][goal[0]][goal[1]]
        if goal_value != 99 and goal_value > max:
            max = goal_value
            max_dir = dir
            
    print "Best goal value: " + str(max) + " from direction: " + str(forward_name[max_dir])
    
    rev_row = goal[0]-forward[max_dir][0]
    rev_col = goal[1]-forward[max_dir][1]
    rev_goal = [rev_row, rev_col]
    rev_val = value[max_dir][rev_row][rev_col]
    #print rev_val
    #print rev_goal
    
    #policy2D[rev_row][rev_col] = max_dir #TODO
    
    prev_val = rev_val
    #print prev_val
    prev_dir = max_dir
    prev_row = rev_row
    prev_col = rev_col
    
    init_reached = 10
    
    while init_reached > 0: #TODO - Temporary to avoid infinite loop until goal found correctly
        for a in range(len(action)):
            #next_dir = (prev_dir - action[a]) % len(forward) ###TODO - This is only true if no turns....
            next_row = prev_row - forward[prev_dir][0]
            next_col = prev_col - forward[prev_dir][1]
            next_ = [next_row, next_col, next_dir]

            #print next_row, next_col, next_dir
            #print next
   
            if next_row >=0 and next_row < len(grid): #check row co-ordinate valid
                #print "watch2"
                if next_col >=0 and next_col < len(grid[0]): #check col co-ordinate valid
                    #print "watch3"
                    #print next_r, grid[next_col][next_row]
                    if grid[next_row][next_col] == 0: #check cell occupiable
                        for poss_dir in [0,1,2,3]:
                            print "Pre  - V,R,C,D: ", prev_val, prev_row, prev_col, prev_dir
                            print "Next - V,R,C,D: ", value[poss_dir][next_row][next_col], next_row, next_col, poss_dir
                            #print value[next_dir][next_row][next_col], prev_row, prev_col, next_dir, cost[next_dir]
                            if value[poss_dir][next_row][next_col] - prev_val == cost[(poss_dir-prev_dir+1)%len(cost)]: ##TODO - FIX
                                #print next_row, next_col, next_dir
                                print "Hit"
                                policy2D[prev_row][prev_col] = action_name[a]
                                tmp_prev_val = value[poss_dir][next_row][next_col]
                                tmp_prev_row = next_row
                                tmp_prev_col = next_col
                                tmp_prev_dir = poss_dir
                            
                                if next_row == init[0] and next_col == init[1]:
                                    init_reached = True
                                
        prev_val = tmp_prev_val
        prev_row = tmp_prev_row
        prev_col = tmp_prev_col
        prev_dir = tmp_prev_dir
        #print prev_val, prev_row, prev_col, prev_dir
        init_reached -= 1
                        
    for l in value:
        for l2 in l:
            print l2
        print ""
    
    #for l in value:
    #    print l
    
    policy2D[goal[0]][goal[1]] = '*'
    return policy2D

result = optimum_policy2D(grid,init,goal,cost)
for l in result:
    print l
