from weights import *

class UnbandedSequencer:

    # seq1 will always be the longer sequence
    #seq1 goes across the top 
    #seq2 goes down the side
    def __init__(self, seqa, seqb):
        if len(seqa) > len(seqb):
            self.seq1 = seqa
            self.seq2 = seqb
        else:
            self.seq1 = seqb
            self.seq2 = seqa

        self.currentDirection = LEFT
        self.table = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        self.directions = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        self.initTable()

    def initTable(self):

        for i in range(len(self.table)):
            self.table[i][0] = INDEL * i

        for j in range(len(self.table[0])):
            self.table[0][j] = INDEL * j
        
        self.printTable()


    def diff(self, rowJ, colI):
        if self.seq1[colI] == self.seq2[rowJ]:
            return MATCH
        else:
            return SWAP

    def minimum(self, left, top, diagonal):
        self.currentDirection = LEFT
        minVal = left
        if top < minVal:
            minVal = top
            self.currentDirection = TOP
        if diagonal < minVal:
            minVal = diagonal
            self.currentDirection = DIAGONAL
        return minVal

    def existingE(self, rowJ, colI):
        return self.table[rowJ][colI]

    def currentE(self, rowJ, colI):
        diagonal = self.diff(rowJ, colI) + self.existingE(rowJ - 1, colI - 1)
        left = INDEL + self.existingE(rowJ, colI - 1)
        top = INDEL + self.existingE(rowJ - 1, colI)

        return self.minimum(left, top, diagonal)

    def fill(self):
        for j in range(len(self.table)):
            if j > 0:
                for i in range(len(self.table[0])):
                    if i > 0:
                        self.table[j][i] = self.currentE(j, i)
                        self.directions[j][i] = self.currentDirection
        
        self.printTable()

    def printTable(self):
        print("weights")
        for row in self.table:
            print(row)
        
        print("directions")
        for row in self.directions:
            print(row)
        



    ################################# seq1 ##########################################
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
   #s
   #e
   #q
   #2
    #
    #
    #
    #
    #
    #
    #
    #

