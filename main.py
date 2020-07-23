import sys 
import PyPDF2
from glob import glob

print("")	
stringToLookFor = sys.argv[1]
pdf_files = glob("**/*.pdf", recursive=True)
# print(pdf_files) 

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
					if CommentContents.find(stringToLookFor) != -1:
						matchNumber = matchNumber + 1
						startIndex = CommentContents.find(stringToLookFor)
						matchResults.append(CommentContents[startIndex:startIndex+15])
		except :
		# there are no annotations on this page
			pass

	if matchNumber > 0:
		print("*** " + pdf + " ***")
		for result in matchResults:
			print(" " + "-" * (len(result)+6)) 
			print("|   " + result + "   |")
			print(" " + "-" * (len(result)+6)) 
		print("")