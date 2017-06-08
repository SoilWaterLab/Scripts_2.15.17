# Extract
# David Gold
# August, 14 2015
#
# Comments added by Tanvi Naidu (June 7th 2017)
#
# Bridges section fixed by Zoya Kaufmann 1/23/17, minor edits 6/8/2017
#
# Updated by Lisa Watkins 9/23/16
#
#
# This script will take the raw data collected in the field by either
# Fulcrum or NAACC data format and extracts useful information and assings
# Culvert ID numbers.

# Input: Field data csv downloaded from Fulcrum or the NAACC database
#
# Outputs: Culvert script input

raw_data=raw_input("Enter name of raw data file:") #prompts user to enter file name
L_rd=len(raw_data)                              
if raw_data[L_rd-4:]!='.csv': #corrects entered file name to end with '.csv' if it doesn't already 
    raw_data=raw_data+'.csv'  #end with '.csv' 
ws_name=raw_input("Enter watershed abbreviation:") #prompts user to enter three-letter watershed abbreviation
data_type=raw_input("Fulcrum data or NAACC data? (Enter F for Fulcrum, N for NAACC):") 
#prompts user to enter F or N based on type of data input

#Makes sure the user cannot input anything but capital or lower-case F or N by displaying the prompt 
#again if anything else is entered
while data_type !='f' and data_type != 'F' and data_type !='n' and data_type !='N':
    data_type=raw_input('Please enter either F for Fulcrum or N for NAACC:')

# Saves the output files as the 3-letter watershed abbreviation followed by the specified suffix
output=ws_name+"_field_data.csv"
not_extracted=ws_name+"_not_extracted.csv"

# imports required packages and modules to extract the data
import numpy, os, re, csv

f_out = open(output, 'wb') #opens output file for extracted culverts for writing in binary mode 
not_extracted_out= open(not_extracted, 'wb') #opens output for crossings not extracted for writing in binary mode
writer = csv.writer(f_out) # returns writer object from output
writer_no_extract=csv.writer(not_extracted_out) #returns writer object from non-extracted-data output

#writes the specified headings along a row for the extracted and excluded data
writer.writerow(['Survey_ID','BarrierID','NAACC_ID','Lat','Long','Rd_Name','Culv_Mat','In_Type','In_Shape','In_A','In_B','HW','Slope','Length','Out_Shape','Out_A','Out_B','Comments','Flags']) #header row
writer_no_extract.writerow(['Survey_ID','NAACC_ID','Lat','Long','Rd_Name','Culv_Mat','In_Type','In_Shape','In_A','In_B','HW','Slope','Length','Out_Shape','Out_A','Out_B','Comments','Flags']) #header row

# create an array to store field data values from the input spreadsheet
CD=[] # initialize an array to store field data values
for j in range(0,67):
    CD.append('blank')

