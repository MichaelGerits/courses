Hello, this is my last project for CS50, kind-off overdue, but hey....i did it :3.

### *I firstly want to mention that i did write most i not all of this program, be it through the original implementation of the crossword puzzle or the adaptation to this project, i have worked on every part of it and understand every aspect of it.*


Let's start with what this project is. I made a Python ***sudoku solver*** usign a constraint satisfction problem,
that's it! (because i'm to lazy to do them myself).

I've wanted to make a Sudoku solver for a while now, even before i started with CS50.
Thinking back my ideas then were destined to fail.
However, As i worked through CS50's course for artificial intelligence
(because i procrastinated this project) i learned about constraint satisfaction problems "CSP's".
There I worked on a crossword generator, a program that i would reference heavily on for this project.

For the rest of that course i wondered if my pet project would finally be doable, but i layed it aside
as i wanted to finish that course first and figured that my laptop didn't have the computational power
( because of the amount of variables).
Then came the deadline i layed upon myself and i did eventually just try it, because i had no better option.

# HOW IT WORKS:
on a high level there are two .py files; One defines what a variable is and the Sudoku itself,
the other defines the solver and houses the ac3-backtrack algorithm to solve it.
There is also a structure folder, which houses a template and three different sudokus i've found online and checked

**!!The Sudoku's rows, collumns and groups are zero indexed!!**

## - The Variable() Class
defines it's position (row, collumn) and which group it is in.
It calculates it's group *with a mathematical* function using it's position, which was a nice treat for me.
Other than that it jut has some other functions for usage and debugging.

## - The Sudoku() class
this class is mainly used to intrpret and define the Sudoku game. It first reads the structure file line by line, character by character. It discards the dividing lines for simplicity in the algorithm. It the defines the proper dimensions and initiates all the variables in the structure.

it then defines a list of sets `self.groups`, wich will come in usefull in a later `neighbours(var)` function.
Lastly it defines four functions, with the eventual purpose of, (*given a variable*), outputting all the other variables which cannot hold the same value.

# SudokuSolver():
This is by far the largest class of all and makes up the biggest part of solve.py. Firstly it reads the structure of `Sudoku()`. and defines a domain dict with each variable in it. **`self.domains`** is a dictionary which links each variable to a list of possible values *(1 -> 9)*.
The values that are known are added to a list as well with length of 1.
**we will talk about `game_grid(assignment)` and `print(assignment, prev_assignment=None)` later.**

### - `solve()`:
the solve runs the entire solving algorithm and eventually returns a finished assignment to `print(assignment, prev_assignment=None)`.

### - `fill_ass(domains)`:
While the name is pretty funny, this function does a very simple task. It assigns the variable of which we technically already know the value, to that alue in a `prev_assignment` dict, which will be the basis for the rest of our algorithm.

### - `revise(x, y)`:
this function is mainly a part of the ac3 algorithm, but I'll still explain it here. In short, it makes variables **arc-consistent** this means that for each value in X's domain, there is a possible value in Y's domain without causiing conflict. If that's not the case, it removes those values from X's domain.

### - `ac3(arcs=None)`:
this is a well known algorithm that makes an entire *CSP* arc-consistent.
For this it goes by each var and gets it's neighbours with the function defined in `Sudoku()` with these it makes arcs (links between variables) ***(X, Y)***. After which it revises each arc creating new ones in between to make sure tht deleted values don't influence the consitency. It does this untill all arcs are revised.
*It has an optional arcs argument to make inferences later on*

### - `backtrack(assignment)`:
once the ac3 algorithm has decreased the size of some domains the backtrack fills in a definitive assignement, using the partial one we got from `fill_ass(domains)`. *This is a recursive algorithm* which selects an unnasigned variable and assings a certain value to it.
(**we'll explore that later on**).

After the assignment it checks if the current assignement is consistent (the Sudoku's currently correct). if that's the case it inferrs the other domains with `self.ac3(arcs)`. and then recursively calls itself for the next variable, effectively making a step towards completion.
If the new assignment is not consistent, it *backtracks*, effectively going backwards in the recursive stack and choosing another vlue in the previous value, if that doesn't work, it goes back another iteration.

What it's basically doing is choosing *"random"* values untill it encounters a mistake then follows its tracks to the eventual point of error. It keeps doing this untill the assignment is complete, which it then returns to be printed out.

### - `select_unassigned_variable(assignment)`:
this is the function that `backtrack(assignment)` uses to select the next variable to assign, from the available variables it chooses the one with the smallest domain, if there is a tie in that departement, it prioritizes the variable with the least amount of unnassigned variables. This way we'll have less chance to make an error which we have to return to way later on.

### - `order_domain_values(var, assignment)`:
another way to decrease error is to choose the best values. This function orders the domain of var in the order of the least impact.
This means that our preferred value rules out the least amount of values for its neighbours.

### together these functions solve our CSP, now as promised, back to grid and print.

# Visualising the answer:
### - `game_grid(assignment)`:
Now that we have a dictionary of variables and thei values, we need to print those values out. Before that though, we would like these values to be in a more.....printable medium.
This is what this function does. It takes each value and puts it on the right place of a 2 dimentional array.

### - `print(assignment, prev_assignment=None)`:
this is the function that will visulize our sudoku. It has the beginning state optional so that i could see the in between states during `backtrack(assignment)` when i needed to debug. The functionality of it is quite simple, as it converts the assignment with `game_grid(assignment)` and then prints them accordingly. It also takes care of putting the lines back to make it a bit more overseeable.

It prints the original and final state for fun comparison :3.

## That was it. Thank you for checking out my little thing. I really enjoyed CS50 and will certaintly continue with thispath of learning.