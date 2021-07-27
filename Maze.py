#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''
''' Run cool maze generating algorithms. '''
import random
import pygame


class Cell:
    ''' Represents a single cell of a maze.  Cells know their neighbors
        and know if they are linked (connected) to each.  Cells have
        four potential neighbors, in NSEW directions.
    '''

    def __init__(self, row, column):
        assert row >= 0
        assert column >= 0
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.visit = False


    def visited(self):
        self.visit = True

    def isvisited(self):
        return self.visit

    def link(self, cell, bidirectional=True):
        ''' Carve a connection to another cell (i.e. the maze connects them)'''
        assert isinstance(cell, Cell)
        self.links[cell] = True
        if bidirectional:
            cell.link(self, bidirectional=False)

    def unlink(self, cell, bidirectional=True):
        ''' Remove a connection to another cell (i.e. the maze
            does not connect the two cells)

            Argument bidirectional is here so that I can call unlink on either
            of the two cells and both will be unlinked.
        '''
        assert isinstance(cell, Cell)
        del self.links[cell]
        if bidirectional:
            cell.unlink(self, bidirectional=False)

    def is_linked(self, cell):
        ''' Test if this cell is connected to another cell.

            Returns: True or False
        '''
        assert isinstance(cell, Cell)
        if cell in self.links.keys():
            return True
        else:
            return False

    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        return self.links.keys()

    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        return len(self.all_links())

    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        list = []
        if self.north is not None:
            list.append(self.north)
        if self.south is not None:
            list.append(self.south)
        if self.east is not None:
            list.append(self.east)
        if self.west is not None:
            list.append(self.west)
        return list

    def __str__(self):
        return f'Cell at {self.row}, {self.column}'


