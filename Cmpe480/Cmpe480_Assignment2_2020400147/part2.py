import sys

selectedAgentNo = int(sys.argv[1])

inputFileName = sys.argv[2]

outputFileName = sys.argv[3]

f = open(inputFileName, "r")

puzzle = []

maxTreeDepth = 10 # If exceeds, draw

# Read input file
for line in f:
    puzzle.append([int(x) for x in line.split()])
outputFile = open(outputFileName, "w")

numberOfExpandedNodes = 1

# Copies by value
def copyArray(puzzle):
    temp = []
    for row in range(3):
        temp.append([])
        for col in range(3):
            temp[row].append(puzzle[row][col])
    return temp

def findOppositeMove(move):
    if(move == "U"):
        return "D"
    elif(move == "D"):
        return "U"
    elif(move == "L"):
        return "R"
    elif(move == "R"):
        return "L"
    
def findTilePosition(puzzle, tile):
    for row in range(3):
        for col in range(3):
            if(puzzle[row][col] == tile):
                return (row, col)
            
def didTileOccupyOpponentWinPosition(agentNo, row, col):
    if(agentNo == 1):
        return ((row == 2 and col == 1) or (row == 2 and col == 2))
    else:
        return ((row == 0 and col == 0) or (row == 0 and col == 1))

# when called from max, selectedAgentNo = node.agentNo and we are deciding minimizer's move
# when called from min, selectedAgentNo = 3 - node.agentNo and we are deciding maximizer's move
# node.agentNo = evaluates the previous move
def terminal_test(node, depth, selectedAgentNo):
    if(depth-1 == maxTreeDepth):
        return (True, 0)
    if((node.puzzle[0][0] + node.puzzle[0][1] == 3)): # 1+2 or 2+1
        return (True, 1 if selectedAgentNo == 1 else -1)
    elif((node.puzzle[2][1] + node.puzzle[2][2] == 17)): # 8+9 or 9+8
        return (True, 1 if selectedAgentNo == 2 else -1)
    elif(depth > 2):
        grandparent = node.parent.parent
        if(node.movedTile == grandparent.movedTile and node.movePosition == findOppositeMove(grandparent.movePosition)):
            return (True, 1 if node.agentNo == selectedAgentNo else -1)
        
        if(node.agentNo == 2):
            tile1Position = findTilePosition(node.puzzle, 1)
            if(tile1Position == findTilePosition(grandparent.puzzle, 1) and didTileOccupyOpponentWinPosition(1, tile1Position[0], tile1Position[1])):
                return (True, 1 if selectedAgentNo == node.agentNo else -1)
            
            tile2Position = findTilePosition(node.puzzle, 2)
            if(tile2Position == findTilePosition(grandparent.puzzle, 2) and didTileOccupyOpponentWinPosition(1, tile2Position[0], tile2Position[1])):
                return (True, 1 if selectedAgentNo == node.agentNo else -1)
        else:
            tile8Position = findTilePosition(node.puzzle, 8)
            if(tile8Position == findTilePosition(grandparent.puzzle, 8) and didTileOccupyOpponentWinPosition(2, tile8Position[0], tile8Position[1])):
                return (True, 1 if selectedAgentNo == node.agentNo else -1)
            
            tile9Position = findTilePosition(node.puzzle, 9)
            if(tile9Position == findTilePosition(grandparent.puzzle, 9) and didTileOccupyOpponentWinPosition(2, tile9Position[0], tile9Position[1])):
                return (True, 1 if selectedAgentNo == node.agentNo else -1)

    return (False, 0)
    
            
