import sys, os, random, analysis, math, bicycle
from tkinter import *

def addCard(event):
	inText = userInput.get().upper()
	if (len(inText) != 2):
		cardEntryWidget.select_range(0, END)
		print("incorrect character count")
	else:
		try:
			suitDict = {'C': 0, 'S': 1, 'D': 2, 'H': 3}
			valDict = {'A': 1, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
			if inText[0] in valDict:
				tmpCard = bicycle.Card(valDict[inText[0]], suitDict[inText[1]])
			else:
				tmpCard = bicycle.Card(int(inText[0]), suitDict[inText[1]])
			#add the card to varHand
			if (len(varHand.rawHand) < 6):
				if not duplicateCheck(tmpCard, varHand):
					varHand.rawHand.append(tmpCard)
					print("added")
					cardEntryWidget.delete(0, END) #erase text box						
		except (ValueError, KeyError):
			cardEntryWidget.select_range(0, END)
			print("invalid character")

def calcUserEntry():
	if (len(varHand.rawHand) == 4):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze4Hand()
		updateTextOutput(hPhase)
	elif (len(varHand.rawHand) == 6):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze6Hand()
		updateTextOutput(hPhase)
	else:
		print("Yo you need 4 or 6 cards, you have %i cards" % len(varHand.rawHand))

def updateTextOutput(hPhase):
	tmpText = "Average Score: %.2f\nBest Score: %i\n" % (hPhase.averageScore, hPhase.bestScore)
	tmpText += "Best Cut: " + hPhase.bestCut.valChart[hPhase.bestCut.value] + " of " + hPhase.bestCut.getSuitChar()
	textOutput.set(tmpText)

def duplicateCheck(card, hand):
	duplicateCard = False
	for x in hand.rawHand:
		if x.value == card.value and x.suit == card.suit:
			duplicateCard = True
	return(duplicateCard)

def calcRandomEntry(num):
	global varHand, cards
	varHand = bicycle.Hand()
	cards = [None] * 6
	counter = 0
	while counter < num:
		tmpCard = bicycle.Card(_value=random.randint(1, 13), _suit=random.randint(0, 3))
		if not duplicateCheck(tmpCard, varHand):
			varHand.rawHand.append(tmpCard)
			cardEntryWidget.delete(0, END) #erase text box
			counter += 1

def getImageFilename(card):
	x = "%s/gif/%s%02d.gif" % (os.getcwd(), card.getSuitChar(), card.value)
	return(x)


def updateCards(): #first, populate with all 6, then dim those who aren't the best (if known)
	cardID = [None] * 6
	count = 0
	for x in varHand.rawHand:
		xLoc = 60 + 110 * count #yLoc is 160
		if cards[count]:
			f = cards[count]
		else:
			f = PhotoImage(file=getImageFilename(x))

		cardID[count] = cardDisplay.create_image(xLoc, 90, image=f)
		cards[count] = f
	
		count += 1


def update():
	updateCards()
	#cardDisplay.update()
	root.update_idletasks()
	root.after(500, update)




root = Tk()
#root.geometry("720x560")
varHand = bicycle.Hand()
hPhase = analysis.handPhase()
userInput = StringVar()
cards = [None] * 6 #keeps images on the canvas, needs to be here
textOutput = StringVar()


Label(root, text="Enter Cards\n(JH is Jack of Hearts)").grid(row=0, column=0)

cardEntryWidget = Entry(root, width=4, textvariable=userInput)
cardEntryWidget.grid(row=1, column=0) #this returns None
root.bind('<Return>', addCard)

Button(root, text="Find Best", command=calcUserEntry).grid(row=2, column=0)
Button(root, text="Random 4", command=lambda: calcRandomEntry(4)).grid(row=0, column=1)
Button(root, text="Random 6", command=lambda: calcRandomEntry(6)).grid(row=1, column=1)

#card display
cardDisplay = Canvas(root, width=720, height=180, bg='#084F3D')
cardDisplay.grid(row=5, rowspan=2, columnspan=5)

statDisplay = Label(root, textvariable=textOutput).grid(row=0, column=2, rowspan=2, columnspan=2)


#run my loop
update()
root.mainloop()