# Culvert Evaluation
This is a previous version of the code used to analyse flood risk for stream crossings based on data collected for culverts across NY state. Please use CulvertEvaluation for the most up-to-date version.

How to use Cornell_Culvert_Evaluation.py



This Python script is found within a folder containing several other scripts that it references. To use the script, do the following: 



For each county being processed, 

1) Create a sub-folder with the county's abbreviation code as its name. For example, for Columbia county with abbreviation CBA, create a folder called 'CBA'.
 

2) Create a 'data' folder and an 'output' folder in each of these county folders. 

3) Place the following data csv files in the 'data' folder:



	a) The culvert watershed file (GIS output). 
		This should have the following columns in the following order:
   
			FID, ID, BarrierID, Area_sqkm, Tc_hr, CN
  

	b) The watershed precipitation file. This should be in the format used by Northeast 		Regional Climate Center Extreme Precipitation estimates. Importantly, the first ten 		rows should be header information, and the 11th column, starting on the 11th row, 		should contain 24-hour estimates.



	c) The field data collection file. 
		It should have the following columns in the following order:

			BarrierID, FieldID, Lat	Long, Rd_Name, Culv_Mat, In_Type, In_Shape				In_A, In_B, HW, Slope, Length, Out_Shape, Out_A, Out_B, Comments



Once all counties have the above folders created with the three input csv files in each 'data' subfolder, make a copy of the 'county_list_headers.csv' file, found within the scripts folder, and start editing it. Each row should contain the county abbreviation and the names of the three filenames that were placed in the 'data' folder for that county. For example, a valid csv file would look like: 
	

County Abbreviation, Culvert watershed file, Watershed precipitation file, Field data 	collection file
 
	CBA,Columbia_7.12.16.csv,CBA_precip.csv,CBA_field_data_usethisone.csv
		RSR,RSR_GISoutput_7.12.csv,RSR_precip.csv,RSR_fielddata_basedonRL2CulvertPts_zerosdeleted.csv



This csv basically serves to identify the names of the counties you want to process, and the names of the input data files for each county.

 Once this is all set up, run Cornell_Culvert_Evaluation.py, either through an IDE or through the console. When prompted, enter the name of the county list CSV file that you just edited. The script should now go through each county in the list, open the three input data files, run all the calculations, and store the output CSV files in the 'output' folder for that county.


