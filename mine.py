import random
import re
import time
from operator import eq
from string import ascii_lowercase


class Equation:
    def __init__(self, lhs, rhs, influence_blocks):
        self.lhs = frozenset(lhs)
        self.rhs = int(rhs)
        self.influence_blocks = frozenset(influence_blocks)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.lhs == other.lhs

    def __repr__(self):
        s = ""
        for row, col in self.lhs:
            s += chr(ord('a') + col) + str(row + 1) + " + "
        return s[:-2] + " = " + str(self.rhs)


class DummyPlayer:

    def __init__(self):
        self.gridsize = -1
        self.grid = []
        self.knowledge_base = set()
        self.safe_moves = []

    def next_move(self):
        print(self.knowledge_base)
        if len(self.safe_moves) != 0:
            move = self.safe_moves.pop()
            return chr(ord('a') + move[1]) + str(move[0] + 1) + ("f" if move[2] == 1 else "")
        else:
            if self.grid == []:
                return "a1"     # First move
            else:
                for i in range(self.gridsize):
                    for j in range(self.gridsize):
                        if self.grid[i][j] == ' ':      # indicates unexplored node
                            for eq in self.knowledge_base:
                                # if the current cell is in any of the equation's LHS, then it might have a mine
                                if (i, j) in eq.lhs:
                                    break
                            else:
                                return chr(ord('a') + j) + str(i + 1)
                else:
                    # No cell was found which is unexplored and not present in any equation's LHS.
                    # so pick randomly
                    print("******************Logical Deadend******************\nPraying to the Almighty and making a random move!!!")

                    return random.choice(ascii_lowercase[:self.gridsize]) + str(random.randrange(1, self.gridsize))     # randomly making moves

    def combine_equations(self, eq1, eq2):

        if len(eq1.lhs) > len(eq2.lhs):
            smaller_eq = eq2
            larger_eq = eq1
        else:
            smaller_eq = eq1
            larger_eq = eq2

        if smaller_eq.lhs.issubset(larger_eq.lhs):
            x = larger_eq.lhs - smaller_eq.lhs
            inference_eq = Equation(x, int(larger_eq.rhs) - int(smaller_eq.rhs), smaller_eq.influence_blocks | larger_eq.influence_blocks)             #(frozenset(x), int(larger_eq[1]) - int(smaller_eq[1]))
            if larger_eq in self.knowledge_base:
                self.knowledge_base.remove(larger_eq)
            # print("Adding Inference Eq", inference_eq, " From\n", larger_eq, "\n", smaller_eq)
            self.add_equation_to_knowledgebase(inference_eq)

    def add_equation_to_knowledgebase(self, new_equation):
        if new_equation not in self.knowledge_base:
            self.knowledge_base.add(new_equation)
            print("Adding: ", new_equation)
            print(self.knowledge_base)
            if new_equation.rhs == 1 and len(new_equation.lhs) == 1:
                tepm = 0
            if len(new_equation.lhs) > 1:
                if new_equation.rhs == 0:
                    self.knowledge_base.remove(new_equation)
                    for row, col in new_equation.lhs:
                        if (row, col, 0) not in self.safe_moves:
                            self.safe_moves.insert(0, (row, col, 0))
                        self.add_equation_to_knowledgebase(Equation([(row, col)], 0, new_equation.influence_blocks))
                elif new_equation.rhs == len(new_equation.lhs):
                    self.knowledge_base.remove(new_equation)
                    for row, col in new_equation.lhs:
                        if (row, col, 1) not in self.safe_moves:
                            self.safe_moves.insert(0, (row, col, 1))
                        self.add_equation_to_knowledgebase(Equation([(row, col)], 1, new_equation.influence_blocks))

            for eq in self.knowledge_base.copy():
                if eq.lhs != new_equation.lhs:
                    self.combine_equations(eq, new_equation)

    def put_new_info(self, info, new_grid):
        self.grid = new_grid
        self.gridsize = len(new_grid)
        LHS = []
        RHS = info[2]
        for cell in getneighbors(self.grid, info[0], info[1]):
            if self.grid[cell[0]][cell[1]] == ' ':
                LHS.append(cell)
            elif self.grid[cell[0]][cell[1]] == 'F':
                RHS = RHS - 1

        if len(LHS) != 0:
            new_equation = Equation(LHS, info[2], [(info[0], info[1])])
            self.add_equation_to_knowledgebase(new_equation)


def setupgrid(gridsize, start, numberofmines):
    emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

    mines = getmines(emptygrid, start, numberofmines)

    for i, j in mines:
        emptygrid[i][j] = 'X'

    grid = getnumbers(emptygrid)

    return (grid, mines)


def showgrid(grid):
    gridsize = len(grid)

    horizontal = '   ' + (4 * gridsize * '-') + '-'

    # Print top column letters
    toplabel = '     '

    for i in ascii_lowercase[:gridsize]:
        toplabel = toplabel + i + '   '

    print(toplabel + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row = '{0:2} |'.format(idx + 1)

        for j in i:
            row = row + ' ' + j + ' |'

        print(row + '\n' + horizontal)

    print('')


def getrandomcell(grid):
    gridsize = len(grid)

    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)

    return (a, b)


