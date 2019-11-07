from weights import *

class UnbandedSequencer:

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

        self.endRow = 0
        self.endCol = 0

        self.iString = self.seq1
        self.jString = self.seq2
        # self.seq1 = "-" + self.seq1
        # self.seq2 = "-" + self.seq2
        
        self.score = 0

        self.currentDirection = LEFT
        # # print("building tables")
        self.table = [[0]]
        # self.table = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        # # print("built weight table")
        # self.directions = [[0 for i in range(len(self.seq1))] for j in range(len(self.seq2))] 
        self.directions = [[]]
        # # print("built dir table")
        self.initTable()

    def reverseStrings(self):
        self.iString = self.iString[::-1]
        self.jString = self.jString[::-1]
        # # print(self.iString)
        # # print(self.jString)

    def initTable(self):
        # print("initTable")
        for i in range(len(self.seq1)):
            self.table[0].append(INDEL * (i+1))
            self.directions[0].append(None)
            self.endCol += 1

        # self.# printTable()
        for j in range(len(self.seq2)):
            self.table.append([INDEL * (j + 1)])
            self.directions.append([None])
            self.endRow += 1

        
        #self.printTable()


    def diff(self, rowJ, colI):
        # print("in diff row is ", rowJ, " col is ", colI)
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
        stringJIndex = rowJ - 1 
        stringIIndex = colI - 1
        # print("rowj is ", rowJ, " colI is ", colI)
        diagonal = self.diff(stringJIndex, stringIIndex) + self.existingE(rowJ - 1, colI - 1)
        left = INDEL + self.existingE(rowJ, colI - 1)
        top = INDEL + self.existingE(rowJ - 1, colI)

        return self.minimum(left, top, diagonal)

    def fill(self):
        # print("filling table")
        # print("num rows ", len(self.table))
        # print("num cols ", len(self.table[0]))
        j = 1 
        while j < (len(self.table)):
            i = 1
            while i < (len(self.table[0])): 
                # print("j is ", j, " and i is ", i)
                self.table[j].append(self.currentE(j, i))
                self.directions[j].append(self.currentDirection)
                i += 1 
            j += 1
        
        #self.printTable()
    def setScore(self, rowJ, colI):
        self.score = self.table[rowJ][colI]

    def betterBuild(self, rowJ, colI):
        direction = self.directions[rowJ][colI]
        if direction == TOP:
            # self.iString += "-"
            # self.jString += self.seq2[rowJ]
            rowJ -= 1
            self.iString = self.iString[:colI] + "-" + self.iString[colI:]
            # self.build(rowJ - 1, colI)
        elif direction == LEFT:
            # self.iString += self.seq1[colI]
            # self.jString += "-"
            self.jString = self.jString[:rowJ] + "-" + self.jString[rowJ:]
            # self.build(rowJ, colI - 1)
            colI -= 1
        elif direction == DIAGONAL:
            # self.iString += self.seq1[colI]
            # self.jString += self.seq2[rowJ]
            # self.build(rowJ - 1, colI - 1)
            rowJ -= 1
            colI -= 1
        else:
            return

    def build(self, rowJ, colI):
        # print("row ", rowJ, " col ", colI)
        # print("rowlen ", len(self.table), ", col len", len(self.table[0]))
        self.score = self.table[rowJ][colI]
        while rowJ >= 0:
            while colI >= 0:
                direction = self.directions[rowJ][colI]
                if direction == None:
                    if rowJ > 0:
                        rowJ -= 1
                    if colI > 0:
                        colI -= 1
                    print("None value at row ", rowJ, ", colI ", colI)

                # # print(self.iString)
                # # print(self.jString)

                if direction == TOP:
                    # self.iString += "-"
                    # self.jString += self.seq2[rowJ]
                    rowJ -= 1
                    self.iString = self.iString[:colI] + "-" + self.iString[colI:]
                    # self.build(rowJ - 1, colI)
                elif direction == LEFT:
                    # self.iString += self.seq1[colI]
                    # self.jString += "-"
                    self.jString = self.jString[:rowJ] + "-" + self.jString[rowJ:]
                    # self.build(rowJ, colI - 1)
                    colI -= 1
                else:
                    # self.iString += self.seq1[colI]
                    # self.jString += self.seq2[rowJ]
                    # self.build(rowJ - 1, colI - 1)
                    rowJ -= 1
                    colI -= 1
                
                # if rowJ < 0 and colI >= 0:
                #     rowJ = 0
                # elif rowJ >= 0 and colI < 0:
                #     colI = 0




    def printTable(self):
        # print("weights")
        # print(self.seq1)
        i = 0
        for row in self.table:
            if(i == 0):
                print("- " , row)
            else:
                print(self.seq2[i - 1] , " " , row)
            i += 1
        
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
