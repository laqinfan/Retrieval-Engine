import requests
import os
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment

from collections import deque
import mimetypes
from nltk import word_tokenize

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

#the seed website
seed = "https://www.memphis.edu/cs/people/faculty_pages/lan-wang.php"
# seed = "http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"

#If there is no such folder, the script will create one automatically
text_location = r'/Users/laqinfan/text_file8'
if not os.path.exists(text_location):os.mkdir(text_location)

pdf_location = r'/Users/laqinfan/pdf_file8'
if not os.path.exists(pdf_location):os.mkdir(pdf_location)

#If there is no such folder, the script will create one automatically
html_location = r'/Users/laqinfan/html_file8'
if not os.path.exists(html_location):os.mkdir(html_location)


visited = set([seed])
dq = deque([[seed, "", 0]]) #initiate a queue to store web link
max_depth = 2 # the tree depth to search

doc_list = {} # map link with the file name
unique_list = [] #unique list for webpage
count = 12350 # record the document number

# main breadth first search entry
while dq:
	base, path, depth = dq.popleft()

	if depth < max_depth:
		try:
			soup = BeautifulSoup(requests.get(base + path).text, "html.parser")

			# get all the <a> tags in current web page
			for link in soup.find_all("a"):
				href = link.get("href")
				join_url = urljoin(base, href)
				if join_url not in unique_list:
					unique_list.append(join_url)

					response = urlopen(join_url)
					if response.info().get_content_type() == 'text/html':
						if urlparse(link.get('href')).fragment == '': # remove  href with fragment
							print("html: ",join_url)
							# Name the files using the last portion of each link which are unique in this case
							filename = os.path.join(html_location,str(count) + ".html") #name the file
							with open(filename, 'wb') as f:
								f.write(requests.get(urljoin(base,href)).content)
								doc_list[filename] = join_url 
								count +=1
								if count == 15000:
									break
							print("count: ", count)
					elif response.info().get_content_type() == 'text/plain': #handle the text files
						filename = os.path.join(text_location,link['href'].split('/')[-1]) #name the file
						text = requests.get(urljoin(base,href)).content
							
						with open(filename, 'wb') as f:
							print("text: ",join_url)
							f.write(text)
							doc_list[filename] = join_url
							count +=1
							if count == 15000:
								break
						print("count: ", count)
					elif response.info().get_content_type() == 'application/pdf': # handle pdf files
						filename = os.path.join(pdf_location,link['href'].split('/')[-1]) #name the file
						text = requests.get(urljoin(base,href)).content
						with open(filename, 'wb') as f:
							print("pdf: ",join_url)
							f.write(text)
							doc_list[filename] = join_url
							count +=1
							if count == 15000:
								break
						print("count: ", count)
					
				if href not in visited:
					visited.add(href)

					#add new link into queue to process
					if href.startswith("http"):
						dq.append([href, "", depth + 1])
					else:
						dq.append([base, href, depth + 1])

			if count == 15000:
				break
		except:
			pass

#store the link list in local file, which has the mapping of link and file name
location = r'/Users/laqinfan/test_link8'
if not os.path.exists(location):os.mkdir(location)


filename = os.path.join(location, str('link7.txt'))
with open(filename, 'w') as f:
	for item in doc_list.items():
		f.write(' '.join(item))
		f.write('\n')










