from automata import BA

class wBA(BA):
    # All states of the weighted automata are accepting states
    # Transitions are of the form (src, destination, alphabet, wt), where each is a list
    def __init__(self, states, alpha, delta, start):
        BA.__init__(self, states, alpha, delta, start, states)

    # Accessor function for weights
    def Weights(self):
        weights = []
        for trans in self.Trans():
            wt = trans[3][0]
            if wt not in weights:
                weights.append(wt)
        return weights

   # Accessor function for maximum Weight
    def maxWeight(self):
        wtList = self.Weights()
        maxWt = 0
        for wt in wtList:
            if maxWt < wt:
                maxWt = wt
        return maxWt

    
    def printWeight(self):
        print("Weights are : " + str(self.Weights()))

    def printTrans(self):
        print("Transitions are :\n")
        for trans in self.Trans():
            print(str(trans[0]) + "--" + str(trans[2]) + "--" + str(trans[3])+"-->" + str(trans[1]))

    def myPrint(self):
        self.printState()
        self.printAlpha()
        self.printStart()
        self.printFinal()
        self.printTrans() 
        self.printWeight()

    #Adds weight to each transition alphabet
    #Input: Weighted automata
    #Output: Buchi automata where alphabet has been augmented with weight of transition
    def augmentWt(self):
        newDelta = []
        newAlpha = []
        delta = self.Trans()
        lenDelta = len(delta)
        for i in range(lenDelta):
            src, destination, alpha, wt = delta[i]
            newTrans = src, destination, alpha + wt
            newAlpha.append(newTrans[2])
            newDelta.append(newTrans)
        return BA(self.States(), newAlpha, newDelta, self.Start(), self.Final())
    
    # Adds weight and uniqe label to each transition alphabet
    # Input: Weigted automata
    # Output: Buchi automata where alphabet have been augmented with weight of the transition and label
    def augmentWtLabel(self):
        newDelta = []
        newAlpha = []
        delta = self.Trans()
        for i in range(len(delta)):
            src, destination, alpha, wt = delta[i]
            newTrans = src, destination, alpha +wt + [i]
            newAlpha.append(newTrans[2])
            newDelta.append(newTrans)
        return BA(self.States(), newAlpha, newDelta, self.Start(), self.Final())

    # Input : filename (string) (File is in .txt format)
    # Input file format: Starts States, 1 Blakc line, Transitions 
    #                    Start States, 1 state per line, Written as an integer
    #                    Transition, 1 transition per line
    #                    Transition format - alphabet, src-->destination, wt
    @classmethod
    def readInput(cls, filename):
        file = open(filename+".txt", "r")
        startList = []
        stateList = []
        alphaList = []
        transList = [] 
        line = file.readline()
        while (line != "\n"):
            startList.append([int(line.strip())])
            line = file.readline()
        line = file.readline()
        while (line !="\n" and line!=""):
            #print l
            alpha, trans, wt = line.strip().split(",")
            temp = trans.split("->")
            src, dest = int(temp[0]), int(temp[1])
            newTrans = [src], [dest], [alpha], [int(wt)]
            if [src] not in stateList:
                stateList.append([src])
            if [dest] not in stateList:
                stateList.append([dest])
            if [alpha] not in alphaList:
                alphaList.append([alpha])
            transList.append(newTrans)
            
            line = file.readline()

        startInState = False
        for st in startList:
            if st in stateList:
                startInState = True
        if startInState == False:
            return wBA([], [], [], [])

        return wBA(stateList, alphaList, transList, startList)
            
        
        
    

#a = ["a"]
#b = ["b"]
#c = ["c"]
#d = ["d"]

#wBA.readInput("text").myPrint()
#state = [[1],[2],[3],[4]]
#start = [[1]]
#alphabet = [a,b,c,d]
#transition =  [([1],[1],a,[2]), ([1],[2],b,[1]), ([1],[3],c,[0]), ([1],[4],d,[3]), ([3],[1],a,[2]), ([3],[2],b,[1]), ([3],[3],c,[3]), ([3],[4],d,[3]), ([4],[1],a,[2]), ([4],[2],b,[1]), ([4],[3],c,[0]), ([4],[4],d,[3])]
#wAut = wBA(state, alphabet, transition, start)
#wAut.myPrint()
#print wAut.maxWeight()
#a = wAut.augmentWtLabel()
#a.printTrans()
#b = BA.sameAlphaProd(a,a)

#b.reassign().myPrint()
#b.baWrite("testWrite")
