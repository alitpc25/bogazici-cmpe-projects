inputLine = input()

# HMM project

inputLine = inputLine.split(" ")

probOfR0 = float(inputLine[0]) # prior probability of rain
probOfRtGivenRtMinus1 = float(inputLine[1]) # transition probability from rain to rain
probOfRtGivenNotRtMinus1 = float(inputLine[2]) # transition probability from no rain to rain
probOfUtGivenRt = float(inputLine[3]) # emission probability from rain to umbrella
probOfUtGivenNotRt = float(inputLine[4]) # transition probability from no rain to umbrella
queryType = inputLine[5] # query type can be F, L, S, or M (forward, likelihood, smoothing, or most likely)
# rest of the input line is the query
k = 0;
if queryType != "S":
    query = inputLine[6:]
    query[0] = query[0].replace("[", "")
    query[-1] = query[-1].replace("]", "")
else:
    query = inputLine[6:-1]
    query[0] = query[0].replace("[", "")
    query[-1] = query[-1].replace("]", "")
    k = int(inputLine[-1])


def forwardAlgorithm(startT, endT):
    if startT == endT:
        if query[0] == "T":
            leftResult = probOfR0*probOfUtGivenRt
            rightResult = (1-probOfR0)*probOfUtGivenNotRt
            temp = leftResult + rightResult
            # round to 2 decimal places
            return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
        else:
            leftResult = probOfR0*(1-probOfUtGivenRt)
            rightResult = (1-probOfR0)*(1-probOfUtGivenNotRt)
            temp = leftResult + rightResult
            # round to 2 decimal places
            return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
    forwardResult = forwardAlgorithm(startT, endT-1)
    trueResult = forwardResult[0]
    falseResult = forwardResult[1]
    if query[endT] == "T":
        leftResult = probOfUtGivenRt*(probOfRtGivenRtMinus1*trueResult+probOfRtGivenNotRtMinus1*falseResult);
        rightResult = probOfUtGivenNotRt*(probOfRtGivenRtMinus1*falseResult+probOfRtGivenNotRtMinus1*trueResult);
        temp = leftResult + rightResult
        return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
    else:
        leftResult = (1-probOfUtGivenRt)*(probOfRtGivenRtMinus1*trueResult+probOfRtGivenNotRtMinus1*falseResult);
        rightResult = (1-probOfUtGivenNotRt)*(probOfRtGivenRtMinus1*falseResult+probOfRtGivenNotRtMinus1*trueResult);
        temp = leftResult + rightResult
        return [round(leftResult/temp, 2), round(rightResult/temp, 2)]

def backwardAlgorithm(startT, endT):
    if startT == endT+1:
        return [1, 1]
    backwardResult = backwardAlgorithm(startT+1, endT)
    trueResult = backwardResult[0]
    falseResult = backwardResult[1]
    if query[startT] == "T":
        leftResult = probOfUtGivenRt*probOfRtGivenRtMinus1*trueResult+probOfUtGivenNotRt*probOfRtGivenNotRtMinus1*falseResult;
        rightResult = probOfUtGivenNotRt*probOfRtGivenRtMinus1*falseResult+probOfUtGivenRt*probOfRtGivenNotRtMinus1*trueResult;
        temp = leftResult + rightResult
        return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
    else:
        leftResult = (1-probOfUtGivenRt)*(probOfRtGivenRtMinus1*trueResult) + (1-probOfUtGivenNotRt)*probOfRtGivenNotRtMinus1*falseResult;
        rightResult = (1-probOfUtGivenNotRt)*(probOfRtGivenRtMinus1*falseResult) + (1-probOfUtGivenNotRt)*probOfRtGivenNotRtMinus1*trueResult;
        temp = leftResult + rightResult
        return [round(leftResult/temp, 2), round(rightResult/temp, 2)]

#print(forwardAlgorithm(0, len(query)-1))
    
