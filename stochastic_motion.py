# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    #set value of goal to 0
    value[goal[0]][goal[1]] = 0

    num_loop = 10000

    while num_loop > 0:
        #iterate through each item in list (except goal) to update probability
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if not (row is goal[0] and col is goal[1]):
                    #value[row][col] = 7
                    #break

                    #row = 0
                    #col = 2
                    min_val = 1000000
                    min_d = None

                    #check probability for each delta
                    for d in range(len(delta)):
                        success_row = row + delta[d][0]
                        success_col = col + delta[d][1]

                        left_row = row + delta[(d+1)%len(delta)][0]
                        left_col = col + delta[(d+1)%len(delta)][1]

                        right_row = row + delta[(d-1)%len(delta)][0]
                        right_col = col + delta[(d-1)%len(delta)][1]
                        

                        #print [success_row, success_col], [left_row, left_col], [right_row, right_col]
                        
                        success_val = collision_cost
                        if success_row >= 0 and success_row < len(grid):
                            if success_col >= 0 and success_col < len(grid[0]):
                                success_val = value[success_row][success_col]
                        
                        left_val = collision_cost
                        if left_row >= 0 and left_row < len(grid):
                            if left_col >= 0 and left_col < len(grid[0]):
                                left_val = value[left_row][left_col]
                            
                        right_val = collision_cost
                        if right_row >= 0 and right_row < len(grid):
                            if right_col >= 0 and right_col < len(grid[0]):
                                right_val = value[right_row][right_col]

                        new_val = success_prob * success_val + failure_prob * left_val + failure_prob * right_val + cost_step
                        #print new_val
                        if new_val < min_val:
                            min_val = new_val
                            min_d = d

                    #print min_val, min_d
                    value[row][col] = min_val
                    policy[row][col] = delta_name[min_d]

        num_loop -= 1



    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 100.00, 100.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
