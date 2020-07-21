import sys 
import PyPDF2

try :
	src = sys.argv[1]
except :
	src = r'~/Applications/yoFinder/test.pdf'

input1 = PyPDF2.PdfFileReader(open(src, "rb"))
nPages = input1.getNumPages()

for i in range(nPages) :
# get the data from this PDF page (first line of text, plus annotations)
	page = input1.getPage(i)
	text = page.extractText()

#	print(text.splitlines()[0])
#	print('')	

	try :
		for annot in page['/Annots'] :
		# Other subtypes, such as /Link, cause errors
			subtype = annot.getObject()['/Subtype']
			if subtype == "/Text":
				print(annot.getObject()['/Contents'])
	#	print('')
	except :
	# there are no annotations on this page
		pass

# print('')