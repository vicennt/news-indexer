#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle

clean_re = re.compile('\W+')
dictionary_terms = {}
dictionary_docs = {}
dictionary_news = {}


def load_data(file):
	global dictionary_terms, dictionary_docs, dictionary_news
	dictionary_terms, dictionary_docs, dictionary_news = pickle.load(open(index_file,'rb'))


def process_query(query):
	terms, operators, negation = parser(query)
	keys_news = [] 

	backup_terms = list(terms)

	if(negation):
		all_new_keys = []
		for tupla in dictionary_terms.items():
			all_new_keys.append(list(tupla[1].keys()))
	# If the query is a term
	if(len(terms) == 1):
		keys_news = [item[0] for item in dictionary_terms[query]]
		
	# If the query has an implicit and

	if(len(terms) > 1 and len(operators) == 0): 
		list1 = [item[0] for item in dictionary_terms[terms[0]]]
		list2 = [item[0] for item in dictionary_terms[terms[1]]]
		keys_news = intersection(list1, list2)
		del terms[0:2]
		while(len(terms) > 0):
			aux = [item[0] for item in dictionary_terms[terms[0]]]
			keys_news = intersection(keys_news, aux)
			terms.pop(0)
	else:
		print("TODO")

		'''
		if(operators[0] == "and"):
			keys_news = intersection(list1, list2)
		elif(operators[0] == "or"):
			keys_news = union(list1, list2)
		elif(operators[0] == "not")
		
		
		operators.pop(0)
		del terms[0:2]

		while(len(terms) > 0):
			aux = list(dictionary_terms[terms[0]].keys())
			keys_news = intersection(keys_news, aux)
			terms.pop(0)
		'''
	print(backup_terms)
	show_data(keys_news, backup_terms)

	# If the query has operators
	#TODO



def show_data(keys_news, terms):
	num_news = len(keys_news)

	ten_first = 0
	for i in keys_news:
		tupla = dictionary_news[i]
		path_doc = dictionary_docs[tupla[0]]
		position_new =  tupla[1]
		file = open(path_doc)
		content = file.read()
		news = content.split('<DOC>')
		news.pop(0) # Delete firs empty item
		new = news[position_new]
		# Extract data from the new
		title = new[new.index('<TITLE>') + 7 : new.index('</TITLE>')]
		text = new[new.index('<TEXT>') + 6 : new.index('</TEXT>')]
		text = clean_re.sub(' ', text) # Clean text
		
		if len(keys_news) <= 2:
			print(title + "\n")
			print(text)
		elif len(keys_news) <= 5:
			print(title + "\n")
			snippet_new(title, text, terms)
		elif len(keys_news) > 5:
			print(title + "\n")
			ten_first += 1
			if(ten_first == 10):
				break




# TODO: Snippet
def snippet_new(title, text, terms):
	for i in terms:
		snippet = "..." + text[text.index(terms[0]) - 30 : text.index(terms[0]) + 30] + "..."
		terms.pop(0)
		if(len(terms) > 0 and terms[0].find(terms[0]) != -1):
			print(snippet)
			terms.pop(0)
		else:
			print(snippet)


			

def parser(query):
	operators = [ "not","or", "and"]
	logical_operators = []
	terms_query = []
	negation = False

	query = query.lower()
	terms = query.split(" ")
	num_elements_query = len(terms)
	if(terms[0] == operators[0]):
		logical_operators.append(terms[0])
		terms.pop(0)
		num_elements_query -= 1 
		negation = True

	i = 0
	while(i < num_elements_query):
		if(query[0] in operators):
			logical_operators.append(terms[i])
		else:
			terms_query.append(terms[i])
		i += 1
	return terms_query, logical_operators, negation

def union(list1, list2):
	i = 0
	j = 0
	res = []
	while (i < len(list1) and j < len(list2)):
		if(list1[i] == list2[j]):
			res.append(list1[i])
			i+=1
			j+=1
		if(list1[i] <= list2[j]):
			res.append(list1[i])
			i+=1
		else:
			res.append(list2[j])
			j+=1
	while(i < len(list1)):
		res.append(i)
		i+=1
	while(j < len(list2)):
		res.append(list2[j])
		j+=1

	return res


def intersection(list1, list2):
	l1 = sorted(list1)
	l2 = sorted(list2)
	res = []
	i = 0
	j = 0
	while (i < len(l1) and j < len(l2)):
		if(l1[i] == l2[j]):
			res.append(l1[i])
			i += 1
			j += 1
		else:
			if(l1[i] < l2[j]):
				i += 1
			else:
				j += 1
	return res


if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
    	print("Usage: python sar_searcher.py <index_file>")
    else: 
    	index_file = sys.argv[1]
    	if not os.path.exists(index_file):
    		print("Error: The file " + index_file + " doesn't exist")
    		sys.exit(1)
    	load_data(index_file) 
    	while(True):
    		query = input("Enter your query: ")
    		if(not query):
    			break
    		process_query(query)

