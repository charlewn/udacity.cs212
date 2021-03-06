"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8
def successors(s):
    """return a dict of {state:action} pairs describing what can be reach from the  s state and how
    In this case something like this:
    {state1: action1, state2: action2,}
    """
    dicto = {}
    
    def filter_object(car):
        'filter objects that are the exit or a wall'
        return car not in ['@','|']
    def move_h(car):
        'does this car moves horizontaly?'
        d = abs(car[0] - car[1])
        return d == 1
    def move_v(car):
        'does this car moves verticaly'
        d = abs(car[0] - car[1])
        return d != 1
    def is_space_empty(state,car,i):
        '''checks if car can move to position i 
         special case for car * as it can walk through 
         the exit ie: @'''
        if car =='*':
            d = dict(state)
            if i in d['@']:
                return True
        #normal cases
        for pair in state:
            if i in pair[1]:
                return False
        return True
    def populate_dict(car,succ):
        verbose = False
        if len(succ)==0:
            return
        state = dict(s)
        car_pos = state[car]
        
        for x in succ:
            move = 0
            if x > car_pos[0]:
                move = x - car_pos[-1]
            else:
                move = x - car_pos[0]
            t = tuple()
            for pos in car_pos :
                t = t + (pos+move,)
            state1 = dict(s)
            state1[car] = t
            dicto[tuple(state1.items())] = (car,move)

    def print_dict():
        print '--------------------'
        for k in dicto.keys():
            print dicto[k]   
    def successors_of_car(state,car,loc):
        res = ()
        if move_h(loc):
            extremity_left = loc[0]
            extremity_right = loc[-1]
            i = extremity_left
            i = i - 1
            while is_space_empty(state,car,i):
                res = res + (i,)
                i = i - 1
            j = extremity_right
            j = j + 1
            while is_space_empty(state,car,j):
                res = res + (j,)
                j = j + 1
        else:
            if not move_v(loc):
                print 'warning: object %s does not move up/down nor left/right'
            extremity_up = loc[0]
            extremity_down = loc[-1]
            i = extremity_up 
            i = i - N
            while is_space_empty(state,car,i):
                res = res + (i,)
                i = i - N
            j = extremity_down
            j = j + N
            while is_space_empty(state,car,j):
                res = res + (j,)
                j = j + N
        return res
    #successor function:
    succ = ()    
    for car, loc in s:
        if filter_object(car):
            succ = successors_of_car(s,car,loc)
            populate_dict(car,succ)
    return dicto.copy()

def solve_parking_puzzle(start, N=N):
    '''Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid.'''
    def is_goal(s):
        goal = ()
        car = ()
        for pairs in s:
            if pairs[0]== '@':
                goal = pairs
            if pairs[0] == '*':
                car = pairs
        for pos in car[1]:
            if pos in goal[1]:
                return True
        return False
    #from Stuart Banks:
    #http://forums.udacity.com/questions/5012700/animate-your-exam-4-solutions#cs212    
    def animate_puzzle(puzzle):
        from os import system
        from time import sleep
        'Shows a puzzle being solved step by step'
        states = shortest_path_search(grid(puzzle,N),successors,is_goal)
        system('clear')
        print '\n'
        for i, state in enumerate(states):
            if i % 2 == 0:
                show(state)
                sleep(0.4)
                system('clear')
            else:
                print 'Action:', state, '\n'
                
    return shortest_path_search(grid(start,N), successors, is_goal)
    #return path_actions(path)


# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    t = (start,)
    current = start + incr
    for i in range(n-1):
        t = t + (current,)
        current = current + incr
    return t

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    t = ()
    goal = ()
    if (N%2)==0:
        goal = ('@',(N*N/2 -1,)) 
        goal_index = N*N/2 -1
    else:
        goal = ('@',((N-1)+(N*(N/2)),))
        goal_index = (N-1)+(N*(N/2))
    
    t = t + (goal,)
    for pairs in cars:
        t = (t) + (pairs,)
    t_walls = tuple(range(N-1))
    count = N - 1
    while count < N*(N-1):
        if count != goal_index:
            t_walls = t_walls + (count,)
        if count+1 != goal_index:
            t_walls = t_walls + (count+1,)
        count = count + N
    t_walls = t_walls + tuple(range(count - (N-2),count +1))
    t = t + (('|',t_walls),)
    return t

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

puzzle4 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 2, N))))

puzzle5 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 2, N)),
    ('Y', locs(41,6))))

puzzle6 = (('@', (14,)),(('*',(11,12))), ('|', (0, 1, 2, 3, 4, 5, 9, 10, 15, 19, 20, 21, 22, 23, 24)))

puzzle7 = grid((
    ('*', locs(11, 2)),
    ('B', locs(20, 2, N))
    ),9)
def test_puzzles():
    print 'puzzle1'
    show(puzzle1)
    print solve_parking_puzzle(puzzle1)
    print 'puzzle2'
    show(puzzle2)    
    print solve_parking_puzzle(puzzle2)
    print 'puzzle3'
    show(puzzle3)
    print solve_parking_puzzle(puzzle3)
    print 'puzzle4'
    show(puzzle4)
    print solve_parking_puzzle(puzzle4)
    print 'puzzle5'
    show(puzzle5)
    print solve_parking_puzzle(puzzle5)
    print 'puzzle6'
    show(puzzle6,5)
    print solve_parking_puzzle(puzzle6, 5)
    print 'puzzle7'
    show(puzzle7,9)
    print solve_parking_puzzle(puzzle7, 9)
def test_puzzles2():
    'tests from Mon Z'
    'http://forums.udacity.com/questions/5011598/parking-tests#cs212'
    from itertools import cycle
    cars = cycle('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    hcar = lambda start, l=2: (next(cars), locs(start, l))
    vcar = lambda start, l=2: (next(cars), locs(start, l, N))
    star = lambda start: ('*', locs(start, 2))
    more_tests = [
        grid((vcar(9), hcar(12, 3), vcar(20), vcar(22, 3), star(25), vcar(29), hcar(33, 3), vcar(43), hcar(45), hcar(49), hcar(52))),
        grid((hcar(9), vcar(12, 3), vcar(14), vcar(17, 3), vcar(21, 3), star(26), vcar(30), hcar(34, 3), vcar(41), hcar(45), hcar(53))),
        grid((vcar(9, 3), hcar(10), vcar(12, 3), star(26), vcar(35), hcar(36, 3), vcar(46), hcar(51, 3),)),
        grid((vcar(9), hcar(10), vcar(14, 3), vcar(19, 3), star(25), hcar(36, 3), vcar(45), hcar(49, 3),)),
        grid((hcar(9), vcar(11), vcar(12, 3), vcar(17, 3), star(26), hcar(34, 3), hcar(52, 3),)),
        grid((vcar(11), hcar(12, 3), vcar(17), vcar(20, 3), hcar(21), star(26), vcar(34), hcar(37), vcar(41), hcar(43), vcar(46), hcar(50, 3),)),
        grid((vcar(9, 3), hcar(10), vcar(18), vcar(19), star(28), vcar(13), vcar(22, 3), hcar(33, 3), vcar(36), vcar(43), hcar(49), hcar(52), hcar(45),))
        ]

    def show_and_solve(puzzle):
        show(puzzle)
        print path_actions(solve_parking_puzzle(puzzle))
        print
    for test in more_tests:
        show_and_solve(test)

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

"""
The successor function needs to have two params:
parameter 1: the current grid
parameter 2: the car you want to analyse

the successor function should return a dictionary of items


state: the state of the car after action is performed
action: the action done 
example: ('A', -3)

"""
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

