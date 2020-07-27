from tkinter import *
from tkinter import filedialog
from pathlib import Path
from glob import glob
import PyPDF2
import os

fileNumber = 0
resultNumber = 0
targetDirectory = Path.cwd()
print("Target directory currently is " + str(targetDirectory))
# print(Path.cwd().parent)
#print(Path.cwd().parent.rglob("*.pdf"))

window = Tk()
window.title("pdfCommentFinder")
window.geometry("600x400")

canvas = Canvas(window, highlightthickness=0)
canvas.pack(side=LEFT)
scrollbar = Scrollbar(window, command=canvas.yview)
scrollbar.pack(side=LEFT, fill='y')
canvas.configure(yscrollcommand=scrollbar.set)
frame = Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'),width=580, height=400)

def setDirectory():
	global targetDirectory 		
	global pathBox
	targetDirectory = Path(r''+filedialog.askdirectory())
	print("Target directory was changed to " + str(targetDirectory))
	
	pathBox.destroy()
	pathBox = Label(frame, text="Searching in " + str(targetDirectory), wraplength=500)
	pathBox.grid(row=0, column=0, pady=(10,0),padx=(27,0))


def setWidgets():
	global pathBox
	pathBox = Label(frame, text="Searching in " + str(targetDirectory), wraplength=500)
	pathBox.grid(row=0, column=0, pady=(10,0),padx=(27,0))

	global inputBar
	inputBar = Entry(frame, width=53)
	inputBar.grid(row=1, column=0, padx=27, pady=(10,0))

	Button(frame, text='Find Comment', command=lookupTerm, width=25).grid(row=2, column=0, pady=(5,0), padx=5)

	Button(frame, text='Select Directory', command=setDirectory, width=25).grid(row=3, column=0, pady=(5,0), padx=5)

	Button(frame, text='Clear Results', command=clearResults, width=25).grid(row=4, column=0, pady=(5,0), padx=5)

def lookupTerm():
	global fileNumber
	global resultNumber
	global targetDirectory
	# os.chdir(targetDirectory)
	# os.chdir("C:\\Users\\Utilisateur\\Documents\\Témoignage\\Patapoésie\\Journal d'un patapoète")
	pdf_files = targetDirectory.rglob("*.pdf")
	# pdf_files = Path.cwd().rglob("*.pdf")
	stringToLookFor = inputBar.get()
	print("Looking for '" + stringToLookFor +"' in " + str(targetDirectory))
	for pdf in pdf_files:
		input1 = PyPDF2.PdfFileReader(open(pdf, "rb"))
		nPages = input1.getNumPages()
		matchNumber = 0
		matchResults = []
		for i in range(nPages) :
		# get the data from this PDF page (first line of text, plus annotations)
			page = input1.getPage(i)
			text = page.extractText()
			try :
				for annot in page['/Annots'] :
				# Other subtypes, such as /Link, cause errors
					subtype = annot.getObject()['/Subtype']
					if subtype == "/Text":
						CommentContents = annot.getObject()['/Contents']
						matchStartIndex = CommentContents.find(stringToLookFor)
						resultPadding = 15
						if matchStartIndex != -1:
							matchNumber = matchNumber + 1
							if matchStartIndex - resultPadding < 0: 
								returnStartIndex = matchStartIndex - resultPadding + (-(matchStartIndex - resultPadding))
							else:
								returnStartIndex = matchStartIndex - resultPadding
							matchResults.append(CommentContents[returnStartIndex:matchStartIndex+resultPadding+len(stringToLookFor)])
			except :
			# there are no annotations on this page
				pass
		if matchNumber > 0:
			fileNumber = fileNumber + 1
			fileBox = Label(frame, text=pdf, font=("Arial Bold", 11), wraplength=500)
			fileBox.grid(row=5 + fileNumber + resultNumber, column=0, pady=(10,0),padx=(38,0))
			for result in matchResults:
				finalIndex = result.find(stringToLookFor)
				resultNumber = resultNumber + 1
				resultRow = 5 + fileNumber + resultNumber
				global resultBox
				resultBox = Text(frame, height=1, width=40, relief=RIDGE)
				resultBox.insert(INSERT,result)
				resultBox.config(state=DISABLED)
				resultBox.tag_add("color","1."+str(finalIndex), "1."+str(finalIndex+len(stringToLookFor)))
				resultBox.tag_config("color",foreground="red")
				resultBox.grid(row=resultRow, column=0)

def clearResults():
	matchNumber = 0
	fileNumber = 0
	resultNumber = 0
	for widget in frame.winfo_children():
		widget.destroy()
	setWidgets()

def pressEnter(event):
	lookupTerm()

window.bind('<Return>', pressEnter)
window.bind('<Configure>', on_configure)

setWidgets()

window.mainloop()