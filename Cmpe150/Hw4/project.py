
glass_size = int(input())
straw_pos = int(input())

# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

numberOfLoops = int(((glass_size*2+2) - straw_pos) / 2) + 1
totalRow = glass_size*2+straw_pos+1
totalCol = glass_size*2+2
width = glass_size*2+2

def topPrinter(rowArg,colArg):
    if colArg == 0:
        return
    if rowArg - colArg == totalRow - totalCol:
        print("o")
        return
    else:
        print(" ", end="")
    topPrinter(rowArg, colArg-1)

def midPrinter(rowArg, colArg, width, currentLoopArg):
    if colArg == 0:
        width -= 2
        return
    if rowArg - colArg < totalRow - totalCol - straw_pos:
        print(" ", end="")
    elif rowArg - colArg == totalRow - totalCol - straw_pos:
        print("\\", end="")
    elif width> rowArg - colArg > totalRow - totalCol - straw_pos:
        if rowArg + currentLoopArg <= glass_size*2+1:
            print("*", end="")
        else:
            if totalCol - colArg == totalRow - rowArg :
                print("o", end="")
            else:
                print(" ", end="")
    else:
        print("/")
        return
    midPrinter(rowArg, colArg-1, width, currentLoopArg)

def bottomPrinter(rowArg, colArg):
    if (totalCol+2)/2 < colArg:
        print(" ", end="")
    else:
        if rowArg == glass_size + 1:
            print("--")
        else:
            print("||")
        return
    bottomPrinter(rowArg, colArg-1)

def strawPrinter(rowArg,colArg, width, numberOfLoops_arg):
    currentLoop = numberOfLoops - numberOfLoops_arg
    if rowArg == 0:
        return
    if totalRow >= rowArg > totalRow - straw_pos:
        topPrinter(rowArg, colArg)
    elif totalRow - straw_pos >= rowArg > totalRow - straw_pos - glass_size:
        width -=2
        midPrinter(rowArg, colArg, width, currentLoop)
    else:
        bottomPrinter(rowArg, colArg)

    strawPrinter(rowArg-1,colArg, width, numberOfLoops_arg)

def loopCounter(numberOfLoops_arg):
    if numberOfLoops_arg == 0:
        return
    strawPrinter(totalRow,totalCol, width, numberOfLoops_arg)
    loopCounter(numberOfLoops_arg-1)

loopCounter(numberOfLoops)


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

