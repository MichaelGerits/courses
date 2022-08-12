import math

class Variable():

    def __init__(self, row, col):
        """Create a new variable with coordinates and group."""
        #get the coordinates
        self.row = row
        self.col = col

        #define group (block of nine) 0 -> 8
        Grow = math.floor(row/3)
        Gcol = math.floor(col/3)
        self.group = int(Grow * 3 + Gcol)


    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (
            (self.row == other.row) and
            (self.col == other.col)
        )

    #represents what you get if you print the variable
    def __str__(self):
        return f"(Row:{self.row}, Col:{self.col}, G:{self.group})"
    #represents the variable as for example a key in a dict
    def __repr__(self):
        return f"Variable({self.row}, {self.col}, {self.group})"


class Sudoku():

    def __init__(self, structure_file):

        # Determine structure of sudoku

        #reads the file
        with open(structure_file) as f:
            rows = f.read().splitlines()
            #(not 9*9 because of the lines, the actual dimensions of the txt files)
            #in order to allow lines and such
            self.height = len(rows)
            self.width = max(len(line) for line in rows)

            #saves the structure into RAM
            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    #if it's already filled in appends the num, if it's yet to be filled in, appends "_"
                    #ignores the lines to make the actual problem easier
                    if j >= len(rows[i]):
                        continue
                    elif rows[i][j] == "#":
                        row.append('_')
                    elif rows[i][j].isnumeric():
                        row.append(rows[i][j])
                if len(row) != 0:
                    self.structure.append(row)

        #resets the dimensions now that the lines are gone
        self.height = 9
        self.width = 9

        # Determine variable set
        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):
                self.variables.add(Variable(row=i, col=j))

        # Compute groups as sets (0 -> 8)
        self.groups = [set(), set(), set(), set(), set(), set(), set(), set(), set()]
        for var in self.variables:
            self.groups[(var.group)].add(var)

    def get_groupN(self, var):
        """Given a variable, return set of the other variables in it's group."""
        neighbours = self.groups[var.group].copy()
        neighbours.discard(var)
        return neighbours

    def get_rowN(self, var):
        """Given a variable, return set of the other variables in it's row."""
        neighbours = set()
        for other_var in self.variables:
            if other_var.row == var.row and other_var != var:
                neighbours.add(other_var)
        return neighbours

    def get_colN(self, var):
        """Given a variable, return set of the other variables in it's collumn."""
        neighbours = set()
        for other_var in self.variables:
            if other_var.col == var.col and other_var != var:
                neighbours.add(other_var)
        return neighbours

    def neighbours(self, var):
        """returns a set of variables which can not have the sam value as var"""
        neighbours = self.get_groupN(var).union(self.get_rowN(var), self.get_colN(var))
        return neighbours
