#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle

dictionary_terms = {}
dictionary_docs = {}
dictionary_news = {}


def load_data(file):
	global dictionary_terms, dictionary_docs, dictionary_news
	dictionary_terms, dictionary_docs, dictionary_news = pickle.load(open(index_file,'rb'))


def process_query(query):
	dict_res_query = dictionary_terms[query]
	for id_new, list_pos in dict_res_query.items():
		tupla = dictionary_news[id_new]
		path = dictionary_docs[tupla[0]]
		file = open(path)
		content = file.read()
		news = content.split('<DOC>')
		news.pop(0) # Delete firs empty item
		print(news[tupla[1]])



# TODO: Snippet
def snippet_new(dict_res_query):
	if len(dict_res_query) <= 2:
		print("# 1 o 2")	
	elif len(dict_res_query) <= 5:
		print("# 3 4 5")	
	elif len(dict_res_query) > 5:
		print("# + 5")	

# TODO: Parser
def parser(query):
	terms = query.split(" ")
	num_terms = len(terms)
	
	if(num_terms % 2 == 0):
		print("# Find pair positions ")
	else:
		print("# Find odd positions")




if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
    	print("Usage: python sar_searcher.py <index_file>")
    else: 
    	index_file = sys.argv[1]
    	if not os.path.exists(index_file):
    		print("Error: The file " + index_file + " doesn't exist")
    		sys.exit(1)
    	load_data(index_file) 
    	process_query("hola") # Testing the query function
    	while(True):
    		query = input("Enter your query: ")
    		if(not query):
    			break
    		results = process_query(query)
    		print(results)

