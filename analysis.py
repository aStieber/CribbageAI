import sys, os, math, random, itertools, bicycle, statistics

class handPhase():
	def __init__(self, testing):
		self.deck = []
		self.myHand = bicycle.Hand()
		self.cut = bicycle.Card()
		#testing
		if (testing):
			self.genState()
		else: getBoard()

		self.analyzeHand()

		
	def genState(self): #create a deck and fill 2 hands, draw crib. Returns the cut.
		#generate the deck (ordered)
		for vl in range(1, 14): #value
			for st in range(4): #suit
				self.deck.append(bicycle.Card(vl, st))

		deckCount = len(self.deck) - 1
		random.shuffle(self.deck) #shuffle the deck
		
		#deal my hand
		for c in range(6): 
			self.myHand.bigHand.append(self.deck.pop(random.randint(0, deckCount)))
			deckCount -= 1
		self.cut = self.deck.pop(random.randint(0, deckCount))


	def analyzeHand(self): #calculate ideal cribbage hand
		#calculate max score of all possible hands
		tmp4hands = []
		perms = list(itertools.combinations(self.myHand.bigHand, 4))
		currentBestHand = [bicycle.Hand()]
		for x in perms: #6 choose 2 means 15 possible arrangements
			#sort from low to high
			tmp4hands.append(bicycle.Hand())
			tmp4hands[-1].idealHand = list(x)
			tmp4hands[-1].averageScore = self.score(tmp4hands[-1])

			if (tmp4hands[-1].averageScore > currentBestHand[0].averageScore): #if this hand is better than previous best, erase all and replace with this. Array must be cleared because best could contain multiple bests
				currentBestHand = [tmp4hands[-1]]
			elif (tmp4hands[-1].averageScore > currentBestHand[0].averageScore):
				currentBestHand.append(tmp4hands[-1])

		currentBestHand[0].printHand()

		#decide ties in currentBestHand
		#print state

	
	def score(self, potentialHand):
		#run check
		#15 check
		#pair/triplet/quad check
		#Nobs check (jack same suit as cut)
		#Flush check
		scores = []
		
		#run check
		for cut in self.deck:
			tmpScore = self.runCheck(potentialHand, cut)
			# tmpScore += self.fifteenCheck(potentialHand, cut)
			# tmpScore += self.multiplesCheck(potentialHand, cut)
			# tmpScore += self.nobsCheck(potentialHand, cut)
			# tmpScore += self.flushCheck(potentialHand, cut)
			scores.append(tmpScore)



		return(statistics.mean(scores))
		

	def runCheck(self, potentialHand, cut): #size 4 hand
		currentRunLength = 0
		fiveHand = bicycle.Hand()
		for x in potentialHand.idealHand:
			fiveHand.bigHand.append(x)
		fiveHand.bigHand.append(cut)
		fiveHand.handSort()
		counter = -1
		#cycle through remaining deck, calculate the deck with the highest average score.
		while (True):
			if (currentRunLength == 5 or counter == -5):
				break
			elif (fiveHand.bigHand[counter].value == (fiveHand.bigHand[counter - 1].value + 1)): #if last item is 1 larger than previous'
				currentRunLength += 1
				counter -= 1
			elif (currentRunLength >= 3):
				break
			else:
				counter -= 1
		#current run length is longest run
		if (currentRunLength >= 3): return (currentRunLength)
		else: return(0)
				


