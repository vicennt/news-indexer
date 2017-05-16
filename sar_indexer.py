#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle

clean_re = re.compile('\W+')


def documents_processing(directory, index_file):
	dictionary_docs = {} 
	dictionary_terms = {}
	dictionary_news = {}
	dictionary_headline = {}
	dictionary_date = {}
	dictionary_categories = {}

	docID = 0
	newID = 0
	list_files_dir = os.listdir(directory)
	for i in list_files_dir:
		path = os.path.join(directory, i)
		dictionary_docs[docID] = path
		file = open(path)
		content = file.read()
		news = content.split('<DOC>')
		news.pop(0) # Delete the first item, it is empty
		relative_new_position = 0

		for n in news:
			dictionary_news[newID] = (docID , relative_new_position) # Add entry
			title = n[n.index('<TITLE>') + 7:n.index('</TITLE>')].lower() 
			category = n[n.index('<CATEGORY>') + 10:n.index('</CATEGORY>')].lower()
			date = n[n.index('<DATE>') + 6:n.index('</DATE>')].lower()
			new = n[n.index('<TEXT>') + 6 : n.index('</TEXT>')].lower()
			title = clean_re.sub(' ', title)
			date = clean_re.sub(' ', date)
			new = clean_re.sub(' ', new) # Clean text


			if(date in dictionary_date):
				dictionary_date[date].append(newID)
			else:
				dictionary_date[date] = [newID]

			if(category in dictionary_categories):
				dictionary_categories[category].append(newID)
			else:
				dictionary_categories[category] = [newID]


			terms_headline = title.split() # Tokenize
			relative_term_position = 0
			for t in terms_headline:
				if(t in dictionary_headline):
					if(newID == dictionary_headline[t][-1][0]): # Ultima posicio de la llista de tuple (ultima tupla)
						dictionary_headline[t][-1][1].append(relative_term_position)
					else:
						dictionary_headline[t].append((newID, [relative_term_position])) 
				else:
					dictionary_headline[t] = [(newID ,[relative_term_position])]
				relative_term_position += 1

			terms = new.split() # Tokenize
			relative_term_position = 0
			for t in terms:
				if(t in dictionary_terms):
					if(newID == dictionary_terms[t][-1][0]): # Ultima posicio de la llista de tuple (ultima tupla)
						dictionary_terms[t][-1][1].append(relative_term_position)
					else:
						dictionary_terms[t].append((newID, [relative_term_position])) 
				else:
					dictionary_terms[t] = [(newID ,[relative_term_position])]
				relative_term_position += 1
			newID += 1
			relative_new_position += 1
		docID += 1
	
	# ---- Printing stats -----
	print("----Stadistics-----")
	print("# num documents: " + str(len(dictionary_docs)))
	print("# num news: " + str(len(dictionary_news)))
	print("# num terms in text: " + str(len(dictionary_terms)))
	print("# num categories: " + str(len(dictionary_categories)))
	print("# num diferents dates: " + str(len(dictionary_date)))
	print("# num terms in headline: " + str(len(dictionary_headline)))

	file = open(index_file,'wb')
	pickle.dump((dictionary_terms, dictionary_docs, dictionary_news, 
		dictionary_headline, dictionary_date, dictionary_categories), file)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
    	print("Usage: python sar_indexer.py <dir_news> <index_file>")
    else: 
    	dir_news = sys.argv[1]
    	index_file = sys.argv[2]
    	if not os.path.exists(dir_news):
    		print("Error: The directory " + dir_news + " doesn't exist")
    		sys.exit(1)
    	documents_processing(dir_news, index_file)        