import sys, os, random, analysis, math, bicycle
from tkinter import *

def addCard(event):
	inText = userInput.get().upper()
	if (len(inText) != 2):
		cardEntryWidget.select_range(0, END)
		print("ah shit mate your character count was fucked")
	else:
		try:
			suitDict = {'C': 0, 'S': 1, 'D': 2, 'H': 3}
			valDict = {'A': 1, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
			if inText[0] in valDict:
				tmpCard = bicycle.Card(valDict[inText[0]], suitDict[inText[1]])
			else:
				tmpCard = bicycle.Card(int(inText[0]), suitDict[inText[1]])
			#add the card to varHand
			if (len(varHand.bigHand) < 6):
				varHand.bigHand.append(tmpCard)
				print("added")
				cardEntryWidget.delete(0, END)	
		except (ValueError, KeyError):
			cardEntryWidget.select_range(0, END)
			print("ah shit mate your entry was fucked")

def calcUserEntry():
	if (len(varHand.bigHand) == 4):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze4Hand
	elif (len(varHand.bigHand) == 6):
		hPhase = analysis.handPhase(varHand)
		hPhase.analyze6Hand
	else:
		print("Yo you need 4 or 6 cards")

def calcRandomEntry():
	pass

def getImageFilename(card):
	x = "%s/gif/%s%02d.gif" % (os.getcwd(), card.getSuitChar(), card.value)
	print(x)
	return(x)


def updateCards(): #first, populate with all 6, then dim those who aren't the best (if known)
	
	cardID = [None] * 6
	count = 0
	for x in varHand.bigHand:
		xLoc = 85 + 110 * count #yLoc is 160
		if cards[count]:
			f = cards[count]
		else:
			f = PhotoImage(file=getImageFilename(x))

		cardID[count] = cardDisplay.create_image(xLoc, 90, image=f)
		cards[count] = f
	
		count += 1

def update():
	updateCards()
	root.after(500, update)


root = Tk()
#root.geometry("720x560")
varHand = bicycle.Hand()
hPhase = analysis.handPhase()
userInput = StringVar()
cards = [None] * 6 #keeps images on the canvas, needs to be here


Label(root, text="Enter Cards\n(JH is Jack of Hearts)").grid(row=0, column=0)

cardEntryWidget = Entry(root, width=4, textvariable=userInput)
cardEntryWidget.grid(row=1, column=0) #this returns None
root.bind('<Return>', addCard)

Button(root, text="Find Best", command=calcUserEntry).grid(row=2, column=0)
Button(root, text="Random", command=calcRandomEntry).grid(row=3, column=0)

#card display
cardDisplay = Canvas(root, width=720, height=180, bg='#084F3D')
cardDisplay.grid(row=5, rowspan=2, columnspan=2)


#run my loop
update()
root.mainloop()