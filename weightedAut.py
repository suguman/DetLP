from automata import BA

class wBA(BA):
    # All states of the weighted automata are accepting states
    # Transitions are of the form (src, destination, alphabet, wt), where each is a list
    def __init__(self, states, alpha, delta, start):
        BA.__init__(self, states, alpha, delta, start, states)

    # Accessor function for weights
    def Weights(self):
        weights = []
        #print self.Trans()
        for trans in self.Trans():
            wt = trans[3][0]
            #print wt
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

    # Accessor function for minimum Weight
    def minWeight(self):
        wtList = self.Weights()
        if wtList == []:
            return 0
        else:
            return min(wtList) 


    # Access weight of each transition
    def wtFunction(self):
        wtF = {(s,d,a):[] for ([s],[d],[a],[wt]) in self.Trans()}
        for ([s],[d],[a],[wt]) in self.Trans():
            wtKey = (s,d,a)
            if wt not in wtF[wtKey]:
                wtF[wtKey].append(wt)
        return  wtF
        
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


    # Linearly transforms weight of transitons
    # Input: wAut with weight w on transitions
    # Output: wAut with weight mult*w + const on transitions
    def linearTransform(self, mult, const):
        oldTrans = self.Trans()
        newTrans = [(src, dest, alpha, [(mult*wt)+const]) for (src, dest, alpha, [wt]) in oldTrans]
        print oldTrans
        print newTrans
        return wBA(self.States(), self.Alpha(), newTrans, self.Start())
        



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
            
    @classmethod
    def sameAlphaProdMinus(cls, aut1, aut2):
        newState = []
        newAlpha = []
        newTrans = []
        for trans1 in aut1.Trans():
            for trans2 in aut2.Trans():
                src1, dest1, alpha1, [wt1] = trans1
                src2, dest2, alpha2, [wt2] = trans2
                #print alpha1, alpha2
                if alpha1 == alpha2:
                    src = src1 + src2
                    dest= dest1 + dest2
                    trans = src, dest, alpha1, [wt1-wt2] 
                    if alpha1 not in newAlpha:
                        newAlpha.append(alpha1)
                        #print alpha1, alpha2, alpha
                    if src not in newState:
                        newState.append(src)
                    if dest not in newState:
                        newState.append(dest)
                    if trans not in newTrans:
                        newTrans.append(trans)
        newStart = []
        for s1 in aut1.Start():
            for s2 in aut2.Start():
                newStart.append(s1+s2)
        startInState = False
        for st in newStart:
            if st in newState:
                startInState = True

        #print newTrans
        #print startInState, "HERE"
        
        if startInState == True:
            return wBA(newState, newAlpha, newTrans, newStart)
        else:
            #aut = BA([], newAlpha, [], [], [])
            #aut.baWrite("AUT")
            
            return wBA([], [], [], [])

        
    # Reassigns states in an automata to [i] where i is an integer
    def reassign(self):
        states = self.States()       
        statesMap = {}
        i = 0
        for state in states:
            statesMap[str(state)] = [i]
            i += 1       
        newStates = [statesMap[str(state)] for state in self.States()]
        newTrans = [(statesMap[str(src)], statesMap[str(destination)], alphabet, wt) for (src, destination, alphabet, wt) in self.Trans()]
        newStart = [statesMap[str(state)] for state in self.Start()]
        reassignedBA = wBA(newStates, self.Alpha(), newTrans, newStart)

        return reassignedBA

    # Remove infinite or -infinite weighted transitions
    def removeInf(self):
        inf = float('inf')
        negInf = -float('inf')
        transList = self.Trans()
        newTransList = []
        for trans in transList:
            src, destination, alpha, [wt] = trans
            if ((wt != inf) and (wt!= negInf)):
                newTransList.append(trans)
        return wBA(self.States(), self.Alpha(), newTransList, self.Start())

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

