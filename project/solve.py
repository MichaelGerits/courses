from copy import deepcopy
import copy
import random
import sys

from Sudoku import *


class SudokuSolver():

    def __init__(self, sudoku):
        """
        Create new CSP crossword generate and assigns domains.
        """
        #adds the domains of each variable, including the known ones
        self.sudoku = sudoku
        self.domains = {}
        for var in self.sudoku.variables:
            #if the value is already known it adds it to domain as a single value
            if self.sudoku.structure[var.row][var.col].isnumeric():
                self.domains[var] = [int(self.sudoku.structure[var.row][var.col])]
            else:
                self.domains[var] = [1,2,3,4,5,6,7,8,9]

    def game_grid(self, assignment):
        """
         transforms the assignment of variables into a 2D array of values.
        """
        #initializes the array
        values = [
            [None for _ in range(self.sudoku.width)]
            for _ in range(self.sudoku.height)
        ]
        for var, val in assignment.items():
            values[var.row][var.col] = val
        return values

    def print(self, assignment, prev_assignment=None):
        """
        Print before and after crossword assignment to the terminal.
        gives the option to print in between the algorithm.
        """
        for list in [prev_assignment, assignment]:
            if list == None:
                continue
            print()
            values = self.game_grid(list)
            for i in range(self.sudoku.height):
                #adds the horizontal lines back
                if i%3 == 0 and i != 0:
                    print("---+---+---")
                for j in range(self.sudoku.width):
                    #adds the vertical lines back
                    if j%3 == 0 and j != 0:
                        print("|", end="")
                    #if the square exists it either adds the value, or "_" if it's empty
                    if self.sudoku.structure[i][j]:
                        print(values[i][j] or "_", end="")
                print()
        print()


    def solve(self):
        """
         arc consistency, and then solve the CSP.
        """
        #initiates the before state which will later also be used for backtrack
        prev_assignment = self.fill_ass(self.domains)

        self.ac3()
        print("--------------------\nac3 done\n-------------------")
        assignment =  self.backtrack(copy.deepcopy(prev_assignment))
        return (prev_assignment, assignment)

    def fill_ass(self, domains):
        """fills in the assignment with the values we already know"""
        prev_assignment = {}
        for var in self.sudoku.variables:
            if len(domains[var]) == 1:
                prev_assignment[var] = domains[var][0]
        return prev_assignment

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #goes by each value of each domain
        for x_val in self.domains[x].copy():
            Xoption = False
            for y_val in self.domains[y]:
                Xoption = True
                #each value is an option untill proven not to be
                #this way when it's unable to prove that there's no possible other values (we have found an option)
                #it can break out of the y domain loop to save time
                if x_val == y_val:
                    Xoption = False
                else:
                    break
            #if no option is proved viable in y's domain
            if Xoption == False:
                self.domains[x].remove(x_val)
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
            for var in self.sudoku.variables:
                neighbours = self.sudoku.neighbours(var)
                for neighbour in neighbours:
                    arcs.append((var, neighbour))

        #goes by each arc and revises them
        while len(arcs) != 0:
            (x,y) = arcs.pop()
            if self.revise(x, y):
                #if there is no possible solution
                if len(self.domains[x]) == 0:
                    return False
                #since we changed a domain, we add more arcs to see if we have possibly ruined other options
                neighbours = self.sudoku.neighbours(x)
                for neighbour in neighbours:
                    if neighbour != y:
                        arcs.append((neighbour, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each variable);
        return False otherwise.
        """
        if len(self.sudoku.variables) == len(assignment):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent
        (i.e., values fit in the crossword without conflicting and none of the domains are empty);
        return False otherwise.
        """
        for var in self.sudoku.variables.intersection(assignment):
            if len(self.domains[var]) == 0:
                return False
            neighbours = self.sudoku.neighbours(var).intersection(assignment)
            for neighbour in neighbours:
                if assignment[var] == assignment[neighbour]:
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
        neighbours = self.sudoku.neighbours(var).difference(assignment)

        #count how many times each value in X's domain clashes with the values of its neighbours' domains
        order = {}
        for value in self.domains[var]:
            count = 0
            for neighbour in neighbours:
                for nVal in self.domains[neighbour]:
                    if value == nVal:
                        count += 1
            order[value] = count

        #orders the value  in X's domain in ascending order
        order_sort= list(sorted(order.keys(), key=lambda key: order[key]))

        return order_sort

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        vars_left = self.sudoku.variables.difference(assignment)
        #sorts the variables based on length of the domain in ascending order and then on the amount of neighbors in descending order, thus the "-"
        sorted_vars_left = list(sorted(vars_left, key=lambda var: (len(self.domains[var]), -len(self.sudoku.neighbours(var)))))
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
                self.domains[var] = [value]
                #inferrs from newly aquired knowledge
                arcs = list()
                for neighbour in self.sudoku.neighbours(var):
                    arcs.append((neighbour, var))
                self.ac3(arcs)
                #continues backtrack
                result = self.backtrack(assignment)
                if result != None:
                    return result
            del assignment[var]
            self.domains = pre_assignment_domains
        return None

def main():

    # Check usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python solve.py structures/file")

    # Parse command-line arguments
    structure = sys.argv[1]

    # Generate sudoku
    sudoku = Sudoku(structure)
    solver = SudokuSolver(sudoku)
    #solve sudoku
    prev_assignment, assignment = solver.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        solver.print(assignment, prev_assignment)


if __name__ == "__main__":
    main()
