#import required modules
import numpy as np
import pandas as pd
import sys

#read in genes of interest tsv to df
input_path = "/scratch/rehmanne/ERC_pairwise_confidence/ERC_pairwise_confidence/Proteosome_Genes_of_Interest_2.tsv"
genes_df = pd.read_csv(input_path, sep = '\t', low_memory = False)
#print(genes_df)

#print(genes_df["gene_name"])


#Hog dataset path
hog_filepath = "/scratch/rehmanne/ERCnet/Ortho_Proteosome_Results_0420/Phylogenetic_Hierarchical_Orthogroups/N1.tsv"
hog_df = pd.read_csv(hog_filepath, sep='\t', low_memory = False)
#print(list(hog_df['ARAT']))
#print(hog_df.columns)


#filtered dataset path
filtered_filepath = "/scratch/rehmanne/ERCnet/OUT_prot_250424/Filtered_genefam_dataset.csv"
filtered_df = pd.read_csv(filtered_filepath, low_memory = False)
#print(filtered_df)
#print(filtered_df.columns)

#network dataset path
network_filepath = "/scratch/rehmanne/ERCnet/OUT_prot_250424/Network_analyses/Text_network_vertices_Filtered_ERC_results_BXB_pearson_0.0001_0.4_fg_trimcutoff_0.tsv"
network_df = pd.read_csv(network_filepath, sep = '\t', low_memory = False)
#print(network_df)

#drop dataset path
dropped_filepath = "/scratch/rehmanne/ERCnet/OUT_prot_250424/Dropped_gene_log.csv"
dropped_df = pd.read_csv(dropped_filepath, low_memory = False)
#print(dropped_df)

genes_df['HOG'] = "NA"
#print(genes_df.columns)

for row in genes_df.index:
    #print(row)
    temp_AGI = genes_df.at[row, "AGI"]
    #print(temp_AGI)
    
    #HOG Search
    HOG_row = hog_df[hog_df['ARAT'].str.contains(temp_AGI, na=False)]
    
    if not HOG_row.empty:
        temp_hog = HOG_row.iloc[0]["HOG"].replace("N1.", "")
        genes_df.at[row, "HOG"] = temp_hog

        #print(temp_hog)
    else:
        #print("No HOG found for:", temp_AGI)
        genes_df.at[row, "HOG"] = "NA"


    #Filtered Search 
    filtered_row = filtered_df[filtered_df['ARAT'].str.contains(temp_AGI, na=False)]
    if not filtered_row.empty:
        genes_df.at[row, "Filtered"] = "Yes"

    else:
        genes_df.at[row, "Filtered"] = "No"


    #Network Search
    network_row = network_df[network_df['Comprehensive_ID'].str.contains(temp_AGI, na=False)]
    if not network_row.empty:
        genes_df.at[row, "Network"] = "Yes"
        genes_df.at[row, "Localization"] = network_row["Functional_category"].iloc[0]

    else: 
        genes_df.at[row, "Network"] = "No"
        genes_df.at[row, "Localization"] = "NA"


    
    #Dropped search
    dropped_row = dropped_df[dropped_df['HOG'].str.contains(temp_hog, na = False)]
    if not dropped_row.empty:
        genes_df.at[row, "Reason_for_Drop"] = dropped_row["Reason"].iloc[0]

    else: 
        genes_df.at[row, "Reason_for_Drop"] = "NA"

    

#print(genes_df)

genes_df.to_csv('gene_accounting.tsv', sep = '\t')
        


    





















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

