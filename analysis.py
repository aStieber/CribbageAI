import sys, os, math, random, itertools, bicycle, statistics

class handPhase():
	def __init__(self, _hand=None):
		self.deck = []
		if (_hand):
			self.myHand = _hand
		else:
			self.myHand = bicycle.Hand()
		self.cut = bicycle.Card()
		
		self.averageScore = 0
		self.bestScore = 0
		self.bestCut = bicycle.Card()

		#perm array for fifteencheck
		self.perms = [list(itertools.combinations(range(5), 2)), list(itertools.combinations(range(5), 3)), list(itertools.combinations(range(5), 4))]			
		self.genDeck(self.myHand)

	def genDeck(self, hand):
		for vl in range(1, 14): #value
			for st in range(4): #suit
				for c in hand.rawHand:
					if c.value != vl or c.suit != st:
						self.deck.append(bicycle.Card(vl, st))
						

	def analyze6Hand(self): #calculate ideal cribbage hand
		#calculate max score of all possible hands
		tmp4hands = []
		perms = list(itertools.combinations(self.myHand.rawHand, 4))
		currentBestHand = [bicycle.Hand()]
		for x in perms: #6 choose 2 means 15 possible arrangements
			#sort from low to high
			tmp4hands.append(bicycle.Hand())
			tmp4hands[-1].rawHand = list(x)
			scoreReport = self.score(tmp4hands[-1]) #(mean, bestScore, bestCard)
			tmp4hands[-1].averageScore  = scoreReport[0]
			tmp4hands[-1].bestScore  = scoreReport[1]
			tmp4hands[-1].bestCut  = scoreReport[2]

			#prefer average score. if tie, prefer max score. This should probably change later.
			if (tmp4hands[-1].averageScore > currentBestHand[0].averageScore): #if this hand is better than previous best, erase all and replace with this. Array must be cleared because best could contain multiple bests
				currentBestHand = [tmp4hands[-1]] #delete previous array and create new one with 1 item
			elif (tmp4hands[-1].averageScore == currentBestHand[0].averageScore):
				if (tmp4hands[-1].bestScore > currentBestHand[0].bestScore):
					currentBestHand = [tmp4hands[-1]] #delete previous array and create new one with 1 item
				elif (tmp4hands[-1].bestScore == currentBestHand[0].bestScore):
					currentBestHand.append(tmp4hands[-1])
		#end-for loop
		#find a better way than the first in the array
		if (len(currentBestHand) > 1):
			print("more than one best hand")


		for card in self.myHand.rawHand:
			enable = False
			for bc in currentBestHand[0].rawHand:
				if bc.value == card.value and bc.suit == card.suit:
					enable = True
					card.disabled = False
			if not enable:
				card.disabled = True



	def analyze4Hand(self): #calculate 4
		tmpHand = bicycle.Hand()
		for card in self.myHand.rawHand:
			if not card.disabled:
				tmpHand.rawHand.append(card)
		scoreReport = self.score(tmpHand)
		self.averageScore  = scoreReport[0]
		self.bestScore  = scoreReport[1]
		self.bestCut  = scoreReport[2]
	
	def score(self, potentialHand):
		#run check
		#15 check
		#pair/triplet/quad check
		#Nobs check (jack same suit as cut)
		#Flush check
		scores = []
		bScore = 0
		bCut = bicycle.Card()
		#run check
		for cut in self.deck:
			#create the full hand
			fiveHand = bicycle.Hand()
			for x in potentialHand.rawHand:
				fiveHand.rawHand.append(x)
			fiveHand.rawHand.append(cut)
			fiveHand.handSort()

			tmpScore = self.runCheck(fiveHand)
			tmpScore += self.fifteenCheck(fiveHand)
			tmpScore += self.multiplesCheck(fiveHand)
			#These two are weird because scoring depends on which card is the cut. Thus, we have to pass in both.
			tmpScore += self.nobsCheck(potentialHand.rawHand, cut) 
			tmpScore += self.flushCheck(potentialHand.rawHand, cut)
			scores.append(float(tmpScore))
			if (tmpScore > bScore):
				bScore = tmpScore
				bCut = cut
		output = (statistics.mean(scores), bScore, bCut)
		return(output)
		
	def runCheck(self, fHand): #size 5 hand
		currentRunLength = 0
		counter = -1
		#cycle through remaining deck, calculate the deck with the highest average score.
		while (True):
			if (currentRunLength == 5 or counter == -5):
				break
			elif (fHand.rawHand[counter].value == (fHand.rawHand[counter - 1].value + 1)): #if last item is 1 larger than previous
				if ((counter <= -4) and (fHand.rawHand[counter].value != (fHand.rawHand[counter + 1].value - 1))):
					break#check against 87643 counting as 4 points

			currentRunLength += 1
			counter -= 1
		else:
				counter -= 1
		#current run length is longest run
		if (currentRunLength >= 3): return (currentRunLength)
		else: return(0)

	def fifteenCheck(self, fHand):#cards are in fHand.rawHand
		score = 0
		for x in self.perms:
			for permList in x:
				tmpCount = 0
				for num in permList:
					tmpCount += fHand.rawHand[num].getGameValue()
				if (tmpCount == 15):
					score += 2
		return(score)

	def multiplesCheck(self, fHand):
		score = 0
		for x in self.perms[0]: #5 choose 2
			if (fHand.rawHand[x[0]].value == fHand.rawHand[x[1]].value):
				score += 2
		return(score)

	def nobsCheck(self, fourHand, cut): #this one is weird because it requires a hand card match a cut
		for card in fourHand:
			if (card.value == 11 and card.suit == cut.suit): #if card is a jack and matches the suit of the cut
				return(1)
		return(0)

	def flushCheck(self, fourHand, cut): #A four-card flush occurs when all of the cards in a player's hand are the same suit and the start card is a different suit. In the crib, a four-card flush scores no points. A five-card flush scores five points.
		if (fourHand[0].suit == fourHand[1].suit == fourHand[2].suit == fourHand[3].suit):
			if (fourHand[0].suit == cut.suit):
				return(5)
			return(4)
		return(0)