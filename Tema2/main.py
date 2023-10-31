# Step 1: Model the Problem
variables = [[0 for _ in range(9)] for _ in range(9)]
initial_board = [
    [8, 4, 0, 0, 5, 0, 0, 0, 0],
    [3, 0, 0, 6, 0, 8, 0, 4, 0],
    [0, 0, 0, 4, 0, 9, 0, 0, 0],
    [0, 2, 3, 0, 0, 0, 9, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 9, 8, 0, 0, 0, 1, 6, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 0],
    [0, 3, 0, 1, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 2, 0, 0, 1, 3]
]
for i in range(9):
    for j in range(9):
        variables[i][j] = initial_board[i][j]

# Step 2: Implement Forward Checking
def forward_check(variables, i, j, value):
    # Check if the assigned value conflicts with other variables
    for k in range(9):
        if k != j and variables[i][k] == value:
            return False
        if k != i and variables[k][j] == value:
            return False
    # Check sub-region constraints
    sub_i, sub_j = i//3*3, j//3*3
    for a in range(sub_i, sub_i+3):
        for b in range(sub_j, sub_j+3):
            if a != i and b != j and variables[a][b] == value:
                return False
    # Additional constraint: Certain cells must allow even numbers
    if (i, j) in [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)]:  # Add your specific cells here
        if value % 2 != 0:
            return False
    return True

# Step 3: Implement Variable Ordering (MRV)
def get_unassigned_variable(variables):
    # Find the unassigned variable with the fewest legal values left (MRV)
    min_legal_values = float('inf')
    selected_i, selected_j = None, None
    for i in range(9):
        for j in range(9):
            if variables[i][j] == 0:
                legal_values = [value for value in range(1, 10) if forward_check(variables, i, j, value)]
                if len(legal_values) < min_legal_values:
                    min_legal_values = len(legal_values)
                    selected_i, selected_j = i, j
    return selected_i, selected_j

# Main solving function (recursive backtracking with forward checking and MRV)
def solve(variables):
    i, j = get_unassigned_variable(variables)
    if i is None and j is None:
        return True  # All variables are assigned, solution found
    for value in range(1, 10):
        if forward_check(variables, i, j, value):
            variables[i][j] = value
            if solve(variables):
                return True
            variables[i][j] = 0  # Undo assignment if no solution found
    return False

# Call the solve function to find a solution
if solve(variables):
    print("Solution found:")
    for row in variables:
        print(row)
else:
    print("No solution found.")