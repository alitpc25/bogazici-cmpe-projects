import heapq
import sys

inputFileName = sys.argv[1]

outputFileName = sys.argv[2]

f = open(inputFileName, "r")

puzzle = []
for line in f:
    puzzle.append([int(x) for x in line.split()])
f.close()

goalPuzzle = [[1,2,3],[4,5,6],[0,0,0]]

outputFile = open(outputFileName, "w");

def moveUp(puzzle, row, col):
    temp_puzzle = copyArray(puzzle)
    if row > 0:
        temp_puzzle[row][col], temp_puzzle[row-1][col] = temp_puzzle[row-1][col], temp_puzzle[row][col]
    return temp_puzzle
    
def moveDown(puzzle, row, col):
    temp_puzzle = copyArray(puzzle)
    if row < 2:
        temp_puzzle[row][col], temp_puzzle[row+1][col] = temp_puzzle[row+1][col], temp_puzzle[row][col]
    return temp_puzzle
    
def moveLeft(puzzle, row, col):
    temp_puzzle = copyArray(puzzle)
    if col > 0:
        temp_puzzle[row][col], temp_puzzle[row][col-1] = temp_puzzle[row][col-1], temp_puzzle[row][col]
    return temp_puzzle
    
def moveRight(puzzle, row, col):
    temp_puzzle = copyArray(puzzle)
    if col < 2:
        temp_puzzle[row][col], temp_puzzle[row][col+1] = temp_puzzle[row][col+1], temp_puzzle[row][col]
    return temp_puzzle
    
# Copies by value
def copyArray(puzzle):
    temp = []
    for row in range(3):
        temp.append([])
        for col in range(3):
            temp[row].append(puzzle[row][col])
    return temp


# Heuristic func is manhattan distance of numbered tiles + their distance to the nearest 0 tile
def heuristic(puzzle, goalPuzzle):
    totalManhDist = 0
    for row in range(3):
        for col in range(3):
            for goalRow in range(3):
                for goalCol in range(3):
                    if puzzle[row][col] == goalPuzzle[goalRow][goalCol] and puzzle[row][col] != 0:
                        totalManhDist += abs(row-goalRow) + abs(col-goalCol)
    return totalManhDist

def expandNode(node):
    puzzle = node.puzzle
    children = set()
    foundZeros = []

    for e in range(3):
        row, col = 0, 0
        for i in range(3):
            for j in range(3):
                if puzzle[i][j] == 0 and (i,j) not in foundZeros:
                    foundZeros.append((i,j))
                    row, col = i, j

                    upNode = moveUp(copyArray(puzzle), row, col)
                    rightNode = moveRight(copyArray(puzzle), row, col)
                    downNode = moveDown(copyArray(puzzle), row, col)
                    leftNode = moveLeft(copyArray(puzzle), row, col)
                    
                    children.add(Node(upNode, node, "U "))
                    children.add(Node(rightNode, node, "R "))
                    children.add(Node(downNode, node, "D "))
                    children.add(Node(leftNode, node, "L "))
    
    return children

# Move priority U > R > D > L
def movePoint(move):
    if(move == "U "):
        return 0;
    elif(move == "R "):
        return 1;
    elif(move == "D "):
        return 2;
    elif(move == "L "):
        return 3;

class Node:
    nodeNumber = 0

    def __init__(self, puzzle, parent=None, move=""):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.movePoint = movePoint(move)
        self.g = 0
        self.h = 0
        self.id = Node.nodeNumber
        Node.nodeNumber += 1

    def __lt__(self, other):
        # First compare f values, if they are equal, priority is as move U > R > D > L
        return ((self.g + self.h) < (other.g + other.h)) \
            or ((self.g + self.h) == (other.g + other.h) and self.movePoint < other.movePoint) \
            or ((self.g + self.h) == (other.g + other.h) and self.movePoint == other.movePoint and self.id < other.id) 
    
    # equality checks should be between only puzzle statse
    def __eq__(self, other):
        if other == None:
            return False
        return self.puzzle == other.puzzle

    def __hash__(self):
        return hash(str(self.puzzle))
    
def pathCost(node):
    if node.parent == None:
        return 0
    return pathCost(node.parent) + 1

def printPuzzleStates(node):
    if node == None:
        return ""
    puzzleStr = "\n"
    for i in range(3):
        puzzleStr += str(node.puzzle[i]) + "\n"
    return printPuzzleStates(node.parent) + puzzleStr + ""

def aStar(puzzle, goalPuzzle):
    toVisit = []
    heapq.heapify(toVisit)
    visited = set()
    root = Node(puzzle)
    root.g = 0
    root.h = heuristic(puzzle, goalPuzzle)
    heapq.heappush(toVisit, root)

    while heapq:
        curNode = heapq.heappop(toVisit)
        
        if curNode.puzzle == goalPuzzle:
            print("Found the solution!")
            outputFile.write("Number of expanded nodes: " + str(len(visited)+len(toVisit)) + "\n")
            outputFile.write("Path-cost: " + str(pathCost(curNode)) + "\n")
            outputFile.write("Path: " + printPuzzleStates(curNode))
            return curNode.puzzle
        
        visited.add(tuple(map(tuple, curNode.puzzle)))

        for child in expandNode(curNode):
            if tuple(map(tuple, child.puzzle)) not in visited:
                child.g = curNode.g + 1
                child.h = heuristic(child.puzzle, goalPuzzle)
                heapq.heappush(toVisit, child)
    
    print("No solution found!")    

aStar(puzzle, goalPuzzle)