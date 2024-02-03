import sys
import random

# Setting the size of the chessboard to 8x8
CHESS_SIZE = 8

# Defining all possible moves a knight can make
moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]

# Probabilities thresholds for evaluating success in the Las Vegas Algorithm
probs = [0.7, 0.8, 0.85]

# k steps to look ahead in the Backtracking Algorithm
k_list = [0, 2, 3]

# Number of trials to run the algorithm
NUM_OF_TRIALS = 100000

# Command line argument to choose which part of the project to execute
partName = sys.argv[1]

# Function to check if the next move is valid
def checkIfValidMove(x, y, board):
    # Conditions to check: within bounds and not already visited
    if x < 0 or x >= CHESS_SIZE or y < 0 or y >= CHESS_SIZE:
        return False
    if board[x][y] != -1:
        return False
    
    return True

# Function to get all valid moves from current position
def getValidMoves(x, y, board):
    validMoves = []
    for move in moves:
        if checkIfValidMove(x + move[0], y + move[1], board):
            validMoves.append(move)
    return validMoves

# Function to write the chessboard state to the output file
def writeChess(outputFile, board):
    for i in range(CHESS_SIZE):
        for j in range(CHESS_SIZE):
            outputFile.write(str(board[i][j]).rjust(2) + " ")
        outputFile.write("\n")
    outputFile.write("\n") 

# Function to perform the Backtracking Algorithm
def backtrackingKnightTour(x, y, board, moveCount, targetMoves, startBacktrackMoveCount):
    # Base case: If targetMoves reached, return True
    if moveCount >= targetMoves:
        return True

    # Generate all valid moves from the current position
    validMoves = getValidMoves(x, y, board)

    # Try each valid move
    for move in validMoves:
        newX, newY = x + move[0], y + move[1]
        board[newX][newY] = moveCount
        if backtrackingKnightTour(newX, newY, board, moveCount + 1, targetMoves, startBacktrackMoveCount):
            return True
        # Backtrack only if beyond the starting point of backtracking
        if moveCount > startBacktrackMoveCount:
            board[newX][newY] = -1

    return False

# Counters for successful tours
successfulCounts = [0, 0, 0]

# Part 1: Implementing Las Vegas Algorithm
if partName == "part1":
    # Run the algorithm for all probability thresholds
    for j in range(0, 3):
        # Open the output file in append mode
        outputFile = open("results_" + str(probs[j]) + ".txt", "a")
        for i in range(1, NUM_OF_TRIALS):

            # Initialize the chessboard with -1 (indicating unvisited squares)
            board = [[-1 for i in range(CHESS_SIZE)] for j in range(CHESS_SIZE)]

            # Randomly select starting position
            currPos = [random.randint(0, CHESS_SIZE - 1), random.randint(0, CHESS_SIZE - 1)]
            outputFile.write("Run " + str(i) + ": starting from (" + str(currPos[0]) + "," + str(currPos[1]) + ")" + "\n")
            tourLength = 0

            while True:
                # Get all valid moves from current position
                validMoves = getValidMoves(currPos[0], currPos[1], board)
                # Check if there are no valid moves left
                if len(validMoves) == 0 or tourLength >= CHESS_SIZE * CHESS_SIZE * probs[j]:
                    break
                else:
                    # Choose a random move from valid moves
                    random.shuffle(validMoves)
                    nextMove = validMoves[0]
                    currPos[0] += nextMove[0]
                    currPos[1] += nextMove[1]
                    # Mark the move on the chessboard
                    board[currPos[0]][currPos[1]] = tourLength
                    tourLength += 1
                    outputFile.write("Stepping into (" + str(currPos[0]) + "," + str(currPos[1]) + ")" + "\n")

            # Check if the tour is successful based on the probability threshold
            if tourLength > CHESS_SIZE * CHESS_SIZE * probs[j]:
                successfulCounts[j] += 1
                outputFile.write("Successful - Tour length: " + str(tourLength) + "\n")
            else:
                outputFile.write("Unsuccessful - Tour length: " + str(tourLength) + "\n")
            # Write the final state of the chessboard to the file
            writeChess(outputFile, board);    

    # Print the results of the Las Vegas Algorithm
    for j in range(0, 3):
        print(f"LasVegas Algorithm With p = {probs[j]}")
        print(f"Number of successful tours : {successfulCounts[j]}")
        print(f"Number of trials : {NUM_OF_TRIALS}")
        print(f"Probability of a successful tour : {successfulCounts[j] / NUM_OF_TRIALS}")
        print()

# Part 2: Implementing Combined Algorithm
elif partName == "part2":
    for probIndex, p in enumerate(probs):
        print(f"--- p = {p} ---")
        for k in k_list:
            successfulCounts = 0
            for trial in range(NUM_OF_TRIALS):
                # Initialize the chessboard
                board = [[-1 for _ in range(CHESS_SIZE)] for _ in range(CHESS_SIZE)]
                # Randomly select starting position
                currPos = [random.randint(0, CHESS_SIZE - 1), random.randint(0, CHESS_SIZE - 1)]
                board[currPos[0]][currPos[1]] = 0
                moveCount = 1

                # Perform k random moves
                for _ in range(k):
                    validMoves = getValidMoves(currPos[0], currPos[1], board)
                    if not validMoves:
                        break
                    nextMove = random.choice(validMoves)
                    currPos[0] += nextMove[0]
                    currPos[1] += nextMove[1]
                    board[currPos[0]][currPos[1]] = moveCount
                    moveCount += 1

                # Now use backtracking from the current position
                if backtrackingKnightTour(currPos[0], currPos[1], board, moveCount, int(CHESS_SIZE * CHESS_SIZE * p), moveCount - 1):
                    successfulCounts += 1

            print(f"LasVegas Algorithm With p = {p} , k = {k}")
            print(f"Number of successful tours : {successfulCounts}")
            print(f"Number of trials : {NUM_OF_TRIALS}")
            print(f"Probability of a successful tour : {successfulCounts / NUM_OF_TRIALS}")
            print()
