import random
import numpy as np

def main(): # test
    n = 10
    population = 12  # Population size has to be n >= 6. Upper bound is determined by how fast your laptop is.
    mutateProbability = 0.25

    if n < 4:
        print("N must be greater than 3")
        exit()
    elif population < 6:
        print("Population size must be greater than or equal to 6")
        exit()

    board = nQueenCalculator(n, population, mutateProbability)
    printNQueenChessBoardWithLines(board)

'''
Parameters:
n - The size of the board and the amount of queens to be displayed on the board
population - population size

Output:
Returns a single solution of the N-Queen problem as a list representing a chess board. (Wraparound function)
'''
def nQueenCalculator(n, population, mutateProbability):
    # Initialize population with random solutions h
    boards = []
    for i in range(population):
        boards.append(generateRandomBoard(n))

    # Until the solution is found, create successive generations
    solutionFound = False
    numGen = 0
    
    while not solutionFound:
        scores = []
        pool = [] # Pool of top pool_size solutions
        bestFit1 = 0 # Index of current best fitting board
        bestFit2 = 0 # Index of second best fitting board
        
        # Evaluate fitness of each solution in the population
        for i in range(len(boards)):
            score, solutionFound = fitness(n, boards[i])
            scores.append(score)

            # Return solution if found, otherwise select 2 best fit solutions as parents
            if solutionFound:
                print("Number of Generations: ", numGen)
                return boards[i]
            elif score < scores[bestFit1]:
                bestFit1 = i
            elif score < scores[bestFit2]:
                bestFit2 = i
        
        # Sort solutions from best to worst, pair up parents for next generation
        pool = np.argsort(scores)
        
        newGen = []
        for i in range (0,population-2,2):
            p1 = pool[i]
            p2 = pool[i+1]
            
            # Crossover & Mutation
            c1, c2 = twoPointCrossover(n, boards[p1].copy(), boards[p2].copy())
            if random.random() <= mutateProbability:
                c1 = mutateBoard(n, c1)
                c2 = mutateBoard(n, c2)

            # Add children to new generation
            newGen.append(c1)
            newGen.append(c2)
            
        # Replace boards with worst fitness scores with boards with best fitness scores
        if population % 2 == 0:
            newGen.append(boards[pool[0]])
            newGen.append(boards[pool[1]])
        else:
            newGen.append(boards[pool[0]])
            newGen.append(boards[pool[1]])
            newGen.append(boards[pool[2]])
        
        boards = newGen
        numGen += 1

    return 

"""
Helper function to implement 2-point crossover of 2 parents

Parameters:
p1 - 1st chosen parent
p2 - 2nd chosen parent

Return:
c1 - 1st child generated from parents. List representation of the queens on a chess board.
c2 - 2nd child generated from parents. List representation of the queens on a chess board.

Example:
c[2] = 5 - A queen is present at column 2 and row 5
"""
def twoPointCrossover(n, p1, p2):
    lcp = random.randint(1, n-2)     # left Cross Point
    rcp = random.randint(1, n-2)     # right Cross Point
    difference = max(lcp, rcp) - min(lcp, rcp)

    if n < 6:
        # Edge case: n is very small, random int generation has high chance of collision
        lcp = 1
        rcp = n-2
    else:
        while (difference < 2):
            lcp = random.randint(1, n-2)     # left Cross Point
            rcp = random.randint(1, n-2)     # right Cross Point
            difference = max(lcp, rcp) - min(lcp, rcp)
        
    # Add a random right shift to make sure that n-2 can also be considered in the two Point Crossover 
    ranRightShift = random.randint(0, 1)  
    lcp += ranRightShift
    rcp += ranRightShift

    # Makes sure lcp is less than rcp as lcp has to be smaller than rcp
    if lcp > rcp:
        lcp, rcp = rcp, lcp

    # Crossover is exclusive of split-off point
    c1 = p1[:lcp] + p2[lcp:rcp] + p1[rcp:]
    c2 = p2[:lcp] + p1[lcp:rcp] + p2[rcp:]
    
    
    # Resolve duplicates, if any, after crossover
    c1 = resolveDuplicateRows(p1, c1, lcp, rcp)
    c2 = resolveDuplicateRows(p2, c2, lcp, rcp)
    
    return c1, c2

