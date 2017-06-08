# Culvert capacity model
# Becky Marjerison
# Oct 10 2013
#
# Updated by David Gold
# July 8 2015
# Updated most recently by Lisa Watkins
# 9/15/16
#
# Comments added by Tanvi Naidu, (6/8/2017)
#
# Calculate the capacity of a culvert under inlet control
#
# Inputs: culvert_capacity_input.csv 
#
# Outputs: culvert capacity (m^3/s)

# Importing required modules and packages for analysis in python
import numpy, os, re, csv


def inlet_control(culv_cap_in, output_filename):
    f_out = open(output_filename, 'wb') #opens the output file for writing in binary form
    writer = csv.writer(f_out) #write object

    writer.writerow(['Final_ID','Q','Flags','NAACC_ID','Latitude','Longitude','Comments','Cross_sectional_area']) #header row
    # Q is culvert capacity under inlet control

    #creating empty lists for the specified parameters
    Q=[]
    culvertID=[]
    Flags=[]
    NAACC_ID=[]
    Lat=[]
    Long=[]
    Comments=[]
    C_Area = []

    with open(culv_cap_in, 'r') as f: #opening culvert capacity input file for reading
        input_table = csv.reader(f)
        next(f) # skip header
    
        for row in input_table: #each culvert

    # Capacity 
            cID = row[0] #Culvert ID, two letters indicate watershed abbreviation
            culvertID.append(cID)
            HW = float(row[4]) #Hydraulic head above the culvert invert, meters
            Culvert_Area = float(row[5]) #Calculated in input data prep script sq. meter
            C_Area.append(Culvert_Area)
            Culvert_Length = float(row[6]) # Length of culvert under road meters
            D = float(row[7]) #Diameter or dimension b, (height of culvert) meters
            # constants c, Y, Ks tabulated, depend on entrance type, from FHWA engineering pub HIF12026, appendix A
            c = float(row[8])
            Y = float(row[9]) 
            Ks = float(row[10]) # -0.5, except where inlet is mitered in which case +0.7
            S = float(row[11]) # meter/meter
            F = int(row[13])
            Flags.append(F)
            N_ID=row[1]
            NAACC_ID.append(N_ID)
            L=row[2]
            Lat.append(L)
            Lo=row[3]
            Long.append(Lo)
            cm=row[12]
            Comments.append(cm)
            
            Ku=1.811 #adjustment factor for units (SI=1.811)
                  
            # Calculate capacities and write to output file
            Qc = (Culvert_Area*numpy.sqrt(D*((HW/D)-Y-Ks*S)/(c)))/Ku #Culvert capacity submerged outlet, inlet control
            Q.append(Qc)

    L=len(Q)
    i=0
    while i < L:
        if Flags[i]>1:
            Qf=0
            for j in range(0,(Flags[i])):
                Qf=Q[i+j]+Qf
            writer.writerow([culvertID[i],Qf,Flags[i],NAACC_ID[i],Lat[i],Long[i],Comments[i],C_Area[i]])
            i=i+Flags[i]
        else:
            Qf=Q[i]
            writer.writerow([culvertID[i],Qf,Flags[i],NAACC_ID[i],Lat[i],Long[i],Comments[i],C_Area[i]])
            i=i+1
       
    
    f.close()
    f_out.close()
    return f_out
