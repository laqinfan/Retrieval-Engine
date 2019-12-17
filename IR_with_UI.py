# -------------------------------------------------------------------------

# Problem 1 [30 points]. 

# Develop a retrieval program that takes as input an user query in the form of 
# a set of keywords, uses the inverted index to retrieve documents containing
# at least one of the keywords, and then ranks these documents based on
# cosine values between query vector and document vectors. The output should be 
# a ranked list of documents with links to the original documents, i.e. URLs to
# the original documents on the web.

# Problem 2 [20 points]. 

# Develop a web interface to the program above.

# -------------------------------------------------------------------------

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from io import BytesIO
import base64
from plotly.tools import mpl_to_plotly

import os
import re
import string
import shutil
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import numpy as np

from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory

from collections import Counter
import math
import mmap

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

location = r'/Users/laqinfan/link'
filename = os.path.join(location, str('inverted_index.txt'))

inverted_index = {} #load inverted index into dictionary

#read inverted index into memory for searching
with open(filename, 'r') as f:
# 	# Size 0 will read the ENTIRE file into memory!
	m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

# 	# Proceed with your code here -- note the file is already in memory
# 	# so "readine" here will be as fast as could be
	for line in iter(m.readline, b""):
		line = line.decode("utf-8")
		print(line, type(line))
		tup = eval(line)
		inverted_index[tup[0]] = tup[1]

class Appearance:
	def __init__(self, dId, freq):
		self.docId = dId
		self.freq = freq

	def __repr__(self):
		return str(self.__dict__)

# Document/query preprocessing
def preprocess(text):
	stop_words = set(stopwords.words("english")) 
	remove_urls = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) #remove html or url
	remove_digits = re.sub(r'\d+', '', remove_urls) # Remove digits
	remove_punc = remove_digits.translate(str.maketrans('', '', string.punctuation)) #remove puncturation
	remove_upcase = remove_punc.lower() #remove upcases or text lowercase
	
	word_tokens = word_tokenize(remove_upcase)

	stemmer = PorterStemmer()
	stemming = []
	for word in word_tokens:
		stemming.append(stemmer.stem(word)) # stemming the texts

	remove_stopwords = [word for word in stemming if word not in stop_words] # remove stop words
	return remove_stopwords

app.layout = html.Div(children=[
	html.H1(children='Information Retrieval Demo'),

	html.Div(children = [ html.H4(f'Search:', style={'margin-left': '3px'}), dcc.Input(id='text-input', value='', type='text')
		], style={'width': '30%',}),

	html.Button('Search', id='button'),

	html.Div(children=[html.H4(f'Result(score, link): ', style={'margin-left': '3px'}),],
		style={'width': '48%'},
	),

	html.Div(id='model_output'),


	html.Div('   ',style={'display': 'inline-block'}),

])

@app.callback(
	Output(component_id='model_output', component_property='children'),
	[	
		Input(component_id='text-input', component_property='value'),
		Input('button', 'n_clicks')
	]
)
def update_output_div(query, click):
	document = {}
	docId = 1
	result = {}

	files = {}
	filelist = []

	print("search now!!!!!!!! \n")

	if click:
		process_query = preprocess(query) #preprocess the query

		print(process_query)

		location = r'/Users/laqinfan/link'
		R = {} #retrieval documents list
		length_q = {}
		idf_q= {}
		doc_length = {}

		N = 10000 # count of corpus

		num = 0

		#inverted-index retrieval algorithm
		for keyword in process_query:

			K = process_query.count(keyword) # the count of term in query
			if keyword in inverted_index:
				m = list(inverted_index[keyword].keys())[0]#num of documents with the keyword in it
				m = int(m)
				I = math.log(N/m) #idf

				W = K*I
				idf_q[keyword] = I

				length_q[keyword] = W*W

				L = list(inverted_index[keyword].values())[0]

				for entry in L:
					D = entry['docId']
					C = entry['freq']
					if D not in R:
						R[D] = 0.0
					R[D] += W*I*C  #increment D's score
					if D not in doc_length:
						doc_length[D] = (I*C)*(I*C)
					else:
						doc_length[D] +=(I*C)*(I*C)

			else:
				I = math.log((N+1)/1)
				num +=1
		if num == len(process_query):
			print("There is query term in the database!\n Please search new query.")

		#Compute the length of vector Q
		q_length = 0.0
		for term in process_query:
			unique_q = set(process_query)
			C = process_query.count(term)
			if term in idf_q.keys():

				I = idf_q[term]
			else:
				print("not in the doc!!!!")

			W = (C*I)*(I*C)
			q_length += W
		#normalize D's final score
		L = math.sqrt(q_length) # the length of vector Query

		for doc, score in R.items(): #calculate the final score by searching retrieved documents in R
			S = score
			Y = math.sqrt(doc_length[doc])
			R[doc] = S/(L*Y)

		
		filename1 = os.path.join(location, str('link.txt'))

		link_output = {}
		ranking_list =  sorted(R.items(), key=lambda kv: kv[1], reverse=True) #sorted the resluts
		for r in ranking_list[0:30]: #only rank the top 20 result based on the cosine similaities
			with open(filename1) as f:
				content = f.readlines()
				for line in content:
					if line != '\n':
						l = line.split(' ')
						if l[0].split('/')[-1] == r[0]:
							print( "score: ", r[1], " : ", l[1] )
							link_output[l[1]] = r[1]
		
		return [html.Li(html.A("Score: " + str(score) + "     " + link , href=link)) for link, score in link_output.items()]


if __name__ == '__main__':
	app.run_server(debug=True)