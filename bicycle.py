#contains Card and Hand objects
import sys, os


class Card(object):
	def __init__(self, val=1, sui=0):
		self.value = val
		self.suit = sui
		#Ace is 1, J is 11, Q is 12, K is 13
		self.valChart = [None, "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
		#0: club, 1: spade, 2: diamond, 3: heart
		self.suitChart = ["c", "s", "d", "h"]

	def getGameValue(self): #score of the card. reduces jqk
		tmpV = self.value
		if (self.value > 10):
			tmpV = 10
		return(tmpV)

	def getSuitChar(self):
		return(self.suitChart[self.suit])

	def printCard(self):
		print(self.valChart[self.value], "of", self.suitChart[self.suit])

class Hand(object):
	def __init__(self):
		self.bigHand = []
		self.idealHand = []
		self.averageScore = 0
		self.bestScore = 0
		self.bestCut = Card()

	def handSort(self):
		self.bigHand.sort(key=lambda x: x.value)
		self.idealHand.sort(key=lambda x: x.value)

	def printHand(self):
		if (self.averageScore):
			print("Average Score: %.2f" % self.averageScore)
		if (self.bigHand):
			print("bigHand:")
			for x in self.bigHand:
				x.printCard()
		if (self.idealHand):
			print("idealHand:")
			for y in self.idealHand:
				y.printCard()
