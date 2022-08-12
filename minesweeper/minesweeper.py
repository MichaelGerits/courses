import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #if the amount of cells is equal to the mine count
        if self.count == len(self.cells):
            return self.cells.copy()
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #if there are no mines in the sentence
        if self.count == 0:
            return self.cells.copy()
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #removes the cell and 1 from the mine count
        try:
            self.cells.remove(cell)
        except KeyError:
            pass
        else:
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #removes the cell while keeping the mine count the same 
        try:
            self.cells.remove(cell)
        except KeyError:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        #executes the markmine func of the sentence on each sentence in knowledge
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        #adds cell to the mines set
        self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        #executes the marksafe func of the sentence on each sentence in knowledge
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        #adds cell to the safes set
        self.safes.add(cell)

    def nearby_cells(self, cell): #works
        """
        returns a tuple with the neighbouring cells which we don't know the state of
        and the amount that we have to offset count with when e create a new sentence
        """
        count = 0
        exploreBottom = 0
        exploreLeft = 0
        exploreRight = 0
        exploreTop = 0
        #checks if it hits any borders
        if cell[0] > 0:
            exploreTop = 1
        if cell[0] < self.height - 1:
            exploreBottom = 1
        if cell[1] < self.width - 1:
            exploreRight = 1
        if cell[1] > 0:
            exploreLeft = 1

        nearbyCells = set()
        #goes through the neighbouring valid rows
        for i in range(cell[0] - exploreTop, cell[0] + (1 + exploreBottom)):
            for j in range(cell[1] - exploreLeft, cell[1] + (exploreRight + 1)):
                #ignores the cells that we've already made and we already know are safe
                if (i, j) == cell or (i, j) in self.moves_made or (i,j) in self.safes:
                    continue
                #ignores the cells that we know are mines and handles the count accordingly
                elif (i,j) in self.mines:
                    count += 1
                    continue
                nearbyCells.add((i, j))
        #returns the new cells and the amount that we have to offput the count value by
        return (nearbyCells, count)


    def update_knowledge(self):
        """
        keeps editing the knowledge to learn more states of the cells
        untill no more edits can b made wihout subset inferring or new knowledge
        """
        #repeats the function untill no more edits can be made
        while True:
            edits = 0
            emptySentences = []
            #goes through each sentence in knowledge
            for i in range(len(self.knowledge)):
                sentence = self.knowledge[i]
                #gets the known cells in the sentence
                safe_cells = sentence.known_safes()
                mine_cells = sentence.known_mines()
                #if there are any safes in the sentence it handles them accordingly
                if safe_cells:
                    for cell in safe_cells:
                        self.mark_safe(cell)
                        edits += 1
                #if there are any mines in the sentence it handles them accordingly
                if mine_cells:
                    for cell in mine_cells:
                        self.mark_mine(cell)
                        edits += 1
                #checks for empty sentences
                if sentence.cells == set():
                    emptySentences.append(sentence)
                    edits += 1
            #deletes the empty sentences in knowledge
            for i in range(len(emptySentences)):
                self.knowledge.remove(emptySentences[i])
            #ends the function if no more edits have been made
            if edits == 0:
                break
    
    def inferr_knowledge(self):
        """
        returns the amount of inferrences we've made this pass
        uses the subset method to create new sentences 
        which can be used in update_knowledge
        """
        #checks if we can inferr any two sentences
        oldKnowledge = self.knowledge.copy()
        inferred = 0
        for sentence in oldKnowledge:
            for subSentence in oldKnowledge:
                #checks if it's a subset of the other sentence
                if subSentence.cells != sentence.cells and sentence.cells.issuperset(subSentence.cells):
                    inferredSentence = Sentence(cells=(sentence.cells.difference(subSentence.cells)), count=(sentence.count - subSentence.count))
                    #if it's a valid sentence that we don't posses yet it adds it to knowledge
                    if inferredSentence.count >= 0 and inferredSentence not in self.knowledge:
                        inferred += 1
                        self.knowledge.append(inferredSentence)
        #returns the amount of subset inferrences that it's made in this pass
        return inferred

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1:
        self.moves_made.add(cell)
        #2:
        #mark_safe of the AI, not a sentence
        self.mark_safe(cell)
        #3:
        nearbyCells = self.nearby_cells(cell)[0]
        countAdjust = self.nearby_cells(cell)[1]
        sentence = Sentence(cells=nearbyCells, count=count - countAdjust)
        if sentence not in self.knowledge and len(sentence.cells) > 0:
            self.knowledge.append(sentence)
        #repeats untill knowledge can't be improved anymore
        while True:
            #4:
            self.update_knowledge()
            #5:
            if self.inferr_knowledge() == 0:
                break
        #run this func again......because i'm paranoid, no other reason
        self.update_knowledge()
        print("possible moves:", self.safes.difference(self.moves_made))
        print("known mines:", self.mines)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safeMoves = self.safes.difference(self.moves_made).copy()
        if safeMoves:
            return safeMoves.pop()
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = set()
        for row in range(self.height):
            for collumn in range(self.width):
                cell = (row, collumn)
                if cell not in self.moves_made and cell not in self.mines:
                    moves.add(cell)
        moves = list(moves)
        if len(moves) == 0:
            return None
        return random.choice(moves)
