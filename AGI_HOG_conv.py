#import required modules
import numpy as np
import pandas as pd
import sys

#read in excel file to df
excel_path = "/scratch/rehmanne/ERCnet/Proteosome_Genes_of_Interest.xlsx"
genes_df = pd.read_excel(excel_path, sheet_name=0)

#Obtain list of ATG IDs
ATG_list = []
for ID in genes_df['AGI']:
    ATG_list.append(ID)

#Search file path 
hog_filepath = "/scratch/rehmanne/ERCnet/Ortho_Proteosome_Results_0420/Phylogenetic_Hierarchical_Orthogroups/N1.tsv"

#naming lines
with open(hog_filepath, 'r') as file:
    lines = file.readlines()

#empty list to store output

agi_hog_list = []

for agi in ATG_list:
    found = False
    for line in lines:
        if agi in line:
            temp_hog_id = line.split()[0].replace("N1.", "", 1)  # First column = HOG ID
            agi_hog_list.append((agi,temp_hog_id))
            found = True
            break
    if not found:
        agi_hog_list.append((agi, "NOT FOUND"))

agi_hog_df = pd.DataFrame(agi_hog_list, columns = ["AGI_ID", "HOG_ID"])
#print(agi_hog_df)

#save to output file
agi_hog_df.to_csv("/scratch/rehmanne/ERCnet/Proteosome_Data_Analyses/agi_hog_conversion.tsv", sep="\t", index=False)

