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

        self.iString = self.colEntries
        self.jString = self.rowEntries
        # self.seq1 = "-" + self.seq1
        # self.seq2 = "-" + self.seq2
        
        self.score = 0
        self.maxBand = 7

        self.currentDirection = LEFT
        # # print("building tables")
        self.band = [[]]
        # self.table = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        # # print("built weight table")
        # self.directions = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        self.directions = [[]]
        # # print("built dir table")
        self.initBand()
        # self.printBand()

    def initBand(self):
        self.currentI = 0

        self.buildRow1()

        self.buildRow2()
        
        self.buildRow3()


    def printBand(self):
        print("seqI : ", self.seq1, " \n seqJ : ", self.seq2)
        for row in range(len(self.band)):
            print(self.band[row])
            print(self.directions[row])

    def diff(self, rowJ, colI):
        # print("at j ", self.rowEntries[rowJ], ", at i ", self.colEntries[colI])
        if self.rowEntries[rowJ] == self.colEntries[colI]:
            return MATCH
        else:
            return SWAP

    # also sets values in directions array
    def minimum(self, diagonal, left, top, rowJ, colI, seqI):
        # print("left ", left, ",top ", top, ",diagonal ", diagonal)
        minCalc = math.inf
        direction = None
        if left != None:
            minCalc = left + INDEL
            direction = LEFT
        
        # print(self.directions[rowJ])

        if top != None and top + INDEL < minCalc:
            minCalc = top + INDEL
            direction = TOP

        if diagonal != None and self.diff(rowJ, seqI) + diagonal < minCalc:
            minCalc = self.diff(rowJ, seqI) + diagonal
            direction = DIAGONAL
        
        return minCalc, direction

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

        while bandIndex < self.maxBand:
            left = None
            top = None
            diagonal = None
            if self.band[1][bandIndex - 1] != None:
                left = self.band[1][bandIndex - 1] 
                # print("setting left")
            if bandIndex < 6:
                top = self.band[0][bandIndex + 1] #top in band is upper right entry 
                # print("setting top")
            if self.band[0][bandIndex] != None:
                diagonal = self.band[0][bandIndex] #diagonal in band is entry above 
                # print("setting diagonal")
    
            # print("appending ",  self.minimum(diagonal, left, top, 1, bandIndex, seqIndex))
            val, dir = self.minimum(diagonal, left, top, 1, bandIndex, seqIndex)
            self.band[1].append(val)
            self.directions[1].append(dir)
            # print("new row is ", self.band[1])
            # print("new dir row is ", self.directions[1])

            
            bandIndex += 1 
            seqIndex += 1

    def buildRow3(self):
        self.band.append([math.inf])
        self.directions.append([None])

        bandIndex = 1
        seqIndex = 0

        while bandIndex < self.maxBand:
            left = None
            top = None
            diagonal = None
            if self.band[2][bandIndex - 1] != None:
                left = self.band[2][bandIndex - 1] 
                # print("setting left")
            if bandIndex < 6:
                top = self.band[1][bandIndex + 1] #top in band is upper right entry 
                # print("setting top")
            if self.band[1][bandIndex] != None:
                diagonal = self.band[1][bandIndex] #diagonal in band is entry above 
                # print("setting diagonal")
    
            # print("appending ",  self.minimum(diagonal, left, top, 1, bandIndex, seqIndex))
            val, dir = self.minimum(diagonal, left, top, 2, bandIndex, seqIndex)
            self.band[2].append(val)
            self.directions[2].append(dir)
            # print("new row is ", self.band[2])
            # print("new dir row is ", self.directions[2])

            
            bandIndex += 1 
            seqIndex += 1


    #problems with initialization
    def fill(self):
        j = 3
        # print(self.rowEntries, " ", self.colEntries)
        while j < len(self.rowEntries):
            self.band.append([])
            self.directions.append([])
            # print("curent row ", self.band[j])
            # doesn't start at next open index, it looks at what is already there, which is infinity so it breaks
            for x in range(self.maxBand):
                y = x + self.currentI
                left = None
                top = None
                diagonal = None
                # print("j : ", j, ", y : ", y, ", x : ", x, ", currentI : ", self.currentI)
                if y < len(self.colEntries):
                    if x > 0 and self.band[j][x - 1] != None:
                        left = self.band[j][x - 1] 
                        # print("setting left")
                    if x < 6 and j > 0:
                        # print(self.band[j - 1])
                        top = self.band[j - 1][x + 1] #top in band is upper right entry 
                        # print("setting top")
                    if j > 0 and self.band[j - 1][x] != None:
                        diagonal = self.band[j - 1][x] #diagonal in band is entry above 
                        # print("setting diagonal")
            
                    # print("appending ",  self.minimum(diagonal, left, top, j, x))
                    val, dir = self.minimum(diagonal, left, top, j, x, y)
                    self.band[j].append(val)
                    self.directions[j].append(dir)
                    # print("new row is ", self.band[j])
                else:
                    self.band[j].append(math.inf)
            j += 1
            self.currentI += 1
    
    def build(self):
        row = len(self.rowEntries) - 1
        # print(" last row ", self.band[len(self.band) - 1])
        col = len(self.directions[len(self.directions) - 1]) - 1
        seqI = len(self.colEntries) - 1
        self.score = self.band[row][col]
        # print("score is ", self.score)
        print("building")
        while row >= 0 and seqI >= 0:
            # print("row ", row, " val ", self.rowEntries[row],  ", seqI ", seqI, " val ", self.colEntries[seqI], " col ", col)
            
            if seqI >= len(self.colEntries):
                seqI = len(self.colEntries) - 1
            elif seqI < 0:
                seqI = 0

            dir = self.directions[row][col]
            # print("direction : ", dir)

            if dir == TOP:
                self.iString = self.iString[:seqI] + "-" + self.iString[seqI:]
                row -= 1
                col += 1
            elif dir == LEFT:
                self.jString = self.jString[:row] + "-" + self.jString[row:]
                seqI -= 1
                col -= 1
            else:
                seqI -= 1
                row -= 1

            if row < 0 and seqI >=0:
                row = 0
            if row >= 0 and seqI < 0:
                seqI = 0

            if col >= 7:
                col = self.maxBand - 1
            elif col < 0:
                col = 0
        
        print("done building")
        self.iString = self.iString[1:]
        self.jString = self.jString[1:]
        print("iStr is ", self.iString)
        print("jStr is ", self.jString)



                    







