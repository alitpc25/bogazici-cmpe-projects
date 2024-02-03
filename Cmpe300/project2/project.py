# Group 26
# MUHAMMET ALİ TOPCU 2020400147
# ABDULLAH ENES GÜLEŞ 2021400135

import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD

input_file = sys.argv[1]
output_file = sys.argv[2]

f = open(input_file, "r")

numOfMachines = int(f.readline())
numOfProdCycles = int(f.readline())
wearFactors = f.readline().split()

enhanceWearFactor = int(wearFactors[0])
reverseWearFactor = int(wearFactors[1])
chopWearFactor = int(wearFactors[2])
trimWearFactor = int(wearFactors[3])
splitWearFactor = int(wearFactors[4])

thresholdForMaintenance = int(f.readline())

# spawn the worker processes, send the necessary arguments to operate 
# the returned intercomm object will be used to communicate with the worker processes' process group
intercomm = comm.Spawn('python3', args=['worker.py', 
                                        str(numOfProdCycles), 
                                        str(thresholdForMaintenance),
                                        str(enhanceWearFactor),
                                        str(reverseWearFactor),
                                        str(chopWearFactor),
                                        str(trimWearFactor),
                                        str(splitWearFactor)
                                        ], maxprocs=numOfMachines);

# Machine class to represent the processes
class Machine:
    def __init__(self, machineID, currentProdCycle, currentOperation, parent = None, product = "", isLeaf = True, children = None, wearFactor = 0):
        self.machineID = machineID
        self.currentProdCycle = currentProdCycle # start from 1, end at numOfProdCycles
        self.currentOperation = currentOperation        
        self.parent = parent
        self.product = product # product is only for leaf nodes to start their operation
        self.isLeaf = isLeaf
        self.children = children
        self.wearFactor = wearFactor

# Create the tree structure
root = Machine(1, 1, "add")
tree_structure = [None] * numOfMachines
tree_structure[0] = root;

# create a list of machines as processes
for i in range(numOfMachines - 1):
    nodeId, parentId, currentOperation = f.readline().split()
    nodeId = int(nodeId)
    parentId = int(parentId)

    node = Machine(nodeId, 1, currentOperation, tree_structure[parentId-1])
    tree_structure[parentId-1].isLeaf = False # parent is not leaf anymore
    if tree_structure[parentId-1].children == None:
        tree_structure[parentId-1].children = []
    tree_structure[parentId-1].children.append(node)
    tree_structure[nodeId-1] = node

for i in range(numOfMachines):
    if tree_structure[i].isLeaf:
        data = f.readline().replace("\n", "")
        tree_structure[i].product = data # leaf nodes takes the initial products
    # send each machine to the relevant worker process over intercommunicator
    intercomm.send(tree_structure[i], dest = i, tag = 0)

output_file = open(output_file, "w")
mLogs = [] # maintenance logs

for i in range(1, numOfProdCycles+1):
    # Receive the data from the machines
    # root machine will send the last product in blocking way
    # other machines will send the maintenance log in non-blocking way
    isFinalProductWritten = False; # used to check for a last time if there is any maintenance log
    while True:
        data_probe_mLog = False
        # iprobe is used to check if there is any maintenance log
        data_probe_mLog = intercomm.iprobe(source = MPI.ANY_SOURCE, tag = numOfProdCycles+1)
        if data_probe_mLog:
            req = intercomm.irecv(source = MPI.ANY_SOURCE, tag = numOfProdCycles+1)
            data = req.wait()
            mLogs.append(data)
        if isFinalProductWritten:
            break;
        data_probe_result = False
        # iprobe is used to check if there is any completed product
        data_probe_result = intercomm.iprobe(source = 0, tag = i)
        if data_probe_result:
            data = intercomm.recv(source = 0, tag = i)
            output_file.write(data+"\n")
            isFinalProductWritten = True
                
mLogs.sort(key = lambda x: int(x.split("-")[0]))
for mLog in mLogs:
    if mLog != mLogs[-1]:
        output_file.write(mLog+"\n")
    else:
        output_file.write(mLog)

output_file.close()
comm.Disconnect()
intercomm.Disconnect()
MPI.Finalize()
