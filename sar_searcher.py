#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle

clean_re = re.compile('\W+')
dictionary_terms = {}
dictionary_docs = {}
dictionary_news = {}
dictionary_headline = {}
dictionary_date = {}
dictionary_categories = {}



def load_data(file):
	global dictionary_terms, dictionary_docs, dictionary_news
	dictionary_terms, dictionary_docs, dictionary_news, dictionary_headline, dictionary_date, dictionary_categories = pickle.load(open(index_file,'rb'))
		

def parser(query):
	logic_operators = ["and", "not", "or"]
	lista = query.split(" ")
	terms = []
	operators = []
	first_negation = lista[0] == "not"

	i = 0
	while(i < len(lista) -1):
		if(lista[i] not in logic_operators and lista[i+1] not in logic_operators):
			terms.append(lista[i])
			operators.append("and")
			i+=1
		elif(lista[i] in logic_operators and lista[i+1] in logic_operators):
			operators.append(lista[i] + lista[i+1])
			i+=2
		else:
			if(lista[i] in logic_operators):
				operators.append(lista[i])
			else:
				terms.append(lista[i])
			i += 1
	terms.append(lista[-1])
	return terms, operators, first_negation


def process_query(query):

	# Aci tenim el termes en una llista els operadors en altra i si la query comença amb NOT
	terms, operators, negation = parser(query)
	keys_news = [] 
	print(terms)
	print(operators)
	backup_terms = list(terms)
	list1 = []
	list2 = []
	finalize = False

	# Si soles tenim un terme en la query
	if(len(terms) == 1 and len(operators) == 0): # Only a term 
		keys_news = [item[0] for item in dictionary_terms[query]]
		terms.pop(0)

	if(negation): # not valencia
		list1 = [item[0] for item in dictionary_terms[terms[0]]]
		keys_news = process_not(list1)
		list1 = list(keys_news)
		operators.pop(0)
		terms.pop(0)

	if(len(terms) > 0):
		if(not(negation)):
			list1 = [item[0] for item in dictionary_terms[terms[0]]]
			list2 = [item[0] for item in dictionary_terms[terms[1]]]
		else:
			list2 = [item[0] for item in dictionary_terms[terms[0]]]

		# mirem quin es el operador que els separa i ejecutem el algoritme adequat
		if(operators[0] == "and"):
			keys_news = intersection(list1,list2)
		elif(operators[0] == "or"):
			keys_news = union(list1, list2)	
		elif(operators[0] == "andnot" or operators[0] == "not"):
			res_not = process_not(list2)
			keys_news = intersection(list1, res_not)
		elif(operators[0] == "ornot"):
			res_not = process_not(list2)
			keys_news = union(all_new_keys, res_not)


		# elimine els termes y el operador de les llistes
		operators.pop(0)
		del terms[0:2]

		# Si tenim mes elements que procesar seguim
		while(len(terms) > 0 and len(operators) > 0):
			aux = [item[0] for item in dictionary_terms[terms[0]]]
			if(operators[0] == "and"):
				keys_news = intersection(aux, keys_news)
			elif(operators[0] == "or"):
				keys_news = union(aux, keys_news)
			elif(operators[0] == "andnot" or operators[0] == "not"):
				res_not = process_not(aux)
				keys_news = intersection(keys_news, res_not)
			elif(operators[0] == "ornot"):
				res_not = process_not(aux)
				keys_news = union(keys_news, res_not)

			terms.pop(0)
			operators.pop(0)

	show_data(keys_news, backup_terms)

def process_not(list_terms):
	# Elimine en les keys de tota la noticia
	all_new_keys = list(dictionary_news.keys())
	res = [i for j, i in enumerate(all_new_keys) if j not in list_terms]
	return res




def show_data(keys_news, terms):
	num_news = len(keys_news)

	ten_first = 0
	for i in keys_news:
		print("###################################")
		print("\n")
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
			snippet_new(text, terms)
		elif len(keys_news) > 5:
			print(title + "\n")
			ten_first += 1
			if(ten_first == 10):
				break
		print("\n")
		print("[File: " + str(path_doc) + "]")
		print("\n")
	print("------Stats-----")
	print("Total number of news retrieved: " + str(len(keys_news)) + "")
	print("\n")





# TODO: Millorar snnipet per a no repetir frases
def snippet_new(text, terms):
	list_text = text.split()
	list_indexs = []
	list_word_query_processed = []
	num_ocurrences_show = 2
	num_elements_show = 4

	for i, v in enumerate(list_text):
		if(v in terms and list_word_query_processed.count(v) <= num_ocurrences_show):
			list_indexs.append(i)
			list_word_query_processed.append(v)

	
	for i in list_indexs:
		if(i - num_elements_show <= 0): # Esta al inici
			snippet = "..." + " ".join(list_text[:i + num_elements_show]) + "..."
		elif(i + num_elements_show >= len(list_text)):
			snippet = "..." + " ".join(list_text[i - num_elements_show:]) + "..." # Esta al final
		else:
			snippet = "..." + " ".join(list_text[i - num_elements_show:i + num_elements_show]) + "..." # Esta pel mig
		print(snippet)


def union(list1, list2):
	i = 0
	j = 0
	res = []
	while (i < len(list1) and j < len(list2)):
		if(list1[i] == list2[j]):
			res.append(list1[i])
			i+=1
			j+=1
		elif(list1[i] < list2[j]):
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


def intersection(l1, l2):
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

