from automata import BA
from weightedAut import wBA
#from fileToBA import *
from determinize import determinize
from DSGame import findMinWeight

def detLP(filename1, filename2, num):

    #Input weighted automata
    wAut1 = wBA.readInput(filename1)
    wAut2 = wBA.readInput(filename2)

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

    
detLP("Input1", "Input3", 3)
