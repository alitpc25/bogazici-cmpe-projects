import sys
from collections import deque
import heapq

sys.setrecursionlimit(10000)

goalPuzzle = [[1,2,3],[4,5,6],[7,8,0]]


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


# BFS to find the solution

def bfs(puzzle, goalPuzzle, outputFile):
    # Adds puzzle and pathUntilPuzzle to the queue as tuple
    queue = deque([(puzzle, "")])
    visited = set()

    while queue:
        curPuzzle, pathUntil = queue.popleft()

        if curPuzzle == goalPuzzle:
            print("Found the solution!")
            outputFile.write("Number of expanded nodes: " + str(len(queue)+len(visited)) + "\n")
            outputFile.write("Path-cost: " + str(int(len(pathUntil)/2)) + "\n") # since we add path as string+" ", i divided by 2
            outputFile.write("Path: " + pathUntil + "\n")
            return curPuzzle
        visited.add(tuple(map(tuple, curPuzzle)))

        for row in range(3):
            for col in range(3):
                if curPuzzle[row][col] == 0:

                    tempPuzzle = moveUp(curPuzzle, row, col)
                    if tuple(map(tuple, tempPuzzle)) not in visited:
                        queue.append((copyArray(tempPuzzle), pathUntil + "U "))

                    tempPuzzle = moveRight(curPuzzle, row, col)
                    if tuple(map(tuple, tempPuzzle)) not in visited:
                        queue.append((copyArray(tempPuzzle), pathUntil + "R "))

                    tempPuzzle = moveDown(curPuzzle, row, col)
                    if tuple(map(tuple, tempPuzzle)) not in visited:
                        queue.append((copyArray(tempPuzzle), pathUntil + "D "))

                    tempPuzzle = moveLeft(curPuzzle, row, col)
                    if tuple(map(tuple, tempPuzzle)) not in visited:
                        queue.append((copyArray(tempPuzzle), pathUntil + "L "))
                    
                    break
    print("No solution found!")
    return None



# DFS to find the solution with stack

def dfs(puzzle, goalPuzzle, outputFile):
    puzzleStack = [puzzle]
    pathStack = [""]
    visited = set()

    while puzzleStack:
        curPuzzle = puzzleStack.pop()
        pathUntil = pathStack.pop()
        
        if curPuzzle == goalPuzzle:
                print("Found the solution!")
                outputFile.write("Number of expanded nodes: " + str(len(visited)) + "\n")
                outputFile.write("Path-cost: " + str(int(len(pathUntil)/2)) + "\n") # since string+" ", i divided by 2
                outputFile.write("Path: " + str(pathUntil) + "\n")
                return curPuzzle
        
        if tuple(map(tuple, curPuzzle)) not in visited:
            visited.add(tuple(map(tuple, curPuzzle)))

            row, col = 0, 0
            for i in range(3):
                for j in range(3):
                    if curPuzzle[i][j] == 0:
                        row, col = i, j

            nextLeft = moveLeft(curPuzzle, row, col)
            if tuple(map(tuple, nextLeft)) not in visited:
                puzzleStack.append(nextLeft)
                pathStack.append(pathUntil + "L ")

            nextDown = moveDown(curPuzzle, row, col)
            if tuple(map(tuple, nextDown)) not in visited:
                puzzleStack.append(nextDown)
                pathStack.append(pathUntil + "D ")

            nextRight = moveRight(curPuzzle, row, col)
            if tuple(map(tuple, nextRight)) not in visited:
                puzzleStack.append(nextRight)
                pathStack.append(pathUntil + "R ")

            nextUp = moveUp(curPuzzle, row, col)
            if tuple(map(tuple, nextUp)) not in visited:
                puzzleStack.append(nextUp)
                pathStack.append(pathUntil + "U ")
                
    print("No solution found!")   


# Heuristic func is manhattan distance of all tiles
def heuristic(puzzle, goalPuzzle):
    totalManhDist = 0
    for row in range(3):
        for col in range(3):
            for goalRow in range(3):
                for goalCol in range(3):
                    if puzzle[row][col] == goalPuzzle[goalRow][goalCol]:
                        totalManhDist += abs(row - goalRow) + abs(col - goalCol)
    return totalManhDist


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

