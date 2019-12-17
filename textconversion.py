import requests
import os
import mimetypes
from nltk import word_tokenize
from bs4 import BeautifulSoup
from bs4.element import Comment

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import html2text

import PyPDF2
import re

#the seed website
seed = "https://www.memphis.edu"
# seed = "http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"

#If there is no such folder, the script will create one automatically
text_location = r'/Users/laqinfan/text_file8'
if not os.path.exists(text_location):os.mkdir(text_location)

pdf_location = r'/Users/laqinfan/pdf_file8'
if not os.path.exists(pdf_location):os.mkdir(pdf_location)

#If there is no such folder, the script will create one automatically
html_location = r'/Users/laqinfan/html_file8'
if not os.path.exists(html_location):os.mkdir(html_location)

doc_list = {} # map link with the file name
doc_list1 = {} # map link with the file name

#convert pdf file to text file
def pdf_text(pdf_path):

	pdfFileObj = open(pdf_path,'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	if not pdfReader.isEncrypted:

		num_pages = pdfReader.numPages

		return u" ".join(pdfReader.getPage(i).extractText() for i in range(num_pages))

#store the link list in local file, which has the mapping of link and file name
location = r'/Users/laqinfan/test_link8'
filename = os.path.join(location, str('link.txt'))

with open(filename) as f:
	content = f.readlines()
	for line in content:
		if line != '\n':
			l = line.split(' ')
			doc_list[l[0]] = l[1]

#To convert pdf files to text files
entries = os.listdir(pdf_location)
for filename in entries:
	if str(filename).endswith('.pdf'):
		value = pdf_text(pdf_location+'/'+str(filename))
		filename1 = os.path.join(text_location, str(filename).split('.')[0] + '.txt')

		f = open(filename1, 'wb')
		f.write(value.encode('utf8'))
		filename2 = os.path.join(pdf_location+'/'+str(filename))
		doc_list1[filename1] = doc_list[filename2]

#To convert html files to text files
entries1 = os.listdir(html_location)
for filename in entries1:
	if str(filename).endswith('.html'):
		htmlForRender = open(html_location+'/'+str(filename), encoding="utf8", errors='ignore').read()

		soup = BeautifulSoup(htmlForRender, "html.parser")
		all_p = soup.find_all('p')

		text1 = ''
		for x in all_p:
		    text1 = text1 + x.text
		# text1 = text1.strip()

		text1 = " ".join(text1.split())

		tokens = word_tokenize(text1)
		if len(tokens)> 50:# only keep documents with at least 50 textual tokens
			# Name the files using the last portion of each link which are unique in this case
			filename1 = os.path.join(text_location, str(filename).split('.')[0] + '.txt')
			with open(filename1, 'w') as f:
				print("html: ",str(filename1))
				f.write(text1)
				doc_list1[filename1] = doc_list[html_location+'/'+str(filename)]

count = 0
for name, link in doc_list1.items():
	print("========: ", name, "--", link, "----", count)
	count +=1


#store the link list in local file, which has the mapping of link and file name
location = r'/Users/laqinfan/test_link8'

filename = os.path.join(location, str('link8.txt'))
with open(filename, 'w') as f:
	for item in doc_list1.items():
		f.write(' '.join(item))
		f.write('\n')









