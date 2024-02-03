import timeit
import random
import math

def algorithm(arr):
    """Takes as input a list of size n and returns an integer y."""
    y = 0

    for i in range(len(arr)):

        if arr[i] == 0:
            for j in range(i, len(arr)):
                y += 1
                k = len(arr)
                while k > 0:
                    k = k // 3
                    y += 1

        elif arr[i] == 1:
            for m in range(i, len(arr)):
                y += 1
                for l in range(m, len(arr)):
                    for t in range(len(arr), 0, -1):
                        for z in range(len(arr), 0, -t):
                            y += 1
            
        else:
            y += 1
            p = 0
            while p < len(arr):
                for j in range(p**2-1):
                    y += 1
                p += 1

    return y


def random_array(n):
    """Takes as input an integer n and returns a random list with 0,1 and 2 as elements of size n."""
    arr = []
    for i in range(n):
        arr.append(random.randint(0,2))
    return arr


# If index < the value of the function, then fill the array with 1, else switch to filling with 2
def worstCaseIndexSwitch(index, n):
    if n <= 1:
        return True
    return index < (3 * math.log2(n) + 6 * n * math.log2(n) - math.sqrt(3) * (math.sqrt((4 * math.log2(n) + 12 * n * math.log2(n) + 8 * n**2 * math.log2(n) + 3 * (math.log2(n))**2)))) / (6 * math.log2(n))


# printing case, size and elapsed time(s) for best, worst and average case and 17 different data sizes n as:
# print("Case: ", case, "Size: ", n, "Time: ", elapsed_time)
# case denotes “best”, “worst” or “average” case

input_sizes_list = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
NUMBER_OF_ITERATIONS_FOR_AVERAGE = 10


for n in input_sizes_list:

    size = n

    # BEST INPUT
    case = "best"
    arrBest = [0] * n

    start_time = timeit.default_timer()
    algorithm(arrBest)
    elapsed_time = timeit.default_timer() - start_time

    print("Case:", case, "Size:", size, "Time:", elapsed_time)


    # WORST INPUT
    case = "worst"
    arrWorst = [0] *n

    for i in range(n):
        arrWorst[i] = 1 if worstCaseIndexSwitch(i, n) else 2

    start_time = timeit.default_timer()
    algorithm(arrWorst)
    elapsed_time = timeit.default_timer() - start_time

    print("Case:", case, "Size:", size, "Time:", elapsed_time)


    # AVERAGE INPUT
    case = "average"
    elapsed_time = 0

    for i in range(NUMBER_OF_ITERATIONS_FOR_AVERAGE):
        # creating a random array with n elements
        arr = random_array(n)

        previous_time = elapsed_time
        start_time = timeit.default_timer()
        algorithm(arr)
        elapsed_time += timeit.default_timer() - start_time
        
        # For each run
        print("Run:" , i+1, "Time:", elapsed_time - previous_time)

    elapsed_time = elapsed_time / NUMBER_OF_ITERATIONS_FOR_AVERAGE

    # Average for all 10 runs
    print("Case:", case, " Size:", size, " Time:", elapsed_time)
    print()
    

