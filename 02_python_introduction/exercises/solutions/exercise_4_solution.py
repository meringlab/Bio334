import numpy as np
import pandas as pd

# 4.2 Manipulating a real data file
samp = pd.read_excel('filtered_samples.xlsx')

# 4.2.1
# Print the mean abundance for each microbe using the command below. What happens if you set axis=1?

samp.mean(axis=1)
# The row means are printed

# 4.2.2 Indexing
# Use the .loc indexer as you learned above to create a new data frame called "selection" containing only the microbes with identifiers S97-100, S97-13505, and S97-8603.

selection = samp.loc[:,['S97-100', 'S97-13505', 'S97-8603']]

# alternative:
selection = samp[['S97-100', 'S97-13505', 'S97-8603']]


# 4.2.3 Column assignment
# Currently, the body sites are used as an index. We want to create a new column called bodysites that contains this information instead, and just use a simple line count as the index instead.

selection = selection.assign(bodysite = selection.index)
selection.index = range(len(selection))

# What is the dtype of your new column?
# int64, then category


# 4.2.4 Sorting
# Sort the 'selection' data frame by the microbe S97-100, with the largest value appearing at the top of the table.

selection.sort_values('S97-100', ascending=False)

# 4.2.5 Boolean indexing
# Which part of the data frame is being selected here?
# selection.loc[(selection.loc[:,'bodysite'] == 'Skin') &
# 			  (selection.loc[:,'S97-8603'] >= 1), :]

# All rows where the bodysite column is skin and where the 'S97-8603' column is larger than or equal to 1.

#Select all samples (i.e. rows) from the 'Feces' body site where at least one of the three microbes is present and assign this selection to a new data frame called feces_samples.

feces_samples = selection.loc[selection.iloc[:,0:3].sum(axis=1) >= 1, :]

# 4.2.6 Write to file
# Now write the feces samples to a tab-separated file called feces_samples.tsv using the .to_csv('path\to\myfile.tsv', sep='\t') method. Can you find the parameter to use in order to not write the index to file?
feces_samples.to_csv('feces_samples.tsv', sep='\t', index=False)
