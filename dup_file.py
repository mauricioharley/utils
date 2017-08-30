#!/usr/bin/env python
"""
The dup_file.py parses the entire directory structure, calculates MD5 hash for all files and
prints the file names whose hashes are equal, i.e., duplicate ones. This code avoids calculating
symbolink links' hash, since they are only pointers to real files.
In the end, it prints two stats: the first one is the total number of duplicate occurrences and
the second one is the number of duplicate files that have been found.
---
Author:  Mauricio Harley
Date:    08/08/2017
"""

# Making sure Python 3's print function will run on Python 2
from __future__ import print_function
import os
import hashlib
from collections import defaultdict

# Creating empty collection to allow duplicate items in a dictionary
files_hashes = defaultdict(list)

# Traversing current directory, and listing directories as dirs and files as files
for root, dirs, files in os.walk("."):
	path = root.split(os.sep)
	for file in files:
		# Getting entire filename (directory + file)
		filename = os.getcwd() + os.path.join(root, file)[1:]
		# Avoiding symbolink links
		if not os.path.islink(filename):
			# Opening file and calculating its MD5 hash
			try:
				with open(filename, 'rb') as file_to_calc:
					data = file_to_calc.read()
					hashvalue = hashlib.md5(data).hexdigest()
			except:
				print("Unable to open", filename)
			else:
				files_hashes[hashvalue].append(filename)

# Printing results. It will only print elements whose hashes are the same (equal files contents).
print("Duplicate files")
print("---------------")
print()
count1 = count2 = 0
for element in files_hashes:
	if len(files_hashes[element]) > 1:
		# Increasing occurrences number
		count1 += 1
		# Increasing total number of duplicate files
		count2 += len(files_hashes[element])
		print(element)
		for i in range(len(files_hashes[element])):
			print(files_hashes[element][i])
		print()

# Printing stats
print("*** I found", count1, "occurrences with a total of", count2, "duplicate files. ***")
