from automata import BA

"""def makeState(stateString):"""
"""print "string is " + stateString"""
"""    stateList = [int(i) for i in stateString[1:len(stateString)-1].split(",")]"""
"""    print stateList"""
"""    return stateList"""

def convertAtomicUnitToTuple(singleAlphaComponents):
    try:
        listTuple = [int(i) for i in singleAlphaComponents.split(";")]
        Tuple = tuple(listTuple)
        return Tuple
    except ValueError:
        alpha = singleAlphaComponents.split(";")
        last = len(alpha)
        alpha = [char for char in alpha] 
        alpha = tuple(alpha)
        return alpha
    
def convertAlphaString(alphaString):
    alphaList = alphaString.split(";")
    #alphaList = alphaTemp[:-4] + [int(x) for x in alphaTemp[-4:]]
    return alphaList

def makeState(stateStr):
    removeBracket = int(stateStr[1:-1])
    return [removeBracket]


def getStartStates(filename):
    stateList = []

    line = peekLine(filename)
    while ((len(line.strip().split("->")) == 1) and line!=""):
        """print "Printing working line: " + line"""
        stateStr = line.strip().split("->")[0]
        state = makeState(stateStr)
        stateList.append(state)
        filename.readline()
        line = peekLine(filename)
        """print "nextLine"
        print line"""
    return stateList


def manipulateTransitions(filename):

    transitionList = []
    alphabetList = []
    stateList = []
    firstState = [1]
    firstTrans = 0

    line = peekLine(filename)

    while(len(line.strip().split("->"))==2):
        splitAtTrans = line.strip().split("->")
        alphabetAndSrc, destinationStr = splitAtTrans[0], splitAtTrans[1]
        splitAtComma = alphabetAndSrc.split(",")
        alphabetStr, srcStr = splitAtComma[0], splitAtComma[1]
        #print alphabetStr, srcStr, destinationStr

        alphabet = convertAlphaString(alphabetStr)
        #print alphabet
        src = makeState(srcStr)
        destination = makeState(destinationStr)
        transition = src, destination, alphabet
        
        if src not in stateList:
            stateList.append(src)
        if destination not in stateList:
            stateList.append(destination)
        if alphabet not in alphabetList:
            alphabetList.append(alphabet)
        if transition not in transitionList:
            transitionList.append(transition)

        if firstTrans == 0:
            firstState = src
            firstTrans = 1

        filename.readline()
        line = peekLine(filename)
    """print line"""
    return transitionList, alphabetList, stateList, firstState


def getFinalStates(filename):
    finalStates = getStartStates(filename)
    """print "FINAL STATES HERE " + str(finalStates)"""
    return finalStates

def peekLine(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

# alphabet a;b;1;2 returns as ["a", "b", "1", "2"]
#alphabet style should be altered based on utility
def convertToBA(inputFileName):
    fileN = open(inputFileName, "r")
    start = getStartStates(fileN)
    transitions, alphabet, states, first = manipulateTransitions(fileN)
    final = getFinalStates(fileN)
    """print "FINAl IS : "+ str(final)"""
    
    #print transitions
    #print alphabet
    #print states
    #print first

    if transitions == []:
        return BA([], [], [], [], [])
    
    if start == []:
        start = [first]

    if final == []:
        final = states

    fileN.close()
    
    return BA(states, alphabet, transitions, start, final)
    

#DSAut = convertToBA("reduced_10_DSAut.ba")
#print len(DSAut.States())
#print len(DSAut.Trans())
#print DSAut.States()
#print DSAut.Start()
#print DSAut.Final()
    
