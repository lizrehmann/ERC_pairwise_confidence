#import required modules
import numpy as np
import pandas as pd
import itertools
import sys

#read in genes of interest tsv to df
input_path = "/scratch/rehmanne/ERC_pairwise_confidence/ERC_pairwise_confidence/gene_accounting.tsv"
genes_df = pd.read_csv(input_path, sep = '\t', low_memory = False)
#print(genes_df.columns)
#print(f"The rest of the df {genes_df}")

#print(genes_df["gene_name"])
# Filter rows where 'Filtered' is 'Yes' and extract the 'HOG' column
filtered_hogs = genes_df[genes_df["Filtered"] == "Yes"]["HOG"].unique().tolist()

# Print or use the list
#print(filtered_hogs)
#print(len(filtered_hogs))
#Create a set of all unique HOG pairs (unordered)
hog_pairs = set(frozenset(pair) for pair in itertools.combinations(filtered_hogs, 2))
#print(hog_pairs)

#Set path to large file
conf_path = "/scratch/rehmanne/ERCnet/OUT_prot_250424/ERC_results/ERC_results_BXB.tsv"

#Set path to output file
output_file = "pair_conf.tsv"

#Process the large conf file in chunks 
chunk_size = 50000  
chunks = pd.read_csv(conf_path, sep="\t", chunksize=chunk_size)

# Create a filtered output file with header
header_written = False
for chunk in chunks:
    # Drop rows with missing HOG values (safety)
    chunk = chunk.dropna(subset=["GeneA_HOG", "GeneB_HOG"])

    # Apply filter
    mask = chunk.apply(
        lambda row: frozenset([row["GeneA_HOG"], row["GeneB_HOG"]]) in hog_pairs,
        axis=1
    )

    filtered_chunk = chunk[mask]
    #print(filtered_chunk)

    # Write results
    filtered_chunk.to_csv(output_file, sep="\t", index=False, mode="a", header=not header_written)
    header_written = True

#reading output_file as input
pair_df = pd.read_csv("pair_conf.tsv", sep = '\t')

# Clean up any duplicated headers that may have been appended during chunk writing
pair_df = pair_df[pair_df["P_R2"] != "P_R2"].copy()

# Convert P_R2 column to numeric (float), forcing errors to NaN
pair_df["P_R2"] = pd.to_numeric(pair_df["P_R2"], errors="coerce")

# Drop rows with NaN P_R2 values
pair_df = pair_df.dropna(subset=["P_R2"])

# Build full list of labels
all_labels = sorted(set(pair_df["GeneA_ID"]).union(pair_df["GeneB_ID"]))

# Empty matrix
heatmap_df = pd.DataFrame(index=all_labels, columns=all_labels, dtype=float)

# Find match and get P_R2 value
for _, row in pair_df.iterrows():
    a, b = row["GeneA_ID"], row["GeneB_ID"]
    val = float(row["P_R2"])
    #both match optinos
    heatmap_df.loc[a, b] = val
    heatmap_df.loc[b, a] = val  

#Store the heatmap data as a tsv file
heatmap_df.to_csv("heatmap_matrix.tsv", sep = "\t")