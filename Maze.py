#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''
import random
import math

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
        self.east  = None
        self.west  = None
        
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
        if cell in self.links:
            return True
        return False
        
    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        list1 = []
        for cell in self.links:
            list1.append(cell)
        return list1
        
    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        return len(self.links)
        
    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        list1 = []
        if self.north != None:
            list1.append(self.north)
        if self.south != None:
            list1.append(self.south)
        if self.east != None:
            list1.append(self.east)
        if self.west != None:
            list1.append(self.west)
        return list1
                
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
        grid = [[Cell(r, c) for c in range(self.num_columns)] for r in range(self.num_rows)]
        return grid
            
    def connect_cells(self):
        ''' Now that all the cells have been created, connect them to 
            each other. 
        '''
        for c in range(self.num_columns):
            self.grid[0][c].south = self.grid[1][c]
            for r in range(1, self.num_rows-1):
                self.grid[r][c].south = self.grid[r+1][c]
                self.grid[r][c].north = self.grid[r-1][c]
            self.grid[self.num_rows-1][c].north = self.grid[self.num_rows-2][c]
        for r in range(self.num_rows):
            self.grid[r][0].east = self.grid[r][1]
            for c in range(1, self.num_columns-1):
                self.grid[r][c].east = self.grid[r][c+1]
                self.grid[r][c].west = self.grid[r][c-1]
            self.grid[r][self.num_columns-1].west = self.grid[r][self.num_columns-2]
        
    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        return self.grid[row][column]
        
    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        l = []
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                cur = self.grid[r][c]
                if len(cur.links) == 1:
                    l.append(cur)
        return l
                            
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
        return self.grid[math.floor(random.uniform(0, self.num_rows))][math.floor(random.uniform(0, self.num_columns))]
        
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
            self.marks[cell]=value
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
        self.marks[root_cell] = 0
        frontier = []
        frontier.append(root_cell)
        while frontier != []:
            cur = frontier.pop(0)
            for neighbor in cur.all_links():
                if neighbor not in self.marks:
                    self.marks[neighbor] = self.marks[cur] + 1
                    frontier.append(neighbor)

    def farthest_cell(self):
        ''' Find the cell with the largest markup value, which will
            be the one farthest away from the root_call.
            
            Returns: Tuple of (cell, distance)
        '''
        return (self.max(), self.marks[self.max()])

class ShortestPathMarkup(DijkstraMarkup):
    ''' Given a starting cell and a goal cell, create a Markup that will
        have the shortest path between those two cells marked.  
    '''

    def __init__(self, grid, start_cell, goal_cell, 
                 path_marker='*', non_path_marker=' '):
        super().__init__(grid, start_cell)
        mark_cells = []
        cur = goal_cell
        mark_cells.append(cur)
        while cur != start_cell:
            for neighbor in cur.all_links():
                if self.marks[neighbor] < self.marks[cur]:
                    cur = neighbor
                    mark_cells.append(cur)
                    break
        for c in range(self.grid.num_columns):
            for r in range(self.grid.num_rows):
                if self.grid.grid[r][c] in mark_cells:
                    self.marks[self.grid.grid[r][c]] = path_marker
                else:
                    self.marks[self.grid.grid[r][c]] = non_path_marker

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
        
    def colorize_dijkstra(self, start_row = None, start_column = None):
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
            dark   = round(255 * intensity)
            bright = round(127 * intensity) + 128
            if self.channel == 'R':
                self.marks[c] = [bright, dark, dark]
            elif self.channel == 'G':
                self.marks[c] = [dark, bright, dark]
            else:
                self.marks[c] = [dark, dark, bright]   

