from automata import BA
from weightedAut import wBA

def determinize(wAutIn, num):
    #Currently, assuming there is a single initial state in wAutIn
    #Algorithm works only on complete automata

    wAut = wAutIn.reassign()
    wtRange = wAut.maxWeight() - wAut.minWeight() 
    #print wAut.maxWeight(), wAut.minWeight(), wtRange
    #Since all our weights are integers, their lcd = 1. Hence we ignore the lcd
    maxVal = 2*wtRange
    limit = float('inf')
    
    gamma = wAut.wtFunction()

    wAutStart = wAut.Start()
    wAutStartIndex = wAutStart[0][0]
    #print wAutStartIndex
    wAutStateNum = len(wAut.States())
    #print wAutStateNum
    
    #new start state
    newStart = [limit for i in range(wAutStartIndex)] + [0] + [limit for i in range(wAutStartIndex+1, wAutStateNum)]
    #print newStart
    newStartList = [newStart]


    newStateList = [newStart]
    newTransList = []
    newAlpha = wAut.Alpha()
    greyStateList = [newStart]


    while greyStateList != []:
        newGreyStateList = []
        for state in greyStateList:
            for [alpha] in newAlpha:
                createState = [limit for i in range(wAutStateNum)]
                #createState Index
                for h in range(wAutStateNum):
                    ch = limit
                    #state index
                    for j in range(wAutStateNum):
                        keyTemp = (j,  h, alpha)
                        #print "Keytemp is " + str(keyTemp)
                        if gamma.has_key(keyTemp):
                            val = min(gamma[keyTemp])
                            #print "val is  " + str(val)
                        else:
                            val = limit
                        if (state[j] + val) < ch:
                            ch = state[j] + val
                            #print "ch val is " + str(ch) +" "+ str( h)
                        createState[h] = ch
                c = min(createState)
                #print "Here2"
                print createState, c, alpha
                destinationState = []
                for ch in createState:
                    if ch == float('inf'):
                        xh = ch
                    else:
                        xh = (ch-c)*num
                        if xh >= maxVal:
                            xh = limit
                    destinationState.append(xh)
                newTrans = (state, destinationState, [alpha], [c])
                print newTrans
                # Adding new transition to list of transitions
                if newTrans not in newTransList:
                    newTransList.append(newTrans)

                # Adding new state to list of states and to newGreyStateList
                if destinationState not in newStateList:
                    newStateList.append(destinationState)
                    newGreyStateList.append(destinationState)
    
            
                
                #print state, alpha,  destinationState, c
        #greyStateList = []
        greyStateList = newGreyStateList

    detWAut = wBA(newStateList, newAlpha,  newTransList, newStartList)
    detWAut.myPrint()
    detWAut.reassign()
    return detWAut





