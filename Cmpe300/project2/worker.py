# Group 26
# MUHAMMET ALİ TOPCU 2020400147
# ABDULLAH ENES GÜLEŞ 2021400135

import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD # comm = own world comm. Will be used to communicate with the worker processes, i.e. worker group
intercomm = comm.Get_parent() # intercomm = parent comm. Will be used to communicate with the master process

# Worker process arguments
numOfProdCycles = int(sys.argv[1])
thresholdForMaintenance = int(sys.argv[2])
enhanceWearFactor = int(sys.argv[3])
reverseWearFactor = int(sys.argv[4])
chopWearFactor = int(sys.argv[5])
trimWearFactor = int(sys.argv[6])
splitWearFactor = int(sys.argv[7])

# Worker operations

# will take the input array, concatenate it and return the result
def add(inputArray):
    result = ""
    for elem in inputArray:
        result += elem
    return result;

#  duplicates the first and the last letter in the product
def enhance(inputString):
    return inputString[0] + inputString + inputString[-1]

def reverse(inputString):
    return inputString[::-1]

# The machine removes the last letter from the product. If the product consists of a single letter, then this operation is not performed
def chop(inputString):
    if len(inputString) > 1:
        return inputString[:-1]
    else:
        return inputString
    
#The machine removes the first and the last letters from the product. If the product consist of two or one letters, then this operation is not performed
def trim(inputString):
    if len(inputString) > 2:
        return inputString[1:-1]
    else:
        return inputString
    
# The machine splits the product into two parts, and discards the right part. If the product consists of odd number of letters, the split operation is performed after middle letter
def split(inputString):
    if len(inputString) > 1:
        upperBound = len(inputString) // 2
        if len(inputString) % 2 == 1:
            upperBound += 1
        return inputString[:upperBound]
    else:
        return inputString
    
def operate(inputString, operation):
    if operation == "enhance":
        return enhance(inputString)
    elif operation == "reverse":
        return reverse(inputString)
    elif operation == "chop":
        return chop(inputString)
    elif operation == "trim":
        return trim(inputString)
    elif operation == "split":
        return split(inputString)
    else:
        return inputString
    
def decideNextOperation(currentOp):
    if currentOp == "trim":
        return "reverse"
    elif currentOp == "reverse":
        return "trim"
    elif currentOp == "chop":
        return "enhance"
    elif currentOp == "enhance":
        return "split"
    elif currentOp == "split":
        return "chop"        
    
def calcWearFactor(currentOp):
    if currentOp == "trim":
        return trimWearFactor
    elif currentOp == "reverse":
        return reverseWearFactor
    elif currentOp == "chop":
        return chopWearFactor
    elif currentOp == "enhance":
        return enhanceWearFactor
    elif currentOp == "split":
        return splitWearFactor
    
class Machine:
    def __init__(self, machineID, currentProdCycle, currentOperation, parent = None, product = "", isLeaf = True, children = None, wearFactor = 0):
        self.machineID = machineID
        self.currentProdCycle = currentProdCycle
        self.currentOperation = currentOperation        
        self.parent = parent
        self.product = product
        self.isLeaf = isLeaf
        self.children = children
        self.wearFactor = wearFactor

intercommReq = None # will be used to check if there is a pending maintenance log to send to root

# get the initial machine from the master process
currentMachine = intercomm.recv(source = 0, tag = 0)

for i in range(1, numOfProdCycles+1):
    if currentMachine.machineID == 1: # root machine
        temp = []
        currentMachine.children.sort(key=lambda x: x.machineID) # sort children by machineID in ascending order
        for child in currentMachine.children:
            # receive the data from the children, in ascending order of their machineID
            data = comm.recv(source = child.machineID-1, tag = currentMachine.currentProdCycle)
            temp.append(data)
        # root machine only adds the data and sends it to the master process
        lastResult = add(temp);
        if intercommReq != None:
            intercommReq.wait()
        intercomm.send(lastResult, dest = 0, tag = currentMachine.currentProdCycle)
        currentMachine.currentProdCycle += 1
    else: # non-root machines
        data = ""
        if currentMachine.isLeaf: # leaf machine
            data = currentMachine.product
        else:
            temp = []
            currentMachine.children.sort(key=lambda x: x.machineID)
            for child in currentMachine.children:
                # receive the data from the children, in ascending order of their machineID
                data = comm.recv(source = child.machineID-1, tag = currentMachine.currentProdCycle)
                temp.append(data)
            data = add(temp)
        data = operate(data, currentMachine.currentOperation)
        # send the resulting product to the parent machine
        if intercommReq != None:
            intercommReq.wait()
        comm.send(data, dest = currentMachine.parent.machineID-1, tag = currentMachine.currentProdCycle)
        currentMachine.wearFactor += calcWearFactor(currentMachine.currentOperation)
        if currentMachine.wearFactor >= thresholdForMaintenance:
            costOfMaintenance = (currentMachine.wearFactor - thresholdForMaintenance + 1) * calcWearFactor(currentMachine.currentOperation);
            
            if intercommReq != None:
                intercommReq.wait()
            maintenanceLog = str(currentMachine.machineID)+"-"+str(costOfMaintenance)+"-"+str(currentMachine.currentProdCycle)
            intercommReq = intercomm.isend(maintenanceLog, dest = 0, tag = numOfProdCycles+1)

            currentMachine.wearFactor = 0
        currentMachine.currentOperation = decideNextOperation(currentMachine.currentOperation)
        currentMachine.currentProdCycle += 1