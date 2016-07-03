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
	setHandChanged(True)

def calcCardDisplay():
	enabledCards = 0
	for card in varHand.rawHand:
		if not card.disabled:
			enabledCards += 1
	if (enabledCards == 4):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze4Hand()
		updateTextOutput(hPhase)
	elif (enabledCards == 6):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze6Hand()
		updateTextOutput(hPhase)
		varHand.rawHand
	else:
		textOutput.set("")
		#print("you need 4 or 6 cards, you have %i cards" % len(varHand.rawHand))

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
	global varHand
	varHand = bicycle.Hand()
	counter = 0
	while counter < num:
		tmpCard = bicycle.Card(_value=random.randint(1, 13), _suit=random.randint(0, 3))
		if not duplicateCheck(tmpCard, varHand):
			varHand.rawHand.append(tmpCard)
			cardEntryWidget.delete(0, END) #erase text box
			counter += 1
	setHandChanged(True)

def updateCards(): #first, populate with all 6, then dim those who aren't the best (if known)
	tmp = []
	yLoc = 20
	count = 0
	for x in varHand.rawHand:
		xLoc = 14 + 110 * count 
		count += 1
		if not x.imageExists:
			x.createImage(xLoc, yLoc)
		cardDisplay.create_image(xLoc, yLoc, image=x.imageObj.image, anchor='nw')

		if x.disabled:
			tmp.append(cardDisplay.create_rectangle(xLoc, yLoc, x.imageObj.width + xLoc, x.imageObj.height + yLoc, stipple='gray75', fill='#000000'))

def cardClick(event, card):
	if event.x >= card.imageObj.x and event.x <= (card.imageObj.x + card.imageObj.width):
		if event.y >= card.imageObj.y and event.y <= (card.imageObj.y + card.imageObj.height):
			return(True)
	return(False)

def __toggleCardEnable(event):
	for card in varHand.rawHand:
		#cardDisplay.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='orange')
		if cardClick(event, card):
			#card was clicked
			card.disabled = not card.disabled
	setHandChanged(True)

def __removeCard(event):
	removed = False
	for card in varHand.rawHand[:]:
		if cardClick(event, card):
			varHand.rawHand.remove(card)
			removed = True
	if removed:
		for card in varHand.rawHand:
			card.imageObj = None
			card.imageExists = False
	setHandChanged(True)

def getHandChanged():
	global handChanged
	return(handChanged)

def setHandChanged(setValue):
	global handChanged
	handChanged = setValue

def update():
	if getHandChanged():
		updateCards()
		calcCardDisplay()
		setHandChanged(False)
	root.after(20, update)



#__main__
root = Tk()
#root.geometry("720x560")
varHand = bicycle.Hand()
hPhase = analysis.handPhase()
handChanged = False
userInput = StringVar()
textOutput = StringVar()



Label(root, text="Enter Cards\n(JH is Jack of Hearts)").grid(row=0, column=0)

cardEntryWidget = Entry(root, width=4, textvariable=userInput)
cardEntryWidget.grid(row=1, column=0) #this returns None
root.bind('<Return>', addCard)

#Button(root, text="Find Best", command=calcUserEntry).grid(row=2, column=0)
Button(root, text="Random 4", command=lambda: calcRandomEntry(4)).grid(row=0, column=1)
Button(root, text="Random 6", command=lambda: calcRandomEntry(6)).grid(row=1, column=1)

#card display
cardDisplay = Canvas(root, width=780, height=180, bg='#084F3D')
cardDisplay.grid(row=5, rowspan=2, columnspan=5)
cardDisplay.bind('<Button-1>', __toggleCardEnable)
cardDisplay.bind('<Button-3>', __removeCard)

statDisplay = Label(root, textvariable=textOutput).grid(row=0, column=2, rowspan=2, columnspan=2)


#run my loop
update()
root.mainloop()