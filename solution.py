assignments = []



rows = 'ABCDEFGHI'
cols = '123456789'



def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

# Create all the possible boxes on the board
boxes = cross(rows, cols)
# Create the row units constraints
row_units = [cross(r, cols) for r in rows]
# Create the col units constraints
column_units = [cross(rows, c) for c in cols]
# Create the 3x3 square units constraints
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Create two main diagonal Sudoku constraint
diag_units = [list(a + b for a,b in zip(list(rows), list(cols))),list(a + b for a,b in zip(list(rows), list(cols)[::-1]))]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# dictionary where key is a box and the value is a set of all other boxes in the same unit
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins

    from collections import defaultdict
    naked_twins_dict = defaultdict(list)
    for i, unit in enumerate(unitlist):
        num_str_location_dict = defaultdict(list)
        # create a dictionary where the key is the string, and the value is the list of the boxes where the values equals the key
        for box in unit:
            num_str_location_dict[''.join(sorted(values[box]))].append(box)

        # if the length of the key equals the length of the values (> 1), that means we found a naked twins. We need to add that into the naked_twins_dict.
        for key, value in num_str_location_dict.items():
            if len(key) == len(value) and len(value) > 1:
                naked_twins_dict[i].extend(list(key))
    # Eliminate the naked twins as possibilities for peers        
    for i, unit in enumerate(unitlist):
        for box in unit:
            # if the box is not one of the naked twins, remove the naked twins from the potential values
            if sorted(values[box]) != sorted(naked_twins_dict[i]):
                values[box] = ''.join(sorted(set(values[box]) - set(naked_twins_dict[i])))

    return values


def naked_twins(values):

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins

    from collections import defaultdict

    for i, unit in enumerate(unitlist):

        print("\n\nWorking on %d unit..." % i)
        
        # For each unique number list (should be a set) as a key, make a list of cells holding that number set.
        print("[Unit %d] Creating a dictionary with possible numbers as the key and a list of cells as the value..." % i)
        num_str_location_dict = defaultdict(list)
        for box in unit:
            num_str_location_dict[''.join(sorted(values[box]))].append(box)
        print("[Unit %d] This unit num_str_loc_dict:\n%s" % (i, str(num_str_location_dict)))

        # For each unique number set, identify the naked twins and remove them from other cells
        print("[Unit %d] Identifying naked twins in this unit..." % i) 
        remove_list = []
        for key, value in num_str_location_dict.items():
            if len(key) == len(value) and len(value) > 1:
                print("\n[Unit %d] Adding naked tuple %s to remove list." % (i, key))
                remove_list.append(key)
            
            # for each cell, if the cell is not one that contains this naked twin, remove the naked twin numbers from the cell
            if len(remove_list):
                print("[Unit %d] Removing naked tuples from all cells in this unit." % i)
                for box in unit:
                    for remove_val in remove_list:
                        if box not in num_str_location_dict[remove_val]:
                            #print('\n[Unit %d] Checking cell %s, current value %s...' % (i, box, values[box]))
                            #print("Going to remove naked twin value %s" % remove_val)
                            #print("Cell %s before removing naked twins: %s" % (box, values[box]))
                            #print('Now removing %s from %s in cell %s.' % (set(remove_val), set(values[box]), box) )
                            values[box] = ''.join(sorted(set(values[box]) - set(remove_val)))
                            #print("Cell %s after removing nake twins: %s" % (box, values[box]))
                            #print('\n')
                            #print(remove_list)
                            #print('Removing %s from cell %s (currently %s)' % (remove_list, box, values[box]))
    return values




def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    # Nine by nine grid
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CFu': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    # if the length of the value is 1, then this box is solved
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # for all the solved boxes, remove this value from all the peers for this box
    for box in solved_values:
        digit = values[box]
        # Remove solved digit from the list of possible values for each peer
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """

    for unit in unitlist:
        for digit in '123456789':
            # Create a list of all the boxes in the unit in question
            # that contain the digit in question
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # This box is the only choice for this digit
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # a list of all the solved boxes
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # run function elimate and only_choice to solve it iteratively.
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solved = search(values)
    if solved:
        return solved
    else:
        return False



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