def getneighbors(grid, rowno, colno):
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append((rowno + i, colno + j))

    return neighbors


def getmines(grid, start, numberofmines):
    mines = []
    neighbors = getneighbors(grid, *start)

    for i in range(numberofmines):
        cell = getrandomcell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getrandomcell(grid)
        mines.append(cell)

    return mines


def getnumbers(grid):
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != 'X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getneighbors(grid,
                                                              rowno, colno)]

                # Counts how many are mines
                grid[rowno][colno] = str(values.count('X'))

    return grid


def showcells(grid, currgrid, rowno, colno):
    # Exit function if the cell was already shown
    if currgrid[rowno][colno] != ' ':
        return

    # Show current cell
    currgrid[rowno][colno] = grid[rowno][colno]
    '''
    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r, c in getneighbors(grid, rowno, colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currgrid[r][c] != 'F':
                showcells(grid, currgrid, r, c)'''
    return grid[rowno][colno]

'''
def playagain():
    choice = input('Play again? (y/n): ')

    return choice.lower() == 'y'
'''

def parseinput(inputstring, gridsize, helpmessage):
    cell = ()
    flag = False
    message = "Invalid cell. " + helpmessage

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
    validinput = re.match(pattern, inputstring)

    if inputstring == 'help':
        message = helpmessage

    elif validinput:
        rowno = int(validinput.group(2)) - 1
        colno = ascii_lowercase.index(validinput.group(1))
        flag = bool(validinput.group(3))

        if -1 < rowno < gridsize:
            cell = (rowno, colno)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}


def playgame(dummyPlayer=None, grid=None, numberofmines=-1, mines=None):
    if grid is None:
        gridsize = 9
        numberofmines = 10
        grid = []
        mines = []
        dummyPlayer.gridsize = gridsize
    else:
        gridsize = len(grid)
        numberofmines = numberofmines

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    flags = []
    #starttime = 0

    helpmessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    showgrid(currgrid)
    print(helpmessage + " Type 'help' to show this message again.\n")

    while True:
        minesleft = numberofmines - len(flags)
        if dummyPlayer is None:
            prompt = input('Enter the cell ({} mines left): '.format(minesleft))
        else:
            prompt = dummyPlayer.next_move()
            print("Move: ", prompt)
        result = parseinput(prompt, gridsize, helpmessage + '\n')

        message = result['message']
        cell = result['cell']

        if cell:
            print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']

            if not grid:
                grid, mines = setupgrid(gridsize, cell, numberofmines)
                print(grid)
            '''
            if not starttime:
                starttime = time.time()'''

            if flag:
                # Add a flag if the cell is empty
                if currcell == ' ':
                    currgrid[rowno][colno] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif currcell == 'F':
                    currgrid[rowno][colno] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'

            elif grid[rowno][colno] == 'X':
                print('Game Over\n')
                showgrid(grid)
                #if playagain():
                    #playgame()
                return

            elif currcell == ' ':
                cell_value = showcells(grid, currgrid, rowno, colno)
                if dummyPlayer is not None:
                    dummyPlayer.put_new_info((rowno, colno, int(cell_value)), currgrid)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                #minutes, seconds = divmod(int(time.time() - starttime), 60)
                print(
                    'You Win. ')
                    #'It took you {} minutes and {} seconds.\n'.format(minutes,
                    #                                                 seconds))
                showgrid(grid)
                '''
                if playagain():
                    playgame()'''
                return

        showgrid(currgrid)
        print(message)


if __name__ == "__main__":

    # Positive Testcase
    # numberofmines = 2
    # grid = [['0', '1', '1', '1'], ['0', '2', 'X', '2'], ['0', '2', 'X', '2'], ['0', '1', '1', '1']]
    # mines = [(1, 2), (2, 2)]

    # Negative Testcase
    numberofmines = 10
    grid = [['0', '0', '0', '0', '1', 'X', '2', '1', '0'], ['0', '0', '0', '0', '1', '2', 'X', '1', '0'], ['0', '0', '0', '0', '1', '2', '2', '1', '0'], ['0', '0', '0', '0', '1', 'X', '2', '1', '0'], ['0', '0', '0', '0', '1', '2', 'X', '1', '0'], ['1', '1', '1', '0', '1', '2', '3', '3', '2'], ['1', 'X', '1', '0', '1', 'X', '3', 'X', 'X'], ['1', '2', '2', '1', '1', '2', 'X', '3', '2'], ['0', '1', 'X', '1', '0', '1', '1', '1', '0']]
    mines = [(0, 5),(1, 6),(3, 5),(4, 6),(6, 1),(6, 5),(6, 7),(6, 8),(7, 6),(8, 2)]
    playgame(DummyPlayer(), grid, numberofmines, mines)
    # playgame(DummyPlayer(), None, None, None)
    # playgame()