from weights import *
import math

class BandedSequencer:

   # seq1 will always be the longer sequence
    #seq1 goes across the top 
    #seq2 goes down the side
    def __init__(self, seqa, seqb):
        # print("__init__")
        if len(seqa) > len(seqb):
            self.seq1 = seqa
            self.seq2 = seqb
        else:
            self.seq1 = seqb
            self.seq2 = seqa


        self.colEntries = "-" + self.seq1
        self.rowEntries = "-" + self.seq2

        self.iString = self.seq1
        self.jString = self.seq2
        # self.seq1 = "-" + self.seq1
        # self.seq2 = "-" + self.seq2
        
        self.score = 0
        self.maxBand = 6

        self.currentDirection = LEFT
        # # print("building tables")
        self.band = [[]]
        # self.table = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        # # print("built weight table")
        # self.directions = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        self.directions = [[]]
        # # print("built dir table")
        self.initBand()
        self.printBand()

    def initBand(self):
        self.currentI = 0

        self.buildRow1()

        self.buildRow2()
        self.band.append([math.inf])

        self.directions.append([None])


    def printBand(self):
        for row in self.band:
            print(row)
        for row in self.directions:
            print(row)

    def diff(self, rowJ, colI):
        if self.rowEntries[rowJ] == self.colEntries[colI]:
            return MATCH
        else:
            return SWAP

    # also sets values in directions array
    def minimum(self, diagonal, left, top, rowJ, colI, seqI):
        print("left ", left, ",top ", top, ",diagonal ", diagonal)
        minCalc = math.inf
        if left != None:
            minCalc = left + INDEL
            self.directions[rowJ].append(LEFT)

        if top != None and top + INDEL < minCalc:
            minCalc = top + INDEL
            self.directions[rowJ][colI] = TOP

        if diagonal != None and self.diff(rowJ, self.currentI) + diagonal < minCalc:
            minCalc = self.diff(rowJ, seqI) + diagonal
            self.directions[rowJ][colI] = DIAGONAL
        
        return minCalc

    def buildRow1(self):
        self.band[0].append(math.inf)
        self.band[0].append(math.inf)
        self.band[0].append(math.inf)
        self.band[0].append(0)
        self.band[0].append(5)
        self.band[0].append(10)
        self.band[0].append(15)

        self.directions[0].append(None)
        self.directions[0].append(None)
        self.directions[0].append(None)
        self.directions[0].append(None)
        self.directions[0].append(None)
        self.directions[0].append(None)
        self.directions[0].append(None)

    def buildRow2(self):
        self.band.append([math.inf, math.inf])
        self.directions.append([None, None])

        bandIndex = 2
        seqIndex = 0

        while bandIndex <= self.maxBand:
            left = None
            top = None
            diagonal = None
            if self.band[1][bandIndex - 1] != None:
                left = self.band[1][bandIndex - 1] 
                print("setting left")
            if bandIndex < 6:
                top = self.band[0][bandIndex + 1] #top in band is upper right entry 
                print("setting top")
            if self.band[0][bandIndex] != None:
                diagonal = self.band[0][bandIndex] #diagonal in band is entry above 
                print("setting diagonal")
    
            # print("appending ",  self.minimum(diagonal, left, top, 1, bandIndex, seqIndex))
            self.band[1].append(self.minimum(diagonal, left, top, 1, bandIndex, seqIndex))
            print("new row is ", self.band[1])
            print("new dir row is ", self.directions[1])

            
            bandIndex += 1 
            seqIndex += 1




    #problems with initialization
    def fill(self):
        j = 1
        while j < len(self.rowEntries):
            if j > 2:
                self.band.append([])
                self.directions.append([])
            if j > 3:
                self.currentI += 1
            print("curent row ", self.band[j])
            markedIndices = len(self.band[j]) - 1
            bandLen = self.maxBand - markedIndices
            # doesn't start at next open index, it looks at what is already there, which is infinity so it breaks
            for x in range(self.maxBand):
                if x < markedIndices:
                    continue
                else: 
                    y = x + self.currentI
                    left = None
                    top = None
                    diagonal = None
                    print("j : ", j, ", y : ", y, ", x : ", x, ", currentI : ", self.currentI)
                    if y < len(self.colEntries):
                        if x > 0 and self.band[j][x - 1] != None:
                            left = self.band[j][x - 1] 
                            print("setting left")
                        if x < 6 and j > 0:
                            top = self.band[j - 1][x + 1] #top in band is upper right entry 
                            print("setting top")
                        if j > 0 and self.band[j - 1][x] != None:
                            diagonal = self.band[j - 1][x] #diagonal in band is entry above 
                            print("setting diagonal")
                
                        print("appending ",  self.minimum(diagonal, left, top, j, x))
                        self.band[j].append(self.minimum(diagonal, left, top, j, x))
                        print("new row is ", self.band[j])
                    else:
                        self.band[j].append(math.inf)
            j += 1


                    







