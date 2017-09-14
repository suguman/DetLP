class BA(object):

    #Input format
    # States = [[1], [2], [3]] : List of states, each state is a list in itself
    # Alphabet = [[a,b], [b,c], [e,f]] : List of symbols, each symbol is a list in itself
    # Delta = [([1], [2], [a,b])] : List of tuples, each tuple is of the form ([fromState], [toState], [symbol])
    # start = [[1]] : List of start states, each state is a list in itself
    # acceptStates = [[2]] : Ditto start state
    def __init__(self, states, alphabet, delta, start, final):
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start = start
        self.final = final

    #Accessor Functions
    def States(self):
        return self.states
    def Alpha(self):
        return self.alphabet
    def Trans(self):
        return self.delta
    def Start(self):
        return self.start
    def Final(self):
        return self.final

    #Individual Print Functions
    def printState(self):
        print("States are : " + str(self.States())+"\n")
    def printAlpha(self):
        print("Alphabets are : " + str(self.Alpha())+"\n")
    def printTrans(self):
        print("Transitions are :\n")
        for trans in self.Trans():
            print(str(trans[0]) + "--" + str(trans[2]) + "-->" + str(trans[1]))
    def printFinal(self):
        print("Final States are : " + str(self.Final())+"\n")
    def printStart(self):
        print("Initial States are : " + str(self.Start())+"\n")

    #Print automata
    def myPrint(self):
        print("")
        self.printState()
        self.printAlpha()
        self.printStart()
        self.printFinal()
        self.printTrans()

    # Input: Two Buchi automata, every state in both automata is an accepting state, A and B
    #Input alphabet is of the form [a,wt,l] in A and [a, wt] in B
    # Output: Output combines two transitions only is 'a' is same for both A\timesB
    @classmethod
    def sameAlphaProd(cls, aut1, aut2):
        newState = []
        newAlpha = []
        newTrans = []
        for trans1 in aut1.Trans():
            for trans2 in aut2.Trans():
                src1, dest1, alpha1 = trans1
                src2, dest2, alpha2 = trans2
                #print alpha1, alpha2
                a1, wt1, l1 = alpha1[:-2], [alpha1[-2]], [alpha1[-1]]
                a2, wt2= alpha2[:-1], [alpha2[-1]]
                #print a2, wt2
                if a1 == a2:
                    alpha = a1 + wt1 + wt2 + l1 
                    src = src1 + src2
                    dest= dest1 + dest2
                    trans = src, dest, alpha
                    if alpha not in newAlpha:
                        newAlpha.append(alpha)
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

        #print startInState, "HERE"
        
        if startInState == True:
            return BA(newState, newAlpha, newTrans, newStart, newState)
        else:
            #aut = BA([], newAlpha, [], [], [])
            #aut.baWrite("AUT")
            
            return BA([], [], [], [], [])
        
            #return BA(newState+newStart, newAlpha, newTrans, newStart, newState+newStart)
        #print newState
        #print newStart
       

    # Reassigns states in an automata to [i] where i is an integer
    def reassign(self):
        states = self.States()       
        statesMap = {}
        i = 0
        for state in states:
            statesMap[str(state)] = [i]
            i += 1       
        newStates = [statesMap[str(state)] for state in self.States()]
        newTrans = [(statesMap[str(src)], statesMap[str(destination)], alphabet) for (src, destination, alphabet) in self.Trans()]
        newFinal = [statesMap[str(state)] for state in self.Final()]
        newStart = [statesMap[str(state)] for state in self.Start()]
        reassignedBA = BA(newStates, self.Alpha(), newTrans, newStart, newFinal)

        return reassignedBA

    # write the BA to a .ba file by the name filename
    def baWrite(self, filename):

        file = open(filename+".ba", "w")

        if ((len(self.States()) == 0) or (len(self.Trans()) == 0) or (len(self.Final()) == 0) or (len(self.Start()) == 0)):
            file.write("[0]\n[0]")

        else:
            aut = self.reassign()
            allInitialStates = aut.Start()
            
            initialStateString = ""
            for state in allInitialStates:
                initialStateString += str(state) + "\n"
            file.write(initialStateString)


            counter = 1
            transitionString = ""
            for transition in aut.Trans():
                counter += 1
                src, destination, alpha = transition
                #print alpha
                alphaString = str(alpha[0])
                for comp in alpha[1:]:
                    alphaString = alphaString + ";" + str(comp)
                    
                #print src, destination, alphaString
                transitionBA = alphaString + "," + str(src) + "->" + str(destination) + "\n"
                """print transitionBA"""
                transitionString += transitionBA
                if counter%10000 == 0:
                    file.write(transitionString)
                    transitionString = ""
            file.write(transitionString)

            allFinalStates = aut.Final()
            """print allFinalStates"""
            if (( allFinalStates == None) or (len(allFinalStates) == 0)):
                allFinalStates = [[10000000000000000000000000000000000000000]]
            
            finalStateString = ""
            for state in allFinalStates: 
                finalStateString += str(state) + "\n"
            file.write(finalStateString)

        file.close() 


    # Buchi automata intersection over different alphabets
    # Input, Automata A, alphabet of the form [a, wt1, wt2, l1]
    #        Automata B, alphabet of the form [wt1, wt2]
    # Output, Automata I that accepts (w,a,b,c) iff (w,a,b,c) is present in A and (a,b) is present in B

    def intersectSelAlpha(self, aut):
        
    
    # Buchi automata intersection
    # Input: Two BA
    # Output: Intersection automata
        #Making states
        states = [s1+s2+[i]  for s1 in self.States() for s2 in aut.States() for i in [1,2]]

        alphaList = self.Alpha()

        #making transitions
        #tList1: transitions out of [s1, s2, 1]
        #tList2: transitions out of [s1, s2, 2]
        tList1 = []
        tList2 = []

        for trans1 in self.Trans():
            for trans2 in aut.Trans():
                src1, dest1, alpha1 = trans1
                src2, dest2, alpha2 = trans2
                digitAlpha = [int(alpha1[1]), int(alpha1[2])]
                if digitAlpha == alpha2:
                    #print alpha1, digitAlpha, alpha2
                    if src1 in self.Final():
                        newTrans1 = src1+src2+[1], dest1+dest2+[2], alpha1
                        #print trans1, trans2, newTrans1
                        tList1.append(newTrans1)
                    else:
                        newTrans1 = src1+src2+[1], dest1+dest2+[1], alpha1
                        #print trans1, trans2, newTrans1
                        tList1.append(newTrans1)
                    

                    if src2 in aut.Final():
                        newTrans2 = src1+src2+[2], dest1+dest2+[1], alpha1
                        #print trans1, trans2, newTrans2
                        tList2.append(newTrans2)
                    else:
                        newTrans2 = src1+src2+[2], dest1+dest2+[2], alpha1
                        #print trans1, trans2, newTrans2
                        tList2.append(newTrans2)

        transitionList = tList1 + tList2
        newTransList = []
        for trans in transitionList:
            if trans not in newTransList:
                newTransList.append(trans)

        #Making Start states
        startList = [s1+s2+[1] for s1 in self.Start() for s2 in aut.Start()]

        #Making Final States
        finalList = [s1+s2+[2] for s1 in self.States() for s2 in aut.Final()]


        
        #tempAut =  BA(states, alphaList, newTransList, startList, finalList)
        #tempAut.baWrite("IntersectFilename.txt")
        return BA(states, alphaList, newTransList, startList, finalList)

            
    def intersect(self, aut):
        #Making states
        states = [s1+s2+[i]  for s1 in self.States() for s2 in aut.States() for i in [1,2]]

        #Making alphabets
        alphaList = self.Alpha()
        for alpha in aut.Alpha():
            if alpha not in alphaList:
                alphaList.append(alpha)

        #Making transitions
        #tList1: transitions out of [s1, s2, 1]
        #tList2: transitions out of [s1, s2, 2]
        tList1 = []
        tList2 = []
        
        for trans1 in self.Trans():
            for trans2 in aut.Trans():
                src1, dest1, alpha1 = trans1
                src2, dest2, alpha2 = trans2
                if alpha1 == alpha2:
                    if src1 in self.Final():
                        newTrans1 = src1+src2+[1], dest1+dest2+[2], alpha1
                        #print trans1, trans2, newTrans1
                        tList1.append(newTrans1)
                    else:
                        newTrans1 = src1+src2+[1], dest1+dest2+[1], alpha1
                        #print trans1, trans2, newTrans1
                        tList1.append(newTrans1)
                    

                    if src2 in aut.Final():
                        newTrans2 = src1+src2+[2], dest1+dest2+[1], alpha1
                        #print trans1, trans2, newTrans2
                        tList2.append(newTrans2)
                    else:
                        newTrans2 = src1+src2+[2], dest1+dest2+[2], alpha1
                        #print trans1, trans2, newTrans2
                        tList2.append(newTrans2)
                    
        transitionList = tList1 + tList2
        newTransList = []
        for trans in transitionList:
            if trans not in newTransList:
                newTransList.append(trans)
        
        #Making Start states
        startList = [s1+s2+[1] for s1 in self.Start() for s2 in aut.Start()]

        #Making Final States
        finalList = [s1+s2+[2] for s1 in self.States() for s2 in aut.Final()]



        #tempAut =  BA(states, alphaList, newTransList, startList, finalList)
        #tempAut.baWrite("IntersectFilename.txt")
        return BA(states, alphaList, newTransList, startList, finalList)


    # calls RABBIT
    # input should be RABBIT path
    #def callRabbit(cls):
        
    # Calls RABBIT, and minimizes the input BA, returning a minimized BA
    #def minimizeAut(self):
   
    

#a = ["a","b"]
#b = ["a", "c"]
#c = ["a", "c"]
#aut = BA([[1],[2]], [a, b, c], [([1],[1],a), ([1],[2],a),([2],[1],b), ([2], [1], c)], [[1]], [[2]])
#aut.baWrite("Test")
#aut.myPrint()
#A = aut.project(1,2)
#A.printAlpha()
#A.printTrans()

    
