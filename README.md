# download_hcp
Tools to download data from the Human Connectome Project repositories

Current tools:

download_hcp.sh - download selected files for selected subjects from the HCP repository on Amazon S3

download_hcp.sh
===============

Usage: download_hcp.sh <subject_list> <file_list>

		subject_list -  the file containing subject numbers
				(one subject number per line)
		file_list - 	the file containing HCP full filenames
				(one filename per line)
				NOTICE: file names must include full path
					relative to the base of each HCP
					subject directory

  Output: For every subject, a subdirectory with the subject 
	   number will be created below the current directory.
	   For each subject directory, the required files will be
	   downloaded from the HCP repository on Amazon S3

  Notes:  
     1. To get access to HCP on Amazon S3, please follow the instructions here:
		https://wiki.humanconnectome.org/display/PublicData/How+To+Connect+to+Connectome+Data+via+AWS  
		
     2. aws should be installed on your system. Make sure it is installed in ~/.local/bin
                You can follow the instructions here:
                https://docs.aws.amazon.com/cli/latest/userguide/install-bundle.html
		
     3. Use '~/.local/bin/aws configre' to set aws with the credentials provided by HCP  
		 (choosing the default region should be sufficient for most users)
		 
     4. HCP files missing from Amazon S3 will be skipped (notice that some files are available on ConnectomeDB,
	      but are missing in Amazon S3)

   Example: to download resting state data files for two selected subjects (all 4 runs), use -
           	download_hcp.sh subjects.txt files.txt
	     
	  The content of subjects.txt should be:
	  100307
		100408

    The content of files.txt should be:
 		MNINonLinear/aparc+aseg.nii.gz
		MNINonLinear/T1w_restore_brain.nii.gz
		MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean.nii.gz
		MNINonLinear/Results/rfMRI_REST1_RL/rfMRI_REST1_RL_hp2000_clean.nii.gz
		MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean.nii.gz
		MNINonLinear/Results/rfMRI_REST2_RL/rfMRI_REST2_RL_hp2000_clean.nii.gz

