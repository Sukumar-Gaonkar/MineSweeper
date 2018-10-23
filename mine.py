import random
import re
import time
from operator import eq
from string import ascii_lowercase


class DummyPlayer:

    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.grid = []
        self.knowledge_base = set()

    def next_move(self):
        return random.choice(ascii_lowercase[:self.gridsize]) + str(random.randrange(1, self.gridsize))     # randomly making moves

    def equation_tostring(self, eq):
        s = ""
        for row, col in eq[0]:
            s += chr(ord('a') + col) + str(row+1) + " + "
        return s[:-2] + " = " + eq[1]

    def combine_equations(self, eq1, eq2):
        pass

    def put_new_info(self, info, new_grid):
        # TODO: Implement put_new_info()
        self.grid = new_grid
        LHS = []
        for cell in getneighbors(grid, info[0], info[1]):
            if self.grid[cell[0]][cell[1]] == ' ':
                LHS.append(cell)
        new_equation = (tuple(LHS), info[2])
        if new_equation not in self.knowledge_base:
            self.knowledge_base.add(new_equation)
        print(self.equation_tostring(new_equation))
        for eq in self.knowledge_base:
            if eq != new_equation:
                self.combine_equations(eq, new_equation)



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


def playgame(dummyPlayer=None, grid=None, numberofmines=-1):
    if grid is None:
        gridsize = 9
        numberofmines = 10
    else:
        gridsize = len(grid)
        numberofmines = numberofmines

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    grid = []
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
                    dummyPlayer.put_new_info((rowno, colno, cell_value), currgrid)

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

    gridsize = 4
    numberofmines = 2
    grid, mines = setupgrid(gridsize, (1, 1), numberofmines)
    playgame(DummyPlayer(gridsize), grid, numberofmines)
    # playgame()