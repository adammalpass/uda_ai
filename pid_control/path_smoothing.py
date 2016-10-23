# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite 
# correct).
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    #######################
    ### ENTER CODE HERE ###
    #######################

    #Formula to use:    yi <- yi + alpha (xi - yi) + beta (yi + 1 + yi - 1 - 2 * yi)
    #print newpath
    num_loops = 0
    time_out = 100
    converged = False

    while converged == False:
        converged = True
        for i in range(1,len(newpath)-1):
            for j in range(len(newpath[0])):
                new_value = newpath[i][j] + weight_data * (path[i][j] - newpath[i][j]) + weight_smooth * (newpath[i-1][j] + newpath[i+1][j] - 2.0 * newpath[i][j])
                
                if abs(new_value - newpath[i][j]) >= tolerance:
                    newpath[i][j] = new_value
                    converged = False
        
        num_loops += 1

        if converged:
            print "Converged in ", num_loops, " steps."
        elif num_loops > time_out:
            print "Covergence failed. Timeout after ", time_out, " steps."
            break

    return newpath # Leave this line for the grader!

printpaths(path,smooth(path))
