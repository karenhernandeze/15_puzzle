from heapq import heappop, heappush
goal_state = []

class Puzzle:
    def __init__(self, state, parent=None, move=None, g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g # depth of the node 

    # keep track of the heap and saved the values from min to max value given the manhattan_distance + depth value 
    def __lt__(self, other):
        return (self.g + self.manhattan_distance()) < (other.g + other.manhattan_distance())

    # checks if the board configurations has all ready been visited 
    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

    def __getitem__(self, key):
        if key == "state":
            return self.state
        else:
            raise KeyError(f"Invalid key: {key}")

    def __repr__(self):
        return f"{self.state}\n{self.g+self.manhattan_distance()}\n"

    def get_zero_index(self):
        return self.state.index(0)

    def swap_numbers(self, i, j):
        # get state 
        new_state = list(self.state)
        # swap the number with the 0 
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def move_up(self):
        zero_index = self.get_zero_index()
        # check if the zero is not in the first row 
        if zero_index not in [0, 1, 2, 3]:
            # swap the zero one row up, so to do that substract 4 
            new_state = self.swap_numbers(zero_index, zero_index - 4)
            return Puzzle(new_state, parent=self, move="U", g=self.g + 1)
        return None

    def move_down(self):
        zero_index = self.get_zero_index()
        # check if the zero is not in the last row 
        if zero_index not in [12, 13, 14, 15]:
            # swap the zero one row down, so to do that add 4 
            new_state = self.swap_numbers(zero_index, zero_index + 4)
            return Puzzle(new_state, parent=self, move="D", g=self.g + 1)
        return None

    def move_left(self):
        zero_index = self.get_zero_index()
        # check if the zero is not in the first column 
        if zero_index not in [0, 4, 8, 12]:
            # swap the zero to the left, so to do that substract 1 
            new_state = self.swap_numbers(zero_index, zero_index - 1)
            return Puzzle(new_state, parent=self, move="L", g=self.g + 1)
        return None

    def move_right(self):
        zero_index = self.get_zero_index()
        # check if the zero is not in the last column 
        if zero_index not in [3, 7, 11, 15]:
            # swap the zero to the right, so to do that add 1 
            new_state = self.swap_numbers(zero_index, zero_index + 1)
            return Puzzle(new_state, parent=self, move="R", g=self.g + 1)
        return None

    # return the path the states took to reach the goal state 
    def get_path(self):
        current = self
        path = []
        while current is not None:
            if current.move:
                path.append(current.move)
            current = current.parent
        return list(reversed(path))

    # manhattan distance checks each number and adds the distance and returns the value 
    def manhattan_distance(self):
        h = 0
        # dictionary used to accomodate the state in a 4 x 4 manner and be able to substract the first value 
        # with the row of the number and also with the column with the second value
        dict = {0:[0,0], 1:[0,1], 2:[0,2], 3:[0,3], 4:[1,0], 5:[1,1], 6:[1,2], 
                7:[1,3], 8:[2,0], 9:[2,1], 10:[2,2], 11:[2,3], 12:[3,0], 
                13:[3,1], 14:[3,2], 15:[3,3]}

        # transverse through the board 
        for i in range(16):
            if self.state[i] != 0:
                current_row, current_col = i // 4, i % 4
                index = goal_state.index(self.state[i])
                i_x = dict[index][0]
                j_x = dict[index][1]
                # sum each manhattan distance for each number, except for the blank space (0)
                h += (abs(current_row - i_x) + abs(current_col - j_x))
        return h
    
def solve(initial_state):
    # iterator used to control the number of iterations the program has went thorugh 
    i = 0 
    # limit of iterations 
    limit = 1000

    # heap used to manage the open tree 
    open = []
    closed = {}

    # get initial state, assign f(n) and add to heap 
    state0 = Puzzle(initial_state)
    heappush(open, state0)

    while open:
        # control number of interations  
        i += 1
        # heap pop takes out the state with the lowest value 
        current_state = heappop(open)

        if current_state.state == goal_state:
            # print the path in format "D", "U", "L", "R" 
            return current_state.get_path()
        
        # REMOVE --------------------------------------- 
        # checks if the state is all ready in the closed array 
        # if tuple(current_state.state) in closed:
        #     function_value = closed[tuple(current_state.state)]
        #     # checks if
        #     if current_state.g + current_state.manhattan_distance() >= function_value:
        #         continue  # Skip this state as it has already been visited with a better or equal cost

        # If the current state is not in the closed_set or it has a better cost, add/update it in the closed_set
        closed[tuple(current_state.state)] = current_state.g + current_state.manhattan_distance()

        # returns None if the move can't be possible, or else returns the new Puzzle object 
        next_moves = [
            current_state.move_up(),
            current_state.move_down(),
            current_state.move_left(),
            current_state.move_right()
        ]

        # for each possible Move add to the open heap 
        for move in next_moves:
            if move is not None:
                # keep track of visited states 
                move_key = tuple(move.state)
                # check state is not in closed and hasnt been visited 
                if move_key not in closed:
                    heappush(open, move)

        # Limit of iterations has been reached 
        if i == limit:
            return None

def read_board(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        initial_state = [list(map(int, line.strip().split(','))) for line in lines[:4]]
        goal_state = [list(map(int, line.strip().split(','))) for line in lines[4:]]
    return initial_state, goal_state

if __name__ == "__main__":
    # Get the states from the txt file - returned in format: [[],[],[],[]]
    read_initial_state, read_initial_goal = read_board("Datos.txt")

    # convert the states to a 2D array - returned as []
    initial_state = [element for sublist in read_initial_state for element in sublist]
    goal_state_f = [element for sublist in read_initial_goal for element in sublist]
    # assign to the global variable 'goal_state' its value 
    goal_state = goal_state_f

    solution = solve(initial_state)
    result = ', '.join(solution)
    print(result)
