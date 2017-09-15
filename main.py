from automata import BA
from weightedAut import wBA
#from fileToBA import *
from determinize import determinize

def detLP(filename1, filename2, num):

    #Input weighted automata
    wAut1 = wBA.readInput(filename1)
    wAut2 = wBA.readInput(filename2)

    #determinization of weighted automata
    detAut1 = determinize(wAut1, num)
    detAut2 = determinize(wAut2, num)

    #take product of detAut1, detAut2 with difference of weight
    prodAut = (wBA.sameAlphaProdMinus(detAut1, detAut2)).reassign()
    prodAut.myPrint()
    
    #solve linear inequality
    
    
detLP("Input1", "Input2", 2)