class FlagAndPlayersMarkup(Markup):
    ''' Markup a maze with Flag and Players Positions
    '''
    def __init__(self, grid, flag_marker='f', player0_marker='p0', player1_marker='p1', props_marker='p', props_num=6, water_marker='w', non_marker=' '):
        super().__init__(grid)
        flag = grid.random_cell()
        dm = DijkstraMarkup(self.grid, flag)
        max_mark = dm.farthest_cell()[1]
        possible_marks = []
        for mark in range(1, max_mark+1):
            possible_marks.append(mark)
        possible_player = []
        while len(possible_player) < 2:
            possible_player = []
            rand_dist = possible_marks.pop(random.randint(0, len(possible_marks)-1))
            for cell in dm.marks:
                if dm.marks[cell] == rand_dist:
                    possible_player.append(cell)
        player0 = possible_player.pop(random.randint(0, len(possible_player)-1))
        player1 = possible_player.pop(random.randint(0, len(possible_player)-1))
        props = []
        non_props = [flag, player0, player1]
        while len(props) < props_num:
            cur = self.grid.grid[random.randint(0, self.grid.num_rows-1)][random.randint(0, self.grid.num_columns-1)]
            if cur not in non_props:
                props.append(cur)
        for c in range(self.grid.num_columns):
            for r in range(self.grid.num_rows):
                dm.marks[self.grid.grid[r][c]] = non_marker
        dm.marks[flag] = flag_marker
        dm.marks[player0] = player0_marker
        dm.marks[player1] = player1_marker
        for prop in props:
            dm.marks[prop] = props_marker
        self.marks = dm.marks
                                       
def binary_tree(grid):
    ''' The Binary Tree Algorithm.
      
        This algorithm works by visiting each cell and randomly choosing
        to link it to the cell to the east or the cell to the north.
        If there is no cell to the east, then always link to the north
        If there is no cell to the north, then always link to the east.
        Except if there are no cells to the north or east (in which case
        don't link it to anything.)
    '''
    for r in range(grid.num_rows):
            for c in range(grid.num_columns):
                cur = grid.grid[r][c]
                if cur.east != None and cur.south != None:
                    if math.floor(random.uniform(0, 2)) == 0:
                        cur.link(cur.east)
                    else:
                        cur.link(cur.south)
                elif cur.east != None:
                    cur.link(cur.east)
                elif cur.south != None:
                    cur.link(cur.south)

            
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
    for c in range(grid.num_columns-1):
        grid.grid[0][c].link(grid.grid[0][c+1])
    for r in range(1, grid.num_rows):
        cur = 0
        while cur < grid.num_columns:
            run_list = []
            run_list.append(grid.grid[r][cur])
            while random.uniform(0, 1) > odds and cur < grid.num_columns - 1:
                cur += 1
                run_list.append(grid.grid[r][cur])
            for num in range(len(run_list)-1):
                run_list[num].link(run_list[num+1])
            randnum = random.randint(0, len(run_list)-1)
            run_list[randnum].link(run_list[randnum].north)
            cur += 1
                
def aldous_broder(grid):
    ''' The Aldous-Broder algorithm is a random-walk algorithm.
    
        Start in a random cell.  Choose a random direction.  If the cell
        in that direction has not been visited yet, link the two cells.
        Otherwise, don't link.
        Move to that randomly chosen cell, regardless of whether it was
        linked or not.
        Continue until all cells have been visited.
    '''
    visited = []
    iteration_count = 0
    cur = grid.random_cell()
    visited.append(cur)
    while len(visited) < grid.size():
        randNum = random.randint(0, 3)
        if randNum == 0:
            target = cur.north
        if randNum == 1:
            target = cur.south
        if randNum == 2:
            target = cur.east
        if randNum == 3:
            target = cur.west
        if target != None:
            if target not in visited:
                cur.link(target)
                visited.append(target)
            cur = target
            iteration_count += 1
    
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
    unvisited = []
    random_choices = 0
    loops_removed = 0
    for c in range(grid.num_columns):
            for r in range(grid.num_rows):
                unvisited.append(grid.grid[r][c])
    unvisited.pop(random.randint(0, len(unvisited)-1))
    random_choices = 1
    while unvisited != []:
        path = []
        cur = unvisited[random.randint(0, len(unvisited)-1)]
        random_choices += 1
        path.append(cur)
        end = False
        while not end:
            randNum = random.randint(0, 3)
            random_choices += 1
            if randNum == 0:
                target = cur.north
            if randNum == 1:
                target = cur.south
            if randNum == 2:
                target = cur.east
            if randNum == 3:
                target = cur.west

            if target != None:
                # reaches visited cell, this is end
                if target not in unvisited: 
                    end = True
                    for cell in path:
                        unvisited.remove(cell)
                    if len(path) > 1:
                        for cellIndex in range(len(path)-1):
                            path[cellIndex].link(path[cellIndex+1])
                    path[-1].link(target)
                # reaches unvisited cell
                else: 
                    # if cell in path, here is loop, erase loop
                    if target in path: 
                        loopIndex = path.index(target)
                        loops_removed += 1
                        # if start cell in loop, this is end
                        if loopIndex == 0: 
                            end = True
                        # if start cell not in loop, erase and continue
                        else:
                            path = path[:loopIndex]
                            cur = path[-1]
                    # if cell not in path, great, add it to path
                    else: 
                        cur = target
                        path.append(cur)   

    print(f'Wilson executed on a grid of size {grid.size()} with {random_choices}', end='')
    print(f' random cells choosen and {loops_removed} loops removed')
            
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
    visited = []
    stack = []
    if start_cell != None:
        cur = start_cell
    else:
        cur = grid.random_cell()
    visited.append(cur)
    stack.append(cur)
    recursive_backtracker_runner(grid, cur, visited, stack)

