#!/usr/bin/python3

from which_pyqt import PYQT_VER
from weights import *
from UnbandedSequencer import UnbandedSequencer
from BandedSequencer import BandedSequencer

if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

class GeneSequencing:

	def __init__( self ):
		pass

	
# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment

	def align( self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		results = []
		

		# sequencer = UnbandedSequencer(sequences[0], sequences[1])
		# print(sequencer.seq1)
		# print(sequencer.seq2)
		# sequencer.fill()
		# sequencer.printTable()
		# row = len(sequencer.table) - 1
		# col = len(sequencer.table[0]) - 1
		# sequencer.printTable()
		# sequencer.build(row, col)
		# alignment1 = sequencer.iString
		# alignment2 = sequencer.jString
		# print(alignment1)
		# print(alignment2)
		# score = sequencer.score
		# print(score)
		# sequencer.reverseStrings()
		
		for i in range(len(sequences)):
		# for i in range(1):
			jresults = []
			for j in range(len(sequences)):
			# for j in range(2):

				if(j < i):
					s = {}
				else:
					# if i == 2 and j == 7:
					# 	s = {'align_cost':69, 'seqi_first100':sequences[i][:100], 'seqj_first100':sequences[i][:100]}
					# 	table.item(i,j).setText('{}'.format(int(69) if 69 != math.inf else 69))
					# 	table.update()	
					# else:
					print("at ", i , " and ", j)
###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
					if banded:
						sequencer = BandedSequencer(sequences[i][:align_length], sequences[j][:align_length])
						# sequencer.printBand()
						print("filling band")
						sequencer.fill()
						print("done filling band")
						# sequencer.printBand()
						sequencer.build()
						alignment1 = sequencer.iString
						alignment2 = sequencer.jString
						score = sequencer.score

						if(len(alignment1) - len(alignment2)) > 100:
							alignment1 = "No Alignment Possible"
							alignment2 = "No Alignment Possible"
							score = math.inf
						else:
							if(len(alignment1) > 100):
								alignment1 = alignment1[:100]
							alignment2 = sequencer.jString
							if(len(alignment2) > 100):
								alignment2 = alignment2[:100]
						
						s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
						table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
						table.update()
					else:
						sequencer = UnbandedSequencer(sequences[i][:align_length], sequences[j][:align_length])
						# print(sequencer.seq1)
						# print(sequencer.seq2)
						print("filling")
						sequencer.fill()
						print("done filling")
						# sequencer.printTable()
						row = len(sequencer.table) - 1
						col = len(sequencer.table[0]) - 1
						# sequencer.printTable()
						print("building at ", row, " , ", col)
						sequencer.build(row, col)
						print("done building")
						alignment1 = sequencer.iString
						if(len(alignment1) > 100):
							alignment1 = alignment1[:100]
						alignment2 = sequencer.jString
						if(len(alignment2) > 100):
							alignment2 = alignment2[:100]
						print("alignment1 ", alignment1)
						print("alignment2 ", alignment2)
						score = sequencer.score
						print("score ", score)
						# alignment1 = 'abc-easy  DEBUG:(seq{}, {} chars,align_len={}{})'.format(i+1,
						# 	len(sequences[i]), align_length, ',BANDED' if banded else '')
						# alignment2 = 'as-123--  DEBUG:(seq{}, {} chars,align_len={}{})'.format(j+1,
						# 	len(sequences[j]), align_length, ',BANDED' if banded else '')
	###################################################################################################					
						s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
						table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
						table.update()	
				jresults.append(s)
			results.append(jresults)
		return results




