import numpy as np

from cachesim import CacheSimulator, Cache, MainMemory
from argparse import ArgumentParser


def make_cache() -> CacheSimulator:
    mem = MainMemory()
    l3 = Cache("L3", 20480, 16, 64, "LRU")                           
    mem.load_to(l3)
    mem.store_from(l3)
    l2 = Cache("L2", 512, 8, 64, "LRU", store_to=l3, load_from=l3)  
    l1 = Cache("L1", 64, 8, 64, "LRU", store_to=l2, load_from=l2) 
    cs = CacheSimulator(l1, mem)
    return cs


parser = ArgumentParser()
parser.add_argument('-a', '--algorithm', type=str, choices=['simple', 'recursive'])
parser.add_argument('-N', '--N', type=int)
parser.add_argument('-K', '--K', type=int)
args = parser.parse_args()

algorithm, N, K = args.algorithm, args.N, args.K

cs1 = make_cache()
cs2 = make_cache()

rnd_vals1 = np.random.rand(N, N)
rnd_vals2 = np.random.rand(N, N)

# WRITE YOUR CODE BELOW #

# memory
m = 256 * 1024 * 1024

# cs1 for row major
# cs2 for block array

# row major:
if(algorithm == 'simple'):
    memory1 = np.zeros([m], dtype=np.float16) # for cs1
    result1 = np.zeros([m], dtype=np.float16) # for cs1, results stored in row major order

    for i in range(N):
        for j in range(N):
            cs1.store((i*N+j))
            memory1[i*N+j] = rnd_vals1[i][j]
            cs1.store(i*N+j+N*N)
            memory1[i*N+j+N*N] = rnd_vals2[i][j]

    resultIndex = 0
    for i in range(N):
        for j in range(N):
            sum = 0
            for k in range(N):
                cs1.load(i*N+k)
                cs1.load(N*N + (N*k) + j)
                elemA = memory1[i*N+k]
                elemB = memory1[N*N + (N*k) + j]
                sum+=elemA*elemB
            result1[resultIndex] = sum
            resultIndex+=1

# block:
if(algorithm == 'recursive'):
    memory2 = np.zeros([m], dtype=np.float16) # for cs2
    result2 = np.zeros([m], dtype=np.float16) # for cs2, results stored in block order

    ind = 0;
    for k in range(N//K):
        for l in range(N//K):
            for i in range(K):
                for j in range(K):
                    cs2.store(ind)
                    memory2[ind] = rnd_vals1[i+K*k][j+l*K]
                    cs2.store(ind + N*N)
                    memory2[ind + N*N] = rnd_vals2[i+K*k][j+l*K]
                    ind+=1

    ind = 0
    for ii in range(N//K):
        for jj in range(N//K):
            for i in range(K):
                for j in range(K):
                        sum = 0
                        for k in range(N):
                            cs2.load(i*K + (k//K)*K*K + (k%K) + ii*(N//K)*K*K)
                            cs2.load((k%K)*K + (k//K)*K*N + (j%K) + jj*K*K + N*N)
                            elemA = memory2[i*K + (i//K)*K*K + (k//K)*K*K + (k%K) + ii*(N//K)*K*K]
                            elemB = memory2[(k%K)*K + (k//K)*K*N + (j%K) + jj*K*K + N*N ]
                            sum+=elemA*elemB
                        result2[ind] = sum
                        ind+=1
        

# WRITE YOUR CODE ABOVE #

print('Row major array')
cs1.print_stats()


print('Block array')
cs2.print_stats()