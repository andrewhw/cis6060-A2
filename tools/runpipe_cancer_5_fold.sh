#!/bin/bash

#
# Runs a simple analysis pipeline on the data in data/fulldata
#

### Safety standards
# -u : tell bash to fail if any variable is not set
# -e : tell bash to fail if any command fails (unless in an if)
# -o pipefail : tell bash to fail if part of a pipe fails (needs -e)
set -e
set -u
set -o pipefail

# save the directory that our script it in so that we can find
# the tools
SCRIPTDIR=`dirname $0`

# -x Turn tracing on to make clearer what is happening
set -x 

# create the "folds"
python3 ${SCRIPTDIR}/create_folds.py \
        --tag "cancer" -l "cancer" 5 \
        data-cancer-by-gene-expression/cancer-by-gene-expression.csv

for fold in 00 01 02 03 04
do
    echo " = Experimental Fold ${fold}"

    # calculate the projection for each fold
    python3 ${SCRIPTDIR}/calculate_data_projection.py \
            --PCA --fig "cancer-folded-${fold}"

    # run SVN on the fold
    python3 ${SCRIPTDIR}/evaluate_svn.py --fig "cancer-folded-${fold}"

    # leave two blank lines between folds
    echo "\n"
done

