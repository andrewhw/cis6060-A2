#!/usr/bin/env python3

'''
Convert the UCI data to a csv file in the parent directory.

Here it was easier simply to encode all the names for the columns
in this file rather than do complicated parsing from the "abalone.names"
file.
'''

import sys
import pandas as pd
import numpy as np

INPUT_FILENAME = sys.argv[1]
OUTPUT_FILENAME = "abalone.csv"
MAPPING_FILENAME = "label-mappings.csv"

DESIRED_COLUMN_NAMES = [
		"Sex",
		"Length",
		"Diameter",
		"Height",
		"Whole weight",
		"Shucked weight",
		"Viscera weight",
		"Shell weight",
		"Rings" ]

print("Loading CSV files....")
try:
	data_set = pd.read_csv(INPUT_FILENAME)
except IOError as err:
	print(f"Error: cannot read {INPUT_FILENAME}: {err}", file=sys.stderr)
	sys.exit(1)

print("CSV files loaded")


# Add column headers for original data
data_set.columns = DESIRED_COLUMN_NAMES


# Now we want to convert "Sex" to be an integer label.
#
# We set up the list of mappings that we want as a list
# of conditions (effectively "if" statement tests) and
# the values that we want to apply based on these conditions.
#
# We also make another dataframe with this information in
# it to store as the label-mappings.csv file

# calculate new values for all three "Sex" values
mapping_conditions = [
			(data_set['Sex'] == 'I'),
			(data_set['Sex'] == 'M'),
			(data_set['Sex'] == 'F')
		]
mapping_values = [ 0, 1, 2 ]
data_set['Sex'] = np.select(mapping_conditions, mapping_values)

label_mappings = pd.DataFrame( { "Label": [ "I", "M", "F" ],
			"MappedTo": [ "0", "1", "2" ] } )

print("Head of data set")
print(data_set.head())

data_set.to_csv(OUTPUT_FILENAME, index=False)
print(f"Wrote {OUTPUT_FILENAME} file with labelled data")

label_mappings.to_csv(MAPPING_FILENAME, index=False)
print(f"Wrote {MAPPING_FILENAME} file with labelled data")


