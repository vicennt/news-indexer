#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle


def process_query(query):
	print("Hi!")
	return query







if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
    	print("Usage: python sar_searcher.py <index_file>")
    else: 
    	index_file = sys.argv[1]
    	if not os.path.exists(index_file):
    		print("Error: The file " + index_file + " doesn't exist")
    		sys.exit(1)
    	dictionary_terms, dictionary_docs, dictionary_news = pickle.load(open(index_file,'rb'))
    	print(dictionary_docs)
    	while(True):
    		query = input("Enter your query: ")
    		if(not query):
    			break
    		results = process_query(query)
    		print(results)