def successors(node):
    global numberOfExpandedNodes
    expandedNodes = []
    moveTiles = []
    if(node.agentNo == 1):
        moveTiles = [1, 2]
    else:
        moveTiles = [8, 9]

    for tile in moveTiles:
        (row, col) = findTilePosition(node.puzzle, tile)
        if(row > 0 and node.puzzle[row-1][col] == 0):
            tempPuzzle = copyArray(node.puzzle)
            tempPuzzle[row][col] = 0
            tempPuzzle[row-1][col] = tile
            expandedNodes.append(Node(tempPuzzle, 3 - node.agentNo, node.depth+1, tile, "U", node))
        if(col < 2 and node.puzzle[row][col+1] == 0):
            tempPuzzle = copyArray(node.puzzle)
            tempPuzzle[row][col] = 0
            tempPuzzle[row][col+1] = tile
            expandedNodes.append(Node(tempPuzzle, 3 - node.agentNo, node.depth+1, tile, "R", node))
        if(row < 2 and node.puzzle[row+1][col] == 0):
            tempPuzzle = copyArray(node.puzzle)
            tempPuzzle[row][col] = 0
            tempPuzzle[row+1][col] = tile
            expandedNodes.append(Node(tempPuzzle, 3 - node.agentNo, node.depth+1, tile, "D", node))
        if(col > 0 and node.puzzle[row][col-1] == 0):
            tempPuzzle = copyArray(node.puzzle)
            tempPuzzle[row][col] = 0
            tempPuzzle[row][col-1] = tile
            expandedNodes.append(Node(tempPuzzle, 3 - node.agentNo, node.depth+1, tile, "L", node))
            
    numberOfExpandedNodes += len(expandedNodes)
    return expandedNodes

possibleWinnerLeaves = []
possibleLoserLeaves = []

def minimax_decision_ab(node, selectedAgentNo, alpha, beta):
    v = -1
    for expandedNode in successors(node):
        temp = min_value_ab(expandedNode, selectedAgentNo, 1, alpha, beta)
        if(temp > v):
            v = temp
        if(v >= beta):
            node.eval = v
            return v
        alpha = max(alpha, v)
    node.eval = v
    return v
    

def max_value_ab(node, selectedAgentNo, depth, alpha, beta):
    # selectedAgentNo = node.agentNo, since we are maximizing
    (boolResult, utilityResult) = terminal_test(node, depth, selectedAgentNo)
    if boolResult:
        if(utilityResult == -1):
            node.eval = -1
            possibleLoserLeaves.append(node)
        return utilityResult
    v = -1
    for expandedNode in successors(node):
        v = max(v, min_value_ab(expandedNode, selectedAgentNo, depth+1, alpha, beta))
        if(v >= beta):
            node.eval = v
            return v
        alpha = max(alpha, v)
    node.eval = v
    return v


def min_value_ab(node, selectedAgentNo, depth, alpha, beta):
    # selectedAgentNo = 3 - node.agentNo, since we are minimizing
    (boolResult, utilityResult) = terminal_test(node, depth, selectedAgentNo)
    if boolResult:
        if(utilityResult == 1):
            node.eval = 1
            possibleWinnerLeaves.append(node)
        return utilityResult
    v = 1
    for expandedNode in successors(node):
        v = min(v, max_value_ab(expandedNode, selectedAgentNo, depth+1, alpha, beta))
        if(v <= alpha):
            node.eval = v
            return v
        beta = min(beta, v)
    node.eval = v
    return v

class Node:
    def __init__(self, puzzle, agentNo, depth, movedTile, movePosition, parent):
        self.puzzle = puzzle
        self.agentNo = agentNo # agent that will move next
        self.depth = depth
        self.movedTile = movedTile # tile that was prev moved
        self.movePosition = movePosition # direction of the prev move
        self.parent = parent # parent node that made the prev move
        self.eval = 0

rootNode = Node(puzzle, selectedAgentNo, 0, 0, "", None)
result = minimax_decision_ab(rootNode, selectedAgentNo, -1, 1)

maxNumOfMoves = 0

for leaf in possibleWinnerLeaves:
    depth = 0
    while(leaf.parent != None and leaf.eval == 1):
        depth += 1
        leaf = leaf.parent
    if (leaf == rootNode):
        maxNumOfMoves = max(maxNumOfMoves, depth)

if(maxNumOfMoves == 0):
    for leaf in possibleLoserLeaves:
        depth = 0
        while(leaf.parent != None and leaf.eval == -1):
            depth += 1
            leaf = leaf.parent
        if (leaf == rootNode and result == -1):
            maxNumOfMoves = max(maxNumOfMoves, depth)

outputFile.write("Minimax value of root node: "+str(result) + "\n")
outputFile.write("Maximum number of moves: "+(str(maxNumOfMoves)) + "\n")
outputFile.write("Number of expanded nodes: "+str(numberOfExpandedNodes) + "\n")
