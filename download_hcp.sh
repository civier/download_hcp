#!/bin/bash

#################################################################
#
#  download_hcp.sh
#  ===============
#
#  Usage: download_hcp.sh <subject_list> <file_list>
#
#		subject_list - the name of the file containing subject #				    numbers (one subject number per line)
#		file_list - the name of the file containing HCP full
#				 file names (one file name per line)
#				 NOTICE: file names must include full path
#					   relative to the base of each HCP
#					   subject directory
#
#  Output: For every subject, a subdirectory with the subject 
#	      number will be created below the current directory.
#		For each subject directory, the required files will be
#		downloaded from the HCP repository on Amazon S3
#
#################################################################

export PATH="/home/oren/.local/bin:$PATH"
for subj_id in `cat $1 | tr '\n' ' '`
do
	echo ${subj_id}
	mkdir ${subj_id}
	for file in `cat $2 | tr '\n' ' '`
	do
		mkdir ${subj_id}/`dirname ${file}`		
		aws s3 cp s3://hcp-openaccess/HCP_1200/${subj_id}/${file} ./${subj_id}/${file}
	done
done
