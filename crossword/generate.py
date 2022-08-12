from copy import deepcopy
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        print("node consitencey done")
        self.ac3()
        print("ac3 done")
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return revised

        for x_word in self.domains[x].copy():
            option = False
            for y_word in self.domains[y]:
                option = True
                #each word is an option untill proven not to be
                #this way when it's unable to prove that it's not a word (we have found an option)
                #it can break out of the y domain loop to save time
                if x_word[overlap[0]] != y_word[overlap[1]]:
                    option = False
                if option == True:
                    break
            #if no option is proved viable in y's domain
            if option == False:
                self.domains[x].remove(x_word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #makes the initial arcs list
        if arcs == None:
            arcs = list()
            for var in self.crossword.variables:
                neighbours = self.crossword.neighbors(var)
                for neighbour in neighbours:
                    arcs.append((var, neighbour))

        while len(arcs) != 0:
            (x,y) = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                neighbours = self.crossword.neighbors(x)
                for neighbour in neighbours:
                    if neighbour != y:
                        arcs.append((neighbour, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.crossword.variables) == len(assignment):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        def duplicates(assignement):
            """
            reverses the dict (values become keys and other way round) if we then have multiple var values
            for one word key, we know that there are duplicates.
            returns true if it has found any, false if none
            """
            rev_dict = {}
            for key, value in assignement.items():
                #adds the variable to a list with the values as keys
                if value not in rev_dict:
                    rev_dict[value] = [key]
                else:
                    rev_dict[value].append(key)

            #if a value key is linked to multiple variables, we know the original dict has duplicate words.
            for key in rev_dict:
                if len(rev_dict[key]) > 1:
                    return True
            return False

        def clashes(x, y, assignment):
            """
            returns true if x and y have a different value for the overlap between the two
            """
            overlap = self.crossword.overlaps[x, y]
            x_word = assignment[x]
            y_word = assignment[y]
            if x_word[overlap[0]] != y_word[overlap[1]]:
                return True
            return False


        for var in assignment:
            #check the length
            if len(assignment[var]) != var.length:
                return False
            #check if the assigned neighbours clash
            for neighbour in self.crossword.neighbors(var).intersection(assignment):
                if clashes(var, neighbour, assignment):
                    return False
        #check if there are duplicates
        if duplicates(assignment):
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #gets all the neighbours who aren't assigned yet
        neighbours = self.crossword.neighbors(var).difference(assignment)
        
        #count how many times each value in X's domain clashes with the values of its neighbours
        order = {}
        for value in self.domains[var]:
            count = 0
            for neighbour in neighbours:
                overlap = self.crossword.overlaps[var, neighbour]
                for nVal in self.domains[neighbour]:
                    if value[overlap[0]] == nVal[overlap[1]]:
                        count += 1
            order[value] = count
        
        #orders the value  in X's domain in ascending order
        order_sort= dict(sorted(order.items(), key=lambda item: item[1]))

        return set(order_sort.keys())
        #raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        vars_left = self.crossword.variables.difference(assignment)
        #sorts the variables based on length of the domain in ascending order and then on the amount of neighbors in descending order, thus the "-" 
        sorted_vars_left = sorted(vars_left, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))
        if sorted_vars_left: 
            return sorted_vars_left[0] 
        else: 
           return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        pre_assignment_domains = deepcopy(self.domains)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                # Update variable domain to be assigned value
                self.domains[var] = {value}
                #inferrs from newly aquired knowledge
                arcs = list()
                for neighbour in self.crossword.neighbors(var):
                    arcs.append((neighbour, var))
                self.ac3(arcs)
                #continues backtrack
                result = self.backtrack(assignment)
                if result != None:
                    return result
            del assignment[var]
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