"""
Helper function to ensure list of row values doesn't contain any duplicates.

Given 2 parents, Parent A and Parent B, crossover will result in Child A and Child B.
 - Child A is Parent A crossed over with Parent B.
 - Child B is Parent B crossed over with Parent A.

Performs Partially Matched Crossover by switching the oldest duplicate gene
with the original gene from the first parent at that location.
 - Ex. The duplicates in Child A are switched to genes in Parent A.

Parameters:
parent - the second parent used in the cross over (array)
child - the child created from crossover (array)
lcp - index of the left crossover point
rcp - index of the right crossover point

Returns:
child - the deduplicated child (array)

"""
def resolveDuplicateRows(parent, child, lcp, rcp):
    workingChild = child.copy()
    dict = {}
    duplicates = True
    
    while duplicates:
    
        duplicates = False
        for i in range(lcp, rcp):
            dict[workingChild[i]] = parent[i]

        for i in range(lcp):
            if workingChild[i] in dict:
                workingChild[i] = dict[workingChild[i]]
        
        for i in range(rcp, len(workingChild)):
            if workingChild[i] in dict:
                workingChild[i] = dict[workingChild[i]]
        
        dupla = set()
        for num in workingChild:
            if num not in dupla:
                dupla.add(num)
            else:
                duplicates = True
                break

    return workingChild

"""
Helper function to generate randomized configurations of chess boards.

Parameters:
n - Size of the board and the number of queens

Output:
c - List representation of the queens on a chess board. The index represents the column of the board, the value represents the row.
The chess board in 0-indexed.

Example:
c[2] = 5 - A queen is present at column 2 and row 5

"""
def generateRandomBoard(n):
    input = range(0, n)
    return random.sample(input, n)

"""
Helper function to determine the fitness score of each board. Evaluates whether solution has been found.

Parameters:
n - Size of the board and the number of queens
board - List representation of the queens on a chess board.


Output:
score - Fitness score representing the number of clashing pairs of queens (integer)
solutionFound - True if fitness score is 0, False otherwise

Example:

"""
def fitness(n, board):
    solutionFound = False
    score = 0

    # Track the number of clashes along the diagonal
    # Create array of counters for the positive & negative diagonals
    negDiagonals = [0 for i in range(2*n - 1)]
    posDiagonals = [0 for i in range(2*n - 1)] 
    for i in range(len(board)):
        # Calculate which diagonal each queen is located on and increment the counters
        negDiagonal = n - (i+1) + (board[i] + 1)
        posDiagonal = (i+1) + board[i]

        negDiagonals[negDiagonal-1] += 1
        posDiagonals[posDiagonal-1] += 1
    
    # Calculate the total number of clashes
    maxCounters = [max(negDiagonals), max(posDiagonals)]
    score = max(maxCounters) - 1   
    
    if score == 0:
        solutionFound = True

    return score, solutionFound

"""
Helper function to generate randomized configurations of chess boards.

Parameters:
n - Size of the board and the number of queens

Output:
c - List representation of the queens on a chess board. The index represents the column of the board, the value represents the row.
The chess board in 0-indexed.

Example:
c[2] = 5 - A queen is present at column 2 and row 5

"""
def generateRandomBoard(n):
    input = range(0, n)
    return random.sample(input, n)

"""
Parameters:
n - 
nQueenList - A list that represents a N-Queen chess board

Output:
A list that represents a N-Queen chess board that is mutated

Example:

Input: nQueenList = [2,0,3,1]
Output: [2,1,3,0]
"""
def mutateBoard(n, nQueenList):
    input = range(0, n)
    indicesToSwap = random.sample(input, 2)

    temp = nQueenList[indicesToSwap[0]]
    nQueenList[indicesToSwap[0]] = nQueenList[indicesToSwap[1]]
    nQueenList[indicesToSwap[1]] = temp
    
    return nQueenList

