from weightedAut import wBA

sep = " "
newline = "\n"
var = "x"
leq = "<="
minus = "-"

# Input : A weighted automata
# Ouput : An lp file to solve discounted payoff game
def makeDSGame(wAut, num, fileName):
    filename = fileName + ".lp"
    f = open(filename, "w")
    f.close()
    f = open(filename, "a")

    # Making objective
    startState = wAut.Start()[0][0]
    varName = var+str(startState)
    line = "Maximize"+newline+varName+newline
    f.write(line)

    # Writing constraints
    bufferLine = "Subject to" + newline
    transList = wAut.Trans()
    counter = 0
    for trans in transList:
        counter += 1
        [src], [destination], alpha, [wt] = trans
        srcVar = var + str(src)
        destinationVar = var + str(destination)
        #line = num+sep+srcVar+sep+minus+desrinationVar+sep+leq+sep+
        constraintAr = [str(num), srcVar, minus, destinationVar, leq, str(num*wt)]
        line = sep.join(constraintAr) + newline
        bufferLine += line
        if counter%2 == 0:
            f.write(bufferLine)
            counter = 0
            bufferLine = ""
    f.write(bufferLine)

    # Ending
    f.write("End")
    
    f.close()

# TODO : Write a function to run the .lp file

# TODO : Write a function to extract the solution from the .lp file output
