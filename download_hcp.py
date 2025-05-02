#!/bin/python

#################################################################
#
#  download_hcp.py
#  ===============
#
#  Usage: download_hcp.py <subjects_list_file> <full_filenames_list_file>
#
#		subjects_list_file         -  the file containing subject numbers
#				                      (one subject number per line)
#		full_filenames_list_file - 	the file containing HCP full filenames
#				                    (one filename per line)
#				                    NOTICE: file names must include full path
#					                        relative to the base of each HCP
#					                        subject directory
#
#  Output: For every subject, a subdirectory with the subject 
#	   number will be created below the current directory.
#	   For each subject directory, the required files will be
#	   downloaded from the HCP repository on Amazon S3
#
#  Notes:  1. To get access to HCP on Amazon S3, please follow the instructions here:
#		https://wiki.humanconnectome.org/display/PublicData/How+To+Connect+to+Connectome+Data+via+AWS  
#	   2. aws should be installed on your system. Make sure it is installed in ~/.local/bin
#                You can follow the instructions here:
#                https://docs.aws.amazon.com/cli/latest/userguide/install-bundle.html
#          3. Use '~/.local/bin/aws configre' to set aws with the credentials provided by HCP  
#		 (choosing the default region should be sufficient for most users)
#	   4. HCP files missing from Amazon S3 will be skipped (notice that some files are available on ConnectomeDB,
#	      but are missing in Amazon S3)
#
#  Example: to download resting state data files for two selected subjects (all 4 runs), use -
#
#           	download_hcp.py subjects.txt files.txt
#	     
#	    The content of subjects.txt should be:
#	    	100307
#		100408
#
#           The content of files.txt should be:
# 		MNINonLinear/aparc+aseg.nii.gz
#		MNINonLinear/T1w_restore_brain.nii.gz
#		MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST1_RL/rfMRI_REST1_RL_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean.nii.gz
#		MNINonLinear/Results/rfMRI_REST2_RL/rfMRI_REST2_RL_hp2000_clean.nii.gz
#
#################################################################

import os
import subprocess
from pathlib import Path
import sys

def download_hcp(subjects_file, files_file):
    # Read subject IDs
    with open(subjects_file, 'r') as f:
        subject_ids = [line.strip() for line in f if line.strip()]

    # Read file paths
    with open(files_file, 'r') as f:
        file_paths = [line.strip() for line in f if line.strip()]

    # Ensure AWS CLI is in PATH
    os.environ["PATH"] = f"{os.path.expanduser('~')}/.local/bin:" + os.environ["PATH"]

    for subj_id in subject_ids:
        print(subj_id)
        subj_dir = Path(subj_id)
        subj_dir.mkdir(exist_ok=True)

        for file_path in file_paths:
            local_path = subj_dir / file_path
            local_path.parent.mkdir(parents=True, exist_ok=True)

            s3_path = f"s3://hcp-openaccess/HCP_1200/{subj_id}/{file_path}"
            print(f"aws s3 cp {s3_path} {local_path}")
            try:
                subprocess.run(["aws", "s3", "cp", s3_path, str(local_path)],
                               check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to download {s3_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_hcp.py <subject_list> <file_list>")
        sys.exit(1)

    download_hcp(sys.argv[1], sys.argv[2])