"""
Prints a chess board representation of the N-Queen board.

Parameters:
nQueenList - A list that represents a N-Queen chess board

Output:
None

Example:
Q - represents a Queen

--------------------------------
|   |   |   |   | Q |   |   |   |
--------------------------------
|   | Q |   |   |   |   |   |   |
--------------------------------
|   |   |   |   |   | Q |   |   |
--------------------------------
| Q |   |   |   |   |   |   |   |
--------------------------------
|   |   |   |   |   |   | Q |   |
--------------------------------
|   |   |   | Q |   |   |   |   |
--------------------------------
|   |   |   |   |   |   |   | Q |
--------------------------------
|   |   | Q |   |   |   |   |   |
--------------------------------

"""
def printNQueenChessBoardWithLines(nQueenList):
    n = len(nQueenList)
    
    for row in range(n):
        print("-"*n*4)
        print("|", end="")
        for col in range(n):
            if row == nQueenList[col]:
                print(" Q |", end="")
            else:
                print("   |", end="")
        print()
    print("-"*n*4)

'''
Prints a 2d matrix of a chess board representation of the N-Queen board.

Parameters:
nQueenList - A list that represents a N-Queen chess board

Output:
None

Example:

1 implies a queen is present
0 implies nothing occupies the tile

Input: 
     nQueenList = [2,0,3,1]
Output:
[
    [ 0, 1, 0, 0]
    [ 0, 0, 0, 1]
    [ 1, 0, 0, 0]
    [ 0, 0, 1, 0]
]     
      2  0  3  1
'''
def printNQueenChessBoard(nQueenList):
    board = []
    n = len(nQueenList)

    boardRow = []
    for i in range(n):
        for b in range(n):
            boardRow.append(0)
        board.append(boardRow)
        boardRow = []

    for i in range(n):
        board[nQueenList[i]][i] = 1

    for row in board:
        print(row)

if __name__ == "__main__":
    main()
    
'''
    --------------------------------------------
    Test Cases
    --------------------------------------------
    TEST printNQueenChessBoard()
    nQueenList = [2,0,3,1]
    print("TEST printNQueenChessBoard(): ")
    printNQueenChessBoard(nQueenList)
    
    TEST generateRandomBoard()
    board = generateRandomBoard(n)
    print("TEST generateRandomBoard(): ", board)

    TEST mutateBoard(nQueenList)
    nQueenList = [2,0,3,1]
    print("TEST mutateBoard(): ")
    print("nQueenList = [2,0,3,1]")
    print("Mutated: ", mutateBoard(nQueenList, n))

    TEST fitness()
    score, solutionFound = fitness(n, board)
    print("TEST fitness(): ", score, solutionFound)

    TEST fitness()
    board = [2, 1, 3, 0]
    board = [3, 2, 1, 0]
    board = [2, 1, 0, 0]
    printNQueenChessBoard(board)
    print("--------------------------------")
    score, solutionFound = fitness(n, board)
    print("--------------------------------")
    print("TEST fitness(): ", score, solutionFound)
    
    TEST twoPointCrossover()
    # list1 = [1,2,3,4]
    # list2 = [5,6,7,8]

    # list3 = list1[:2] + list2[2:]

    # print("list1:", list1)
    # print("list2:", list2)
    # print()
    # print("list3:", list3)


    # p1 = [1, 2, 3, 4, 5, 6, 7, 8]
    # p2 = [8, 7, 6, 5, 4, 3, 2, 1]

    # c1, c2 = twoPointCrossover(n, p1, p2)

    # print("p1: ", p1)
    # print("p2: ", p2)
    # print()
    # print("c1: ", c1)
    # print("c2: ", c2)
'''