def recursive_backtracker_runner(grid, cur, visited, stack):
    neighbor = []
    if cur.north != None and cur.north not in visited:
        neighbor.append(cur.north)
    if cur.south != None and cur.south not in visited:
        neighbor.append(cur.south)
    if cur.east != None and cur.east not in visited:
        neighbor.append(cur.east)
    if cur.west != None and cur.west not in visited:
        neighbor.append(cur.west)
    if neighbor != []:
        target = neighbor[random.randint(0, len(neighbor)-1)]
        cur.link(target)
        visited.append(target)
        if len(visited) == grid.size():
            return
        stack.append(target)
        recursive_backtracker_runner(grid, target, visited, stack)
    else:
        back = stack.pop()
        recursive_backtracker_runner(grid, back, visited, stack)

def ABWilson(grid, change=0.5):
    unvisited = []
    iteration_count = 0
    for c in range(grid.num_columns):
            for r in range(grid.num_rows):
                unvisited.append(grid.grid[r][c])
    cur = unvisited.pop(random.randint(0, len(unvisited)-1))
    while len(unvisited) > grid.size() * change:
        randNum = random.randint(0, 3)
        if randNum == 0:
            target = cur.north
        if randNum == 1:
            target = cur.south
        if randNum == 2:
            target = cur.east
        if randNum == 3:
            target = cur.west
        if target != None:
            if target in unvisited:
                cur.link(target)
                unvisited.remove(target)
            cur = target
            iteration_count += 1
    while unvisited != []:
        path = []
        cur = unvisited[random.randint(0, len(unvisited)-1)]
        iteration_count += 1
        path.append(cur)
        end = False
        while not end:
            randNum = random.randint(0, 3)
            iteration_count += 1
            if randNum == 0:
                target = cur.north
            if randNum == 1:
                target = cur.south
            if randNum == 2:
                target = cur.east
            if randNum == 3:
                target = cur.west

            if target != None:
                # reaches visited cell, this is end
                if target not in unvisited: 
                    end = True
                    for cell in path:
                        unvisited.remove(cell)
                    if len(path) > 1:
                        for cellIndex in range(len(path)-1):
                            path[cellIndex].link(path[cellIndex+1])
                    path[-1].link(target)
                # reaches unvisited cell
                else: 
                    # if cell in path, here is loop, erase loop
                    if target in path: 
                        loopIndex = path.index(target)
                        # if start cell in loop, this is end
                        if loopIndex == 0: 
                            end = True
                        # if start cell not in loop, erase and continue
                        else:
                            path = path[:loopIndex]
                            cur = path[-1]
                    # if cell not in path, great, add it to path
                    else: 
                        cur = target
                        path.append(cur)