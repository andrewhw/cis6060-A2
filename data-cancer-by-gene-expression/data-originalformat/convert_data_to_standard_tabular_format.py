#!/usr/bin/env python3


import pandas as pd
import numpy as np

OUTPUT_FILENAME = "../cancer-by-gene-expression.csv"
MAPPING_FILENAME = "../label-mappings.csv"

print("Loading CSV files....")
training_data_from_csv = pd.read_csv("data_set_ALL_AML_train.csv")
independent_data_from_csv = pd.read_csv("data_set_ALL_AML_independent.csv")
labels_by_patient_id = pd.read_csv("actual.csv", index_col = 'patient')

print("CSV files loaded")


# Pull out only the first two columns -- these contain all the
# gene identity and description infomration

id_data = training_data_from_csv[
			['Gene Description','Gene Accession Number']
		]
# save this as the IDs file
id_data.to_csv("../IDs.csv", index=True, index_label="Gene ID")
print("Wrote ../IDs.csv file with gene ID information")


## Now clean up the rest of the data

# Drop "call" columns from both testing and training,
# as they are irrelevant for our purpose
delete_cols = [col for col in independent_data_from_csv.columns if 'call' in col]
independent_data_without_call = independent_data_from_csv.drop(delete_cols, 1)

delete_cols = [col for col in training_data_from_csv.columns if 'call' in col]
train_data_without_call = training_data_from_csv.drop(delete_cols, 1)


# Create a list of patient ID strings.
# We want strings so that they match the
# values read (as strings) from the CSV file
# in the next step when we concatenate the
# data files together
patients = [str(i) for i in range(1, 73, 1)]


# Concatenate "independent" and "training" data sets
# into one list.
# This still has 7128 genes, one per line, but each line
# has now been extended with the additional independent
# samples from the "independent" set.
full_gene_data_no_labels = pd.concat(
		[train_data_without_call, independent_data_without_call],
		axis = 1)[patients]

# Our learning systems can't deal with decisions based on
# lines, so we transpose the result in order to get rows
# based on samples (from people) and columns now refer to
# gene assay data.
full_gene_data_no_labels = full_gene_data_no_labels.T


# Add a "patient" column based on the patient ID number
# (we force "to_numeric()" here as the values were created
# as strings above, but now we want numbers
full_gene_data_no_labels["patient"] = pd.to_numeric(patients)


# This reassigns a 0 or 1 to the column "cancer" based on the
# previous value of the column in the labels data frame, assigning
# "ALL" to 0, and "AML" to 1.
#
# We record the mapping in the "label_mappings" data frame so that
# we can store this to a file

# calculate new values for all three "Sex" values
mapping_conditions = [
			(labels_by_patient_id['cancer'] == 'ALL'),
			(labels_by_patient_id['cancer'] == 'AML')
		]
mapping_values = [ 0, 1 ]
labels_by_patient_id['cancer'] = np.select(mapping_conditions, mapping_values)

label_mappings = pd.DataFrame( { "Label": [ "ALL", "AML" ],
			"MappedTo": [ "0", "1" ] } )


# Perform a "join" between the data and the labels to get
# labelled row data
full_data_with_labels = pd.merge(
			full_gene_data_no_labels,
			labels_by_patient_id,
			on="patient"
		).drop(columns='patient')

print("Head of full_data_with_labels:")
print(full_data_with_labels.head())

full_data_with_labels.to_csv(OUTPUT_FILENAME, index=False)
print(f"Wrote {OUTPUT_FILENAME} file with labelled data")

label_mappings.to_csv(MAPPING_FILENAME, index=False)
print(f"Wrote {MAPPING_FILENAME} file with labelled data")


