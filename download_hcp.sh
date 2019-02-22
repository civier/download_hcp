#!/bin/bash

#################################################################
#
#  download_hcp.sh
#  ===============
#
#  Usage: download_hcp.sh <subject_list> <file_list>
#
#		subject_list -  the file containing subject numbers
#				(one subject number per line)
#		file_list - 	the file containing HCP full filenames
#				(one filename per line)
#				NOTICE: file names must include full path
#					relative to the base of each HCP
#					subject directory
#
#  Output: For every subject, a subdirectory with the subject 
#	   number will be created below the current directory.
#	   For each subject directory, the required files will be
#	   downloaded from the HCP repository on Amazon S3
#
#  Notes:  1. Make sure aws is installed in ~/.local/bin
#	   2. Files missing from Amazon S3 will be skipped
#
#  Example: to download resting state data files for two selected subjects, use -
#           	download_hcp.sh subjects.txt files.txt
#	     
#	    The content of subjects.txt is:
#	    	100307
#		100408
#
#           The content of files.txt is:
# 		MNINonLinear/aparc+aseg.nii.gz
#		MNINonLinear/T1w_restore_brain.nii.gz
#		MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST1_RL/rfMRI_REST1_RL_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST2_RL/rfMRI_REST2_RL_hp2000_clean.nii.gz
#
#################################################################

export PATH="~/.local/bin:$PATH"
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