with open(raw_data, 'r') as f:
    input_table = csv.reader(f)
    next(f) # skip header
    k=1
    if data_type=='F'or data_type=='f': #if the data is fulcrum type
        for row in input_table: #running through each row, i.e. each culvert 
            
                #naming specific columns in each row
                Fulcrum_ID=row[15] #eg: column 15 in each row represents fulcrum ID
                Lat=float(row[11])
                Long=float(row[12])
                Road_Name=row[16]
                
                # Assign culvert material and convert to language accepted by model
                Culv_material=row[18]
                if Culv_material=="Dual-Walled HDPE":
                    Culv_material="Plastic"
                elif Culv_material=="Corrugated HDPE":
                    Culv_material="Plastic"
                elif Culv_material=='Smooth Metal':
                    Culv_material='Metal'
                elif Culv_material=='Corrugated Metal':
                    Culv_material='Metal'
                
                Inlet_type=row[19]
                Inlet_Shape=row[22]               
                Inlet_A=float(row[23])
                 Inlet_B=float(row[24])
                HW=float(row[25])
                Slope=float(row[26])
                Length=float(row[27])
                Outlet_shape=row[31]
                Outlet_A=float(row[34])
                Outlet_B=float(row[35])
                Comments=row[39]
                Fulcrum_ID
                Flags=0
                
                # skipping rows if certain values are 0 or negligible
                if Inlet_A<0:  #skip in inlet width=0
                    next(f)
                elif Inlet_B<0: #skip if inlet height= 0
                    next(f)
                elif HW<0:
                    next(f)
                elif Slope<0:
                    next(f)
                elif Length <1:
                    next(f)

                BarrierID=str(k)+ws_name #coerces data into string with number and watershed name
                k=k+1     
                writer.writerow([BarrierID, Fulcrum_ID, Lat, Long, Road_Name, Culv_material, Inlet_type, Inlet_Shape, Inlet_A, Inlet_B, HW, Slope,Length, Outlet_shape, Outlet_A, Outlet_B, Comments])
                           
    elif data_type=='N'or data_type=='n':# otherwise, if data is of NAACC type (as opposed to fulcrum)
        NAACC_ID="1"   
        for row in input_table: #running through each culvert

            # eliminate blank cells from data and add data to array
            for i in range(0,67): 
                cell_value=row[i]
                if cell_value=='':
                    cell_value=-1
                CD[i]=cell_value # add field data to array

            BarrierID=str(k)+ws_name #setting barrier id as the number followed by watershed name
            
            #assigning names to the different columns (same for each row)
            Survey_ID=CD[0] 
            NAACC_ID=CD[35]
            Lat=float(CD[20])
            Long=float(CD[19])
            Road_Name=CD[26]
            Culv_material=CD[49]
            
            # Assign inlet type and then convert to language accepted by capacity_prep script
            Inlet_type=CD[22]
            if Inlet_type=="Headwall and Wingwalls":
                Inlet_type="Wingwall and Headwall"
            elif Inlet_type=="Wingwalls":
                Inlet_type='Wingwall'
            elif Inlet_type=='None':
                Inlet_type='Projecting'
                
            # Assign culvert shape and then convert to language accepted by capacity_prep script
            Inlet_Shape=CD[44]
            if Inlet_Shape=='Round Culvert':
                Inlet_Shape='Round'
            elif Inlet_Shape=='Pipe Arch/Elliptical Culvert':
                Inlet_Shape="Elliptical"
            elif Inlet_Shape=='Box Culvert':
                Inlet_Shape='Box'
            elif Inlet_Shape=='Box/Bridge with Abutments':
                Inlet_Shape='Box'
            elif Inlet_Shape=='Open Bottom Arch Bridge/Culvert':
                Inlet_Shape='Arch'
            
            Inlet_A=float(CD[47]) 
            Inlet_B=float(CD[43])
            HW=float(CD[27]) #This is from the top of the culvert, make sure the next step adds the culvert height
            Slope=float(CD[61]) 
            if Slope<0: # Negatives slopes are assumed to be zero
                Slope=0
            Length=float(CD[39])
            Outlet_shape=CD[55]
            Outlet_A=float(CD[58])
            Outlet_B=float(CD[54])
            Comments=CD[8]
            Number_of_culverts=float(CD[24])
            if Number_of_culverts > 1:
                if Number_of_culverts == 2:
                    Flags=2 # the crossing has two culverts
                elif Number_of_culverts == 3:
                    Flags=3 # The crossing has three culverts
                elif Number_of_culverts == 4:
                    Flags=4 # The crossing has four culverts
                elif Number_of_culverts == 5:
                    Flags=5 # The crossings has five culverts
                elif Number_of_culverts == 6:
                    Flags=6 # The crossing has six culverts
                elif Number_of_culverts == 7:
                    Flags=7 # The crossings has seven culverts
                elif Number_of_culverts == 8:
                    Flags=8 # The crossings has eight culverts
                elif Number_of_culverts == 9:
                    Flags=9 # The crossings has nine culverts
                elif Number_of_culverts == 10:
                    Flags=10 # The crossings has ten culverts                              
            else:
                Flags=0

            Neg_test=[Inlet_A,Inlet_B,HW,Length]
            N=0
            for i in range(0,4):
                if Neg_test[i]<0:
                    N=N+1
                
            if N==0 and (CD[44]!="Bridge with Abutments and Side Slopes" # Bridge crossings are not modeled, look up how ors are tabbed
            and CD[44]!="Bridge with Side Slopes and Abutments"
            and CD[44]!="Bridge with Side Slopes"
            and (CD[44]!="Box/Bridge with Abutments" and Inlet_A<20) # Crossings less than 20 ft are considered culverts
            and (CD[44]!="Open Bottom Arch Bridge/Culvert" and Inlet_A<20)): # Crossings less than 20 ft are considered culverts
                writer.writerow([Survey_ID, BarrierID, NAACC_ID, Lat, Long, Road_Name, Culv_material, Inlet_type, Inlet_Shape, Inlet_A, Inlet_B, HW, Slope,Length, Outlet_shape, Outlet_A, Outlet_A, Comments, Flags])
                k=k+1
            else:
                writer_no_extract.writerow([Survey_ID, NAACC_ID, Lat, Long, Road_Name, Culv_material, Inlet_type, Inlet_Shape, Inlet_A, Inlet_B, HW, Slope,Length, Outlet_shape, Outlet_A, Outlet_A, Comments, Flags])
            
f.close()
f_out.close()
not_extracted_out.close()

file_out_path=os.path.dirname(os.path.abspath(output))+'\\' + output #sets the directory and name of the output file
no_extract_out_path=os.path.dirname(os.path.abspath(not_extracted))+'\\' + not_extracted #sets the directory and name of the file containing data not extracted

#displays a message to the user indicating completion of extraction and the locations of the output files
print '\nExtraction complete! Extracted values can be found here:\n'
print file_out_path
print 'Crossings excluded from analysis can be found here:\n'
print no_extract_out_path


                    
        
