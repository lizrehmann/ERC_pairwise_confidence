#import required modules
import numpy as np
import pandas as pd
import sys

#read in genes of interest tsv to df
input_path = "/scratch/rehmanne/ERC_pairwise_confidence/ERC_pairwise_confidence/Proteosome_Genes_of_Interest.tsv"
genes_df = pd.read_csv(input_path, sep = '\t', low_memory = False)
#print(genes_df)

#print(genes_df["gene_name"])

#Obtain list of ATG IDs
ATG_list = []
for ID in genes_df['AGI']:
    ATG_list.append(ID)
#print(ATG_list)

#Search file path 
hog_filepath = "/scratch/rehmanne/ERCnet/Ortho_Proteosome_Results_0420/Phylogenetic_Hierarchical_Orthogroups/N1.tsv"
hog_df = pd.read_csv(hog_filepath, sep='\t', low_memory = False)
#print(hog_df)
#print(hog_df.columns)


#filtered dataset path
filtered_filepath = "/scratch/rehmanne/ERCnet/OUT_prot_250424/Filtered_genefam_dataset.csv"
filtered_df = pd.read_csv(filtered_filepath, low_memory = False)
#print(filtered_df)
#print(filtered_df.columns)


for row in genes_df:
    #temp_index = genes_df.index
    #print(temp_index)
    #print(index)
    temp_AGI=genes_df.iloc[row]["AGI"]
    print(temp_AGI)
    sys.exit()


    
    for line in lines:
        if temp_AGI in line:
            temp_hog_id = line.split()[0].replace("N1.", "", 1)  # First column = HOG ID
            #agi_hog_list.append(agi,temp_hog_id)
    for row in rows: 
            
        #print(row)
        if temp_AGI in row:
            filtered = "Yes"
            break
        else:
            filtered = "No"
    
    genes_df.iloc[index]["HOG ID from ERCnet run"]=temp_hog_id

    genes_df.iloc[index]['Present in "filtered dataset"']=filtered


print(genes_df)
        


    





















sys.exit()

#empty list to store output

agi_hog_list = []
filtered = "NA"
temp_hog_id = ""

for agi in ATG_list:
    for line in lines:
        if agi in line:
            temp_hog_id = line.split()[0].replace("N1.", "", 1)  # First column = HOG ID
            #agi_hog_list.append(agi,temp_hog_id)
    for row in rows: 
        
        #print(row)
        if agi in row:
            filtered = "Yes"
            break
        else:
            filtered = "No"

    #for loop for dropped reason
        #if filtered = "Yes"
    agi_hog_list.append((agi, temp_hog_id, filtered))
#print(agi_hog_list)

   

agi_hog_df = pd.DataFrame(agi_hog_list, columns = ["AGI_ID", "HOG_ID", "Filtered"])
print(agi_hog_df)

#save to output file
#agi_hog_df.to_csv("/scratch/rehmanne/ERCnet/Proteosome_Data_Analyses/agi_hog_filter.tsv", sep="\t", index=False)

