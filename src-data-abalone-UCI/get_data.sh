#!/bin/sh

DATADIR="data-originalformat"
DATAFILE="${DATADIR}/abalone.data"

if [ ! -d ${DATADIR} ] ; then
	mkdir -p ${DATADIR}
fi

if
	echo ". Running: python3 download_abalone_data.py ${DATADIR}" >&2
	python3 download_abalone_data.py ${DATADIR}
then
	if
		echo ". Running: python3 convert_abalone_data_to_standard_tabular_format.py ${DATAFILE}
		" >&2
		python3 convert_abalone_data_to_standard_tabular_format.py ${DATAFILE}
	then
		echo "Success: data downloaded and converted to tabular format" >&2
	else
		echo "Error: data downloaded, but format conversion failed" >&2
	fi
else
	echo "Error: data failed to download" >&2
	echo "" >&2
	echo "Try downloading the data manually and then running:" >&2
	echo "    convert_abalone_data_to_standard_tabular_format.py" >&2
	echo "once 'abalone.data' and 'abalone.names' have been placed" >&2
	echo "in the 'data-originalformat' directory" >&2
	echo "" >&2
fi

