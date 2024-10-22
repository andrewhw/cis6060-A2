#!/usr/bin/env python3

##
## Obtains and unzips the Abalone data set from the UCI machine
## learning repository:
## 
## J Nash, W.; Sellers, T. L.; Talbot, S. R.; Cawthorn, A. J. &amp; Ford, W. B.
## "Abalone Data Set"
## in
## Dua, D. &amp; Graff, C.
## "UCI Machine Learning Repository"
## University of California, Irvine, School of Information and Computer Sciences,
## 2017.
##
## [https://archive.ics.uci.edu/ml/datasets/Abalone](https://archive.ics.uci.edu/ml/datasets/Abalone)
## Accessed: April 28, 2024.
##
## UCI citation and usage policy: https://archive.ics.uci.edu/ml/citation_policy.html

import sys
import os
import wget
import zipfile

if len(sys.argv) < 2:
	print("Error: data directory argument required on command line",
			file=sys.stderr)
	sys.exit(1)

datadir = sys.argv[1]

URL = "https://archive.ics.uci.edu/static/public/1/abalone.zip"

print(f". Downloading Abalone data set from '{URL}'")
try:
	zipfilename = wget.download(URL)
except Error as err:
	print(f"Error: failed downloading data set from repository -- {err}",
			file=sys.stderr)
	sys.exit(1)

print("")
print("")
print(f". Successfully downloaded '{zipfilename}'")
print(f". Unpacking Abalone data set into {datadir}")


try:
	with zipfile.ZipFile(zipfilename, "r") as zipper:
		zipper.extractall(datadir)
except Error as err:
	print(f"Error: failed unpacking zip file '{zipfilename}' -- {err}",
			file=sys.stderr)
	sys.exit(1)

print(f". Successfully unpacked Abalone data into '{datadir}':")
for item in os.listdir(datadir):
	print(f".   {item}")

print(f". Done")

sys.exit(0)
