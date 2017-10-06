from automata import BA
from weightedAut import wBA
#from fileToBA import *
from determinize import determinize
from DSGame import findMinWeight


# detLP is defined when weight of word is given by infimum of weight of runs
# Input
#    wAut1 and wAut2 are input weighted automata
#    num is discount factor
# Output
#    Returns wAut1 \subseteq_d wAut2

def detLP(wAut1, wAut2, num):

    #complete automata
    #TODO
    
    #determinization of weighted automata
    detAut1 = determinize(wAut1, num)
    detAut2 = determinize(wAut2, num)

    #take product of detAut1, detAut2 with difference of weight
    prodAutTemp = (wBA.sameAlphaProdMinus(detAut1, detAut2)).reassign()
    prodAutTemp.printTrans()

    #To remove infinite or -infinite weighted edges. 
    prodAut = prodAutTemp.removeInf()
    prodAut.printTrans()

    #solve linear inequality
    minWeight = findMinWeight(prodAut, num, "file")
    print minWeight

    if minWeight == "ERROR":
        return "ERROR"

    return minWeight>0

# filename1, and filename2 are the input .wBA files
# num is the value of the discount factor
# wtFun determines whether the weight of words is taken by supremum or infimum of runs
def detLPWrapper(filename1, filename2, num, wtFun):

    #Input weighted automata
    wAut1 = wBA.readInput(filename1)
    wAut2 = wBA.readInput(filename2)

    if wtFun == "inf":
        print detLP
        return detLP(wAut1, wAut2, num)

    wt1 = wAut1.maxWeight()
    wt2 = wAut2.maxWeight()
    wt = max(wt1, wt2)
    wAutNew1 = wAut1.linearTransform(-1, wt)
    wAutNew2 = wAut2.linearTransform(-1, wt)
    #wAut1.myPrint()
    #wAutNew1.myPrint()
    print detLP(wAutNew2, wAutNew1, num)
    
detLPWrapper("Input3", "Input3", 3, "sup")