def forwardAlgorithmForLikelihood(startT, endT):
    if startT == endT:
        if query[0] == "T":
            leftResult = probOfR0*probOfUtGivenRt
            rightResult = (1-probOfR0)*probOfUtGivenNotRt
            return leftResult + rightResult
        else:
            leftResult = probOfR0*(1-probOfUtGivenRt)
            rightResult = (1-probOfR0)*(1-probOfUtGivenNotRt)
            return leftResult + rightResult
    estimatedResult = forwardAlgorithmForLikelihood(startT, endT-1)
    if query[endT] == "T":
        leftResult = probOfUtGivenRt*(probOfRtGivenRtMinus1*estimatedResult+probOfRtGivenNotRtMinus1*(1-estimatedResult));
        rightResult = probOfUtGivenNotRt*(probOfRtGivenRtMinus1*(1-estimatedResult)+probOfRtGivenNotRtMinus1*estimatedResult);
        return leftResult + rightResult
    else:
        leftResult = (1-probOfUtGivenRt)*(probOfRtGivenRtMinus1*estimatedResult+probOfRtGivenNotRtMinus1*(1-estimatedResult));
        rightResult = (1-probOfUtGivenNotRt)*(probOfRtGivenRtMinus1*(1-estimatedResult)+probOfRtGivenNotRtMinus1*estimatedResult);
        return leftResult + rightResult
    
sequence = []
    
def forwardAlgorithmForMostLikelySequence(startT, endT):
    if startT == endT:
        #base case = f1:1
        if query[0] == "T":
            leftResult = probOfR0*probOfUtGivenRt
            rightResult = (1-probOfR0)*probOfUtGivenNotRt
            temp = leftResult + rightResult
            # round to 2 decimal places
            return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
        else:
            leftResult = probOfR0*(1-probOfUtGivenRt)
            rightResult = (1-probOfR0)*(1-probOfUtGivenNotRt)
            temp = leftResult + rightResult
            # round to 2 decimal places
            return [round(leftResult/temp, 2), round(rightResult/temp, 2)]
    prevResult = forwardAlgorithmForMostLikelySequence(startT, endT-1)
    sequence.append(prevResult)
    trueResult = prevResult[0]
    falseResult = prevResult[1]
    if query[endT] == "T":
        if trueResult > falseResult:
            leftResult = probOfUtGivenRt*(probOfRtGivenRtMinus1*trueResult);
            rightResult = probOfUtGivenNotRt*((1-probOfRtGivenRtMinus1)*trueResult);
            return [round(leftResult, 2), round(rightResult, 2)]
        else:
            leftResult = probOfUtGivenRt*(probOfRtGivenNotRtMinus1*falseResult);
            rightResult = probOfUtGivenNotRt*((1-probOfRtGivenNotRtMinus1)*falseResult);
            return [round(leftResult, 2), round(rightResult, 2)]
    else:
        if trueResult > falseResult:
            leftResult = (1-probOfUtGivenRt)*(probOfRtGivenRtMinus1*trueResult);
            rightResult = (1-probOfUtGivenNotRt)*((1-probOfRtGivenRtMinus1)*trueResult);
            return [round(leftResult, 2), round(rightResult, 2)]
        else:
            leftResult = (1-probOfUtGivenRt)*(probOfRtGivenNotRtMinus1*falseResult);
            rightResult = (1-probOfUtGivenNotRt)*((1-probOfRtGivenNotRtMinus1)*falseResult);
            return [round(leftResult, 2), round(rightResult, 2)]
    

# i will use from 0 to n-1 for the time steps

if queryType == "F":
    print(forwardAlgorithm(0, len(query)-1))
elif queryType == "L":
    print(forwardAlgorithmForLikelihood(0, len(query)-1))
elif queryType == "S":
    # k is a now a number between 0 and t-1
    k = k - 1
    evidenceCount = len(query)
    forwardResult = forwardAlgorithm(0, k)
    backwardResult = backwardAlgorithm(k+1, evidenceCount-1)
    trueResult = forwardResult[0]*backwardResult[0]
    falseResult = forwardResult[1]*backwardResult[1]
    temp = trueResult + falseResult
    print([round(trueResult/temp, 2), round(falseResult/temp, 2)])
elif queryType == "M":
    sequence.append(forwardAlgorithmForMostLikelySequence(0, len(query)-1))
    print(sequence)