def path(node):
    if node == None:
        return ""
    return path(node.parent) + node.move

def expandNode(node):
    puzzle = node.puzzle
    children = []
    row, col = 0, 0

    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                row, col = i, j

    upNode = moveUp(copyArray(puzzle), row, col)
    rightNode = moveRight(copyArray(puzzle), row, col)
    downNode = moveDown(copyArray(puzzle), row, col)
    leftNode = moveLeft(copyArray(puzzle), row, col)

    if upNode != puzzle:
        children.append(Node(upNode, node, "U "))
    if rightNode != puzzle:
        children.append(Node(rightNode, node, "R "))
    if downNode != puzzle:
        children.append(Node(downNode, node, "D "))
    if leftNode != puzzle:
        children.append(Node(leftNode, node, "L "))

    return children


# Uniform cost search to find the solution.

def ucs(puzzle, goalPuzzle, outputFile):
    toVisit = []
    heapq.heapify(toVisit)
    visited = set()
    root = Node(puzzle)
    root.g = 0
    root.h = 0
    heapq.heappush(toVisit, root)

    while heapq:
        curNode = heapq.heappop(toVisit)

        if curNode.puzzle == goalPuzzle:
            print("Found the solution!")
            outputFile.write("Number of expanded nodes: " + str(len(visited)+len(toVisit)) + "\n")
            outputFile.write("Path-cost: " + str(pathCost(curNode)) + "\n")
            outputFile.write("Path: " + path(curNode) + "\n")
            return curNode.puzzle
        
        visited.add(tuple(map(tuple, curNode.puzzle)))

        for child in expandNode(curNode):
            if tuple(map(tuple, child.puzzle)) not in visited:
                child.g = curNode.g + 1
                child.h = 0
                heapq.heappush(toVisit, child)
    
    print("No solution found!")


# Greedy search to find the solution

def greedy(puzzle, goalPuzzle, outputFile):
    toVisit = []
    heapq.heapify(toVisit)
    visited = set()
    root = Node(puzzle)
    root.h = heuristic(puzzle, goalPuzzle)
    root.g = 0
    heapq.heappush(toVisit, root)

    while heapq:
        curNode = heapq.heappop(toVisit)

        if curNode.puzzle == goalPuzzle:
            print("Found the solution!")
            outputFile.write("Number of expanded nodes: " + str(len(visited)+len(toVisit)) + "\n")
            outputFile.write("Path-cost: " + str(pathCost(curNode)) + "\n")
            outputFile.write("Path: " + path(curNode) + "\n")
            return curNode.puzzle
        
        visited.add(tuple(map(tuple, curNode.puzzle)))

        for child in expandNode(curNode):
            if tuple(map(tuple, child.puzzle)) not in visited:
                child.g = 0 # since greedy doesn't care about path cost
                child.h = heuristic(child.puzzle, goalPuzzle)
                heapq.heappush(toVisit, child)
    
    print("No solution found!")
    

# A* search to find the solution

def aStar(puzzle, goalPuzzle, outputFile):
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
            outputFile.write("Path: " + path(curNode) + "\n")
            return curNode.puzzle
        
        visited.add(tuple(map(tuple, curNode.puzzle)))

        for child in expandNode(curNode):
            if tuple(map(tuple, child.puzzle)) not in visited:
                child.g = curNode.g + 1
                child.h = heuristic(child.puzzle, goalPuzzle)
                heapq.heappush(toVisit, child)
    
    print("No solution found!")



inputFileName = sys.argv[1]

outputFileName = sys.argv[2]

f = open(inputFileName, "r")

puzzle = []

for line in f:
    puzzle.append([int(x) for x in line.split()])
f.close()

outputFile = open(outputFileName, "w")

bfs(puzzle, goalPuzzle, outputFile)
dfs(puzzle, goalPuzzle, outputFile)
ucs(puzzle, goalPuzzle, outputFile)
greedy(puzzle, goalPuzzle, outputFile)
aStar(puzzle, goalPuzzle, outputFile)
