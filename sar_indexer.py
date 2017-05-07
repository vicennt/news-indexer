#!/usr/bin/env python
#! -*- encoding: utf8 -*-

import sys


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
    	print("Usage: python sar_indexer.py <dir_news> <index_file>")
    else: 
    	dir_news = sys.argv[1]
    	index_file = sys.argv[2]

        