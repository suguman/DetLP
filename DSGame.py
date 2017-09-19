from weightedAut import wBA
import os

GLPKPath = "../Tools/glpk-4.63/"

sep = " "
newline = "\n"
var = "x"
leq = "<="
minus = "-"

# Input : A weighted automata
# Ouput : An lp file to solve discounted payoff game
def makeDSGame(wAut, num, fileName):
    filename = GLPKPath+fileName + ".lp"
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
    f.write("End\n")
    
    f.close()

# TODO : Write a function to run the .lp file
def runGLPK(filename):
    cmd = "glpsol --cpxlp " + GLPKPath + filename + ".lp > output1.txt"
    #cmd = "glpsol --cpxlp " + GLPKPath + "sample" + ".lp > output1.txt"
    os.system(cmd)
    minWeight = getValFromFile("output1.txt")
    cmd = "rm "+GLPKPath + filename + ".lp " + "output1.txt"
    os.system(cmd)
    return minWeight


    
# TODO : Write a function to extract the solution from the .lp file output
def getValFromFile(filename):
    f = open(filename)
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()
    isTimeLine = line3.strip().split()[0]
    while isTimeLine != "Time":
        line1 = line2
        line2 = line3
        line3 = f.readline()
        isTimeLine = line3.strip().split()[0]

    
    #print line1, line2, line3
    if line2.strip().split()[0] == "OPTIMAL":
        valStr = line1.strip().split()[4]
        #print valStr
        val = float(valStr)
        #print val
        return val
    else:
        return "ERROR"
    
def findMinWeight(wAut, num, filename):
    makeDSGame(wAut, num, filename)
    return runGLPK(filename)
