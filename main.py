import sys 
import PyPDF2
from glob import glob

print("")	
stringToLookFor = sys.argv[1]
pdf_files = glob("**/*.pdf", recursive=True)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
		print("*** " + pdf + " ***")
		for result in matchResults:
			finalIndex = result.find(stringToLookFor)
			print(" " + "-" * (len(result)+6)) 
			print("|   " + result[0:finalIndex] + bcolors.FAIL + result[finalIndex:finalIndex+len(stringToLookFor)] + bcolors.ENDC + result[finalIndex+len(stringToLookFor):len(result)] + "   |")
			print(" " + "-" * (len(result)+6)) 
		print("")