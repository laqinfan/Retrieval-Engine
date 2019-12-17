
import os
import re
import string
import shutil
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import nltk

files = {}
filelist = []
new_files = {}
doc_list = {} # map link with the file name
doc_list1 = {} # map link with the file name


path = r'/Users/laqinfan/text_file8/'
entries = os.listdir(path)
for filename in entries:
	filelist.append(str(filename))

#read files into files dictonary mapping the file name with its content
for filename in filelist:
	with open(path+filename, 'r', encoding = 'utf8', errors = 'ignore') as file:
		if filename in files:
			continue
		files[filename] = file.read()


#get the link mapping with the file info into a dictionary
link_location = r'/Users/laqinfan/test_link8'

filename = os.path.join(link_location, str('link8.txt'))

with open(filename) as f:
	content = f.readlines()
	for line in content:
		if line != '\n':
			l = line.split(' ')
			doc_list[l[0]] = l[1]

# Document preprocessing
def preprocess(text):
	stop_words = set(stopwords.words("english"))
	remove_urls = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) #remove html or url
	remove_digits = re.sub(r'\d+', '', remove_urls) # Remove digits
	remove_punc = remove_digits.translate(str.maketrans('', '', string.punctuation)) #remove puncturation
	remove_upcase = remove_punc.lower() #remove upcases or text lowercase

	english_words = ''

	for w in remove_upcase.split():
		if wordnet.synsets(w):
			english_words = english_words + ' ' + w
	
	word_tokens = word_tokenize(english_words)

	stemmer = PorterStemmer()
	stemming = []
	for word in word_tokens:
		stemming.append(stemmer.stem(word)) # stemming the texts

	remove_stopwords = [word for word in stemming if word not in stop_words] # remove stop words

	return remove_stopwords

words = set(nltk.corpus.words.words())

count = 0
for filename, text in files.items():

	print("==========", count)
	count +=1
	new_files[filename] = preprocess(text)# use a new dictonary to map the filename with pre-processed texts
	
#store the preprocessed file
location = r'/Users/laqinfan/preprocessed/'
if not os.path.exists(location):os.mkdir(location)

for filename, text in new_files.items():
	print("\n",filename)
	filename1 = os.path.join(location, str(filename))
	filename2 = os.path.join(path, str(filename))
	doc_list1[filename1] = doc_list[filename2]

	with open(filename1, 'w') as f:

		f.write(' '.join(text))
		# f.write(' '.join(str(item) for item in text))

#store the link list in local file, which has the mapping of link and file name
location = r'/Users/laqinfan/test_link8'

filename = os.path.join(location, str('link9.txt'))
with open(filename, 'w') as f:
	for item in doc_list1.items():
		f.write(' '.join(item))
