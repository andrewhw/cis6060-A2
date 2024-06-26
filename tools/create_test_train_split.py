#!/usr/bin/env python3

'''
Break the data up into training/testing
'''

import argparse
import os
import sys

import pandas as pd
import numpy as np

import random

from sklearn.model_selection import train_test_split, StratifiedShuffleSplit


## get values from command line if given
argparser = argparse.ArgumentParser(
		description="set up training/testing files",
		epilog="If a label column is not given, it will be assumed "
			"that the last column is the label column.")
argparser.add_argument("--tag", action="store",
		default=None, type=str,
		help="Give an additional tag used in output directory name "
			"creation.")
argparser.add_argument("-t", "--tsplit", action="store",
		default=0.25, type=float,
		help="Set the fraction of data to be set aside for training.")
argparser.add_argument("-v", "--vsplit", action="store",
		default=0.5, type=float,
		help="Set the fraction of the non-testing data to be "
			"set aside for validation. The rest is used for "
			"training.")
argparser.add_argument("-s", "--seed", action="store",
		default=None, type=int,
		help="Set the random seed -- if set to any value, every "
			"run of the program will use the same sequence of "
			"random values")
argparser.add_argument("-l", "--label", action="store",
		default=None, type=str,
		help="Indicate the label column -- if not given, the last "
			"column is assumed to be the label")
argparser.add_argument("filename",
		help="The filename to use for input, which is assumed to contain "
			"all available data.  The first line of this file is expected "
			"to hold the names of the columns, and all others lines are "
			"expected to be data values.")

args = argparser.parse_args(sys.argv[1:])



## set the seed if given for reproducible runs
if args.seed is not None:
	random.seed(argparse.seed)

if args.label is None:
	LABEL=None
else:
	LABEL=args.label

if args.tag is None:
	TAG = ""
else:
	TAG = "%s-" % args.tag

DATAFILENAME=args.filename
TESTSPLIT=args.tsplit
VALIDSPLIT=args.vsplit


print(f"Loading '{DATAFILENAME}'")
labelled_data = pd.read_csv(DATAFILENAME)
print("Data loaded")
print("Splitting: %.2f testing, %.2f of remainder validation"
		% (TESTSPLIT, VALIDSPLIT))

if LABEL is None:
	LABEL = labelled_data.columns[-1]
	print(f" . Using '{LABEL}' as label")
elif LABEL not in labelled_data.columns:
	print(f"Error: Data from '{DATAFILENAME}' has no column named '{LABEL}'",
			file=sys.stderr)
	sys.exit(1)


##
## Processing starts here
##



# Split off the label column into a separate vector
#
# At this point X is a matrix of measures (feature values),
# and y is the vector of labels describing the rows in the X matrix
X, y = labelled_data.drop(columns=[LABEL]), labelled_data[LABEL]



# break into testing and training
X_train_and_validate, X_test, y_train_and_validate, y_test = \
		train_test_split(X, y, test_size=TESTSPLIT)

## At this point we have split the data set into two independent
## subsamples.  At a 0.25 "test_size" we get:
## X_train_and_validate -- 75% of the data
## X_test -- 25% of the data independent from the train set
## y_train_and_validate -- labels for the rows in X_train_and_validate
## y_test -- labels for the rows in X_test
##
## What this does not provide for is any validation data if we
## with to do, for example, parameter tuning.  We therefore need
## to further subdivide the "X_train_and_validate" data into
## true training and validation



# Create a splitter to divide the non-test data into training and validation
#
# The splitter generates a (set of one) split
train_validate_splitter = StratifiedShuffleSplit(n_splits=1, test_size=VALIDSPLIT)

# We only need the first one from the set (of one), so we just use
# next() to pull the value from the iterator and then discard the
# iterator
validation_indices, training_indices = \
		next(train_validate_splitter.split(
				X_train_and_validate,
				y_train_and_validate))

		
# We now have the indices of data samples for our testing, validation
# and training, but only the data for the testing, so pull the data
# for training and validation.
# 
# To pull the labels, we can just use the list of indices to pull those
# values from the y vector.  For the X data we want to pull whole rows,
# so use use np.take() to pull entire rows based on their index value.
y_training = y[training_indices]
y_validation = y[validation_indices]

X_training = np.take(X, training_indices, axis=0)
X_validation = np.take(X, validation_indices, axis=0)



# save the data into the directory identified by this fold

data_dirname = "%strain-vs-test" % TAG
if not os.path.exists(data_dirname):
	os.mkdir(data_dirname)

X_training.to_csv("%s/X_train.csv" % data_dirname, index=False)
X_validation.to_csv("%s/X_validation.csv" % data_dirname, index=False)
X_test.to_csv("%s/X_test.csv" % data_dirname, index=False)

y_training.to_csv("%s/y_train.csv" % data_dirname, index=False)
y_validation.to_csv("%s/y_validation.csv" % data_dirname, index=False)
y_test.to_csv("%s/y_test.csv" % data_dirname, index=False)


