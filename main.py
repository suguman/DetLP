from automata import BA
from weightedAut import wBA
from fileToBA import *
from determinize import determinize

def detLP(filename1, filename2, num):

    #Input weighted automata
    wAut1 = wBA.readInput(filename1)
    wAut2 = wBA.readInput(filename2)

    #determinization of weighted automata
    detAut1 = determinize(wAut1, num)
    detAut2 = determinize(wAut2, num)
    

    
