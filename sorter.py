# Sorter.py
# David Gold
# November 6, 2015


# This script will sort the ws data exported from GIS by ID number

import csv, sys, operator, numpy, loader

def sort(watershed_data_input_filename, county_abbreviation, output_filename):

    # Define signature for input file.
    watershed_data_signature = [
        {'name': 'BarrierID', 'type': str},
        {'name': 'Area_sqkm', 'type': float},
        {'name': 'Tc_hr', 'type': float},
        {'name': 'CN', 'type': float}
        # Future: latitude and longitude.
    ];

    # Load data.
    watershed_data = loader.load(watershed_data_input_filename, watershed_data_signature, 1, -1)
    valid_watersheds = watershed_data['valid_rows']

    # If there were invalid watershed rows, make a note but continue on.
    num_invalid_rows = len(watershed_data['invalid_rows']) 
    if num_invalid_rows > 0:
        print "* Note: there were " \
            + str(num_invalid_rows) \
            + " invalid rows in the watershed data. Continuing with the " \
            + str(len(valid_watersheds)) \
            + " valid rows."

    # Strip *their* county abbreviation off BarrierIDs and cast to int, e.g., '10cmbws' -> 10
    id_suffix_len = 5 # Seems like their abbreviations are always 3-letter acronyms plus 'ws'.
    for watershed in valid_watersheds:
        barrier_id = watershed['BarrierID']
        watershed['BarrierID'] = int(barrier_id[:len(barrier_id) - id_suffix_len])
    
    # Sort the valid watersheds by this BarrierID number.
    def get_id(row):
        return row['BarrierID']
    valid_watersheds = sorted(valid_watersheds, key = get_id, reverse = False)

    # Write the sorted data to a new csv file.
    with open(output_filename, 'wb') as output_file:
        output_writer = csv.writer(output_file)

        # Header.
        output_writer.writerow(['BarrierID','Area_sqkm','Tc_hr','CN'])
    
        # Row for each watershed.
        # Note we are adding *our* county abbreviation back onto the BarrierID number.
        for watershed in valid_watersheds:
            output_writer.writerow([ \
                str(watershed['BarrierID']) + county_abbreviation, \
                watershed['Area_sqkm'], \
                watershed['Tc_hr'], \
                watershed['CN'] \
            ])

    # File automatically closed by 'with'.