class Grid:
    ''' A container to hold all the cells in a maze. The grid is a
        rectangular collection, with equal numbers of columns in each
        row and vis versa.
    '''

    def __init__(self, num_rows, num_columns):
        assert num_rows > 0
        assert num_columns > 0
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = self.create_cells()
        self.connect_cells()

    def create_cells(self):
        ''' Call the cells into being.  Keep track of them in a list
            for each row and a list of all rows (i.e. a 2d list-of-lists).

            Do not connect the cells, as their neighbors may not yet have
            been created.
        '''
        list = []
        for x in range(self.num_rows):
            row = []
            for y in range(self.num_columns):
                row.append(Cell(x, y))
            list.append(row)
        return list

    def connect_cells(self):
        ''' Now that all the cells have been created, connect them to
            each other.
        '''
        for list in self.grid:
            for cell in list:
                if cell.row - 1 >= 0:
                    cell.north = self.grid[cell.row - 1][cell.column]
                if cell.row + 1 < self.num_rows:
                    cell.south = self.grid[cell.row + 1][cell.column]
                if cell.column - 1 >= 0:
                    cell.west = self.grid[cell.row][cell.column - 1]
                if cell.column + 1 < self.num_columns:
                    cell.east = self.grid[cell.row][cell.column + 1]

    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        return self.grid[row][column]

    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        list = []
        for x in range(self.num_rows):
            for y in range(self.num_columns):
                if len(self.grid[x][y].all_links()) < 2:
                    list.append(self.grid[x][y])
        return list

    def each_cell(self):
        ''' A generator.  Each time it is called, it will return one of
            the cells in the grid.
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                c = self.cell_at(row, col)
                yield c

    def each_row(self):
        ''' A row is a list of cells.'''
        for row in self.grid:
            yield row

    def random_cell(self):
        ''' Chose one of the cells in an independent, uniform distribution. '''
        row = random.randint(0, self.num_rows - 1)
        columns = random.randint(0, self.num_columns - 1)
        return self.grid[row][columns]

    def size(self):
        ''' How many cells are in the grid? '''
        return self.num_rows * self.num_columns

    def set_markup(self, markup):
        ''' Warning: this is a hack.
            Keep track of a markup, for use in representing the grid
            as a string.  It is used in the __str__ function and probably
            shouldn't be used elsewhere.
        '''
        self.markup = markup

    def __str__(self):
        ret_val = '+' + '---+' * self.num_columns + '\n'
        for row in self.grid:
            ret_val += '|'
            for cell in row:
                cell_value = self.markup[cell]
                ret_val += '{:^3s}'.format(str(cell_value))
                if not cell.east:
                    ret_val += '|'
                elif cell.east.is_linked(cell):
                    ret_val += ' '
                else:
                    ret_val += '|'
            ret_val += '\n+'
            for cell in row:
                if not cell.south:
                    ret_val += '---+'
                elif cell.south.is_linked(cell):
                    ret_val += '   +'
                else:
                    ret_val += '---+'
            ret_val += '\n'
        return ret_val


class Markup:
    ''' A Markup is a way to add data to a grid.  It is associated with
        a particular grid.

        In this case, each cell can have a single object associated with it.

        Subclasses could have other stuff, of course
    '''

    def __init__(self, grid, default=' '):
        self.grid = grid
        self.marks = {}  # Key: cell, Value = some object
        self.default = default

    def reset(self):
        self.marks = {}

    def __setitem__(self, cell, value):
        self.marks[cell] = value

    def __getitem__(self, cell):
        return self.marks.get(cell, self.default)

    def set_item_at(self, row, column, value):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            self.marks[cell] = value
        else:
            raise IndexError

    def get_item_at(self, row, column):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            return self.marks.get(cell)
        else:
            raise IndexError

    def max(self):
        ''' Return the cell with the largest markup value. '''
        return max(self.marks.keys(), key=self.__getitem__)

    def min(self):
        ''' Return the cell with the largest markup value. '''
        return min(self.marks.keys(), key=self.__getitem__)


class DijkstraMarkup(Markup):
    ''' A markup class that will run Djikstra's algorithm and keep track
        of the distance values for each cell.
    '''

    def __init__(self, grid, root_cell, default=0):
        ''' Execute the algorithm and store each cell's value in self.marks[]
        '''
        super().__init__(grid, default)
        count = 0
        self.recur(root_cell, count)

    def recur(self, cell, count):
        cell.visited()
        self.marks[cell] = count
        for nebor in cell.all_links():
            if not nebor.isvisited():
                self.recur(nebor, count + 1)

    def farthest_cell(self):
        ''' Find the cell with the largest markup value, which will
            be the one farthest away from the root_call.

            Returns: Tuple of (cell, distance)
        '''
        return self.max()



class ShortestPathMarkup(DijkstraMarkup):
    ''' Given a starting cell and a goal cell, create a Markup that will
        have the shortest path between those two cells marked.
    '''

    def __init__(self, grid, start_cell, goal_cell,
                 path_marker='*', non_path_marker=' '):
        super().__init__(grid, start_cell)
        search_list = []
        search_list.append(start_cell)
        level = 0
        while len(search_list)>0:
            size = len(search_list)
            for i in range(size):
                current_cell = search_list.pop(0)
                self.marks[current_cell] = level
                for cell in current_cell.all_links():
                    if cell not in self.marks:
                        search_list.append(cell)
            level+=1









class LongestPathMarkup(ShortestPathMarkup):
    ''' Create a markup with the longest path in the graph marked.
        Note: Shortest path is dependent upon the start and target cells chosen.
              This markup is the longest path to be found _anywhere_ in the maze.
    '''

    def __init__(self, grid, path_marker='*', non_path_marker=' '):
        start_cell = grid.random_cell()
        dm = DijkstraMarkup(grid, start_cell)
        farthest, _ = dm.farthest_cell()
        dm = DijkstraMarkup(grid, farthest)
        next_farthest, _ = dm.farthest_cell()
        super().__init__(grid, farthest, next_farthest, path_marker, non_path_marker)


class ColorizedMarkup(Markup):
    ''' Markup a maze with various colors.  Each value in the markup is
        an RGB triplet.
    '''


    def __init__(self, grid, channel='R'):
        assert channel in 'RGB'
        super().__init__(grid)
        self.channel = channel

    def colorize_dijkstra(self, start_row=None, start_column=None):
        ''' Provide colors for the maze based on their distance from
            some cell.  By default, from the center cell.
        '''
        if not start_row:
            start_row = self.grid.num_rows // 2
        if not start_column:
            start_column = self.grid.num_columns // 2
        start_cell = self.grid.cell_at(start_row, start_column)
        dm = DijkstraMarkup(self.grid, start_cell)
        self.intensity_colorize(dm)

    def intensity_colorize(self, markup):
        ''' Given a markup of numeric values, colorize based on
            the relationship to the max numeric value.
        '''
        max = markup.max()
        max_value = markup[max]
        for c in self.grid.each_cell():
            cell_value = markup[c]
            intensity = (max_value - cell_value) / max_value
            dark = round(255 * intensity)
            bright = round(127 * intensity) + 128
            if self.channel == 'R':
                self.marks[c] = [bright, dark, dark]
            elif self.channel == 'G':
                self.marks[c] = [dark, bright, dark]
            else:
                self.marks[c] = [dark, dark, bright]


def binary_tree(grid):
    ''' The Binary Tree Algorithm.

        This algorithm works by visiting each cell and randomly choosing
        to link it to the cell to the east or the cell to the north.
        If there is no cell to the east, then always link to the north
        If there is no cell to the north, then always link to the east.
        Except if there are no cells to the north or east (in which case
        don't link it to anything.)
    '''
    for x in range(grid.num_rows):
        for y in range(grid.num_columns):
            nebor = []
            if grid.grid[x][y].north != None:
                nebor.append(grid.grid[x][y].north)
            if grid.grid[x][y].east != None:
                nebor.append(grid.grid[x][y].east)
            if len(nebor) != 0:
                grid.grid[x][y].link(random.choice(nebor), bidirectional=True)


def sidewinder(grid, odds=.5):
    ''' The Sidewinder algorithm.

        Considers each row, one at a time.
        For each row, start with the cell on the west end and an empty list
        (the run).  Append the cell to the run list.
        Choose a random number between 0 and 1.  If it is greater
        than the odds parameter, then add the eastern cell to the run list and
        link it to the current cell.  That eastern cell then becomes the
        current cell.
        If the random number was less than the odds parameter, then you are
        done with the run.  Choose one of the cells in the run and link it to
        the cell to the north.

        Be careful, these instructions don't cover the cases where the row
        is the northernmost one (which will need to be a single, linked run)
        or for cells at the far east (which automatically close the run)
    '''
    assert odds >= 0.0
    assert odds < 1.0
    list = []
    for x in range(grid.num_rows):
        list.clear()
        for y in range(grid.num_columns):
            start_cell = grid.grid[x][y]
            a=random.random()
            if a < odds:
                if start_cell.north:
                    rand = random.randrange(len(list))
                    chosen_cell = list[rand]
                    chosen_cell.link(chosen_cell.north)
                list.clear()
                continue
            else:
                list.append(start_cell)






def aldous_broder(grid):
    ''' The Aldous-Broder algorithm is a random-walk algorithm.

        Start in a random cell.  Choose a random direction.  If the cell
        in that direction has not been visited yet, link the two cells.
        Otherwise, don't link.
        Move to that randomly chosen cell, regardless of whether it was
        linked or not.
        Continue until all cells have been visited.
    '''
    start_cell = grid.random_cell()
    cell_notvisited = []
    for alllist in grid.grid:
        for cell in alllist:
            cell_notvisited.append(cell)

    start_cell.visited = True
    cell_notvisited.remove(start_cell)

    iteration_count = 0
    while len(cell_notvisited) != 0:
        cell_to_link = random.choice(start_cell.neighbors())

        if cell_to_link.visited != True:
            start_cell.link(cell_to_link)
            cell_to_link.visited = True

            cell_notvisited.remove(cell_to_link)

            start_cell = cell_to_link
            iteration_count += 1
            # print(grid.size)
            # print(len(cell_visited))
        else:
            start_cell = cell_to_link
            iteration_count += 1
    print(f'Aldous-Broder executed on a grid of size {grid.size()} in {iteration_count} steps.')


def wilson(grid):

    ''' Wilson's algorithm is a random-walk algorithm.

        1) Choose a random cell.  Mark it visited.
        2) Choose a random unvisited cell (note, this will necessarily not be the
          same cell from step 1).  Perform a "loop-erased" random walk until
          running into a visited cell.  The cells chosen during this random
          walk are not yet marked as visited.
        3) Add the path from step 2 to the maze.  Mark all of the cells as visited.
          Connect all the cells from the path, one to each other, and to the
          already-visited cell it ran into.
        4) Repeat steps 2 and 3 until all cells are visited.

        Great.  But, what is a "loop-erased" random walk?  At each step, one
        random neighbor gets added to the path (which is kept track
        of in order).  Then, check if the neighbor is already in the path.  If
        so, then the entire loop is removed from the path.  So, if the
        path consisted of cells at locations (0,0), (0,1), (0,2), (1,2), (1,3),
        (2,3), (2,2), and the random neighbor is (1,2), then there is a loop.
        Chop the path back to (0,0), (0,1), (0,2), (1,2) and continue

        BTW, it  may be easier to manage a  list of unvisited cells, which
        makes it simpler to choose a random unvisited cell, for instance.
    '''
    cell_notvisited = []
    start_cell = grid.random_cell()
    for alllist in grid.grid:
        for cell in alllist:
            cell_notvisited.append(cell)
    start_cell.visited()
    cell_notvisited.remove(start_cell)

    path = []
    loop_removed =0

    cell_rand = random.choice(cell_notvisited)
    path.append(cell_rand)
    while True:
        cell_n=  random.choice(cell_rand.neighbors())

        if cell_n not in cell_notvisited:
            for i, cell in enumerate(path):
                if path[i] != path[-1]:
                    path[i].link(path[i+1])
                cell_notvisited.remove(path[i])

            path[-1].link(cell_n)
            path.clear()
            if len(cell_notvisited) == 0 :
                break
            cell_rand = random.choice(cell_notvisited)
            path.append(cell_rand)

        elif cell_n in path:
            loop_removed+=1
            while path[-1] != cell_n:
                path.pop()
            cell_rand = path[-1]

        else:
            path.append(cell_n)
            cell_rand = cell_n
    print(f'Wilson executed with the grid with size {grid.size()} with first cell {cell_rand}', end=' ')
    print(f' random cells chosen and {loop_removed} loops removed')







def recursive_backtracker(grid, start_cell=None):
    ''' Recursive Backtracker is a high-river maze algorithm.

        1) if start_cell is None, choose a random cell for the start
        2) Examine all neighbors and make a list of those that have not been visited
           Note: you can tell it hasn't been visited if it is not linked to any cell
        3) Randomly choose one of the cells from this list.  Link to and move to that
           neighbor
        3a) If there are no neighbors in the list, then you must backtrack to the last
            cell you visited and repeat.

        Suggestion: Use an explicit stack.  You can write this implicitly (in fact,
        the code will be quite short), but for large mazes you will be making lots of
        function calls and you risk running out of stack space.
    '''
    pass
