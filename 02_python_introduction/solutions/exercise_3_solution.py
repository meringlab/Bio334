import sys
import os
import subprocess

## Exercise 3.1 Check the input

# python analyse_microbial_samples.py <body site> <dataset path> <output path>

# check the input belogs to element in the list

accepted_sites = ['Skin','Oral','Feces']

if len(sys.argv) < 4:
    print("Need at least 3 arguments: <body site> <dataset path> <output path>")
    sys.exit()

body_site = sys.argv[1]

if body_site not in accepted_sites:
    print("First argument has to be one of the following %s" % accepted_sites)
    sys.exit()

dataset_path = sys.argv[2]

if not os.path.exists(dataset_path):
    print("Dataset path does not exist!")
    sys.exit()

output_path = sys.argv[3]

if not os.path.exists(output_path):
    print("Will create new output path")
    os.makedirs(output_path)

# good to go, all input arguments were checked

## Exercise 3.2 Filter the samples

output_file_name = os.path.join(output_path, "filtered_samples.txt")

unix_cmd = 'cat ' + dataset_path + '/*' + ' | grep ' + body_site + '> ' + output_file_name

subprocess.call(unix_cmd,shell=True)

print("#Saved %s samples in %s" % (body_site, output_file_name))

# alternative way to directly obtain results with the check_output function
"""
alt_cmd_def = 'cat %s/* | grep %s'%(dataset_path,body_site)

result = subprocess.check_output(alt_cmd_def, shell=True)
print result.split(body_site)
"""

#### Exercise 3.3. General data set statistics

import numpy as np

# read the abundances without the body site identifier in the first column
# 1. read the data with genfromtxt
abundance_matrix = np.genfromtxt(output_file_name)
# 2. remove the first colum by array slicing
abundance_matrix = abundance_matrix[:,1:]

sample_no = abundance_matrix.shape[0]
print("#Found %d %s samples" % (sample_no,body_site))

microbe_no = abundance_matrix.shape[1]
print("#Found %d %s microbes" % (microbe_no,body_site))

# report sorted abundances for samples
sample_sums = abundance_matrix.sum(1)
sorted_sums = sorted(sample_sums, reverse=True)
print("\n#Summed sample abundance:")
print(sorted_sums)

# get microbe identfiers
# place "exercise_3_solution.py" in
# ./02_python_introduction/exercises/files/exercise_3/ location or adapt file path below
with open("microbe_identifiers.txt",'r') as id_file:
    identfiers = id_file.readline()

identfiers = identfiers.split()
microbe_means = abundance_matrix.mean(0)

# zip to join microbe names and abundances
joined_list = list(zip(identfiers, microbe_means))

print("\n#Mean abundance for all microbes:")
for identifier, mean_abundance in joined_list:
    print(identifier, mean_abundance)

#extra: report by highest incidence
print("\n#The 10 microbes with highest abundance:")

from operator import itemgetter
joined_list.sort(reverse=True, key=itemgetter(1))

for name, mean_abundance in joined_list[:10]:
    print(name, mean_abundance)

### Exercise 3.4 Microbial interactions

# execute microbial interaction script
unix_command = "python compute_microbial_interactions.py " + output_file_name
subprocess.call(unix_command, shell=True)

# retrieve interaction file
expected_file_name = "pairwise_interaction_strengths.txt"
output_file_name = os.path.join(output_path, expected_file_name)

print("\n#Strongest positive and the strongest negative interaction partner:")

# loop through all the lines in the interaction file
with open(output_file_name,'r') as f:

    # Keep track of the current row/line to avoid self-relationships
    current_idx = 0
    for line in f:

        # Initialize two pairs of variables to store the strongest:

        # negative interaction partner
        min_val = 2.0
        min_idx = -1

        # positive interaction partner
        max_val = -2.0
        max_idx = -1

        # use the built-in enumerate function to return both element and index
        for idx, element in enumerate(line.rstrip().split()):

            # transform the elmenent into a floating point value
            val = float(element)

            if idx == current_idx:
                # skip self-interactions
                continue

            if val > max_val:
                max_val = val
                max_idx = idx

            if val < min_val:
                min_val = val
                min_idx = idx

        # Output the desired result
        print(identfiers[current_idx], ":", identfiers[max_idx], "(", max_val, ");", identfiers[min_idx], "(", min_val, ")")

        # Update the current line/row index
        current_idx += 1


# Bonus: computing correlations with numpy and timing them

# correlation function from compute_microbial_interactions.py

import math


def infer_interactions(data_set):
    number_samples = len(data_set)
    number_otus = len(data_set[0])
    otu_freqs = [0] * number_otus
    for data_row in data_set:
        for i in range(len(data_row)):
            otu_freqs[i] += data_row[i]

    mean_freqs = [freq / float(number_samples) for freq in otu_freqs]

    var_covar_matrix = [[0.0] * number_otus for i in range(number_otus)]
    for i in range(number_otus):
        for j in range(number_otus):
            for k in range(number_samples):
                var_covar_matrix[i][j] += (data_set[k][i] - mean_freqs[i]) * (data_set[k][j] - mean_freqs[j])

    for i in range(number_otus):
        for j in range(number_otus):
            var_covar_matrix[i][j] = var_covar_matrix[i][j] / number_samples


    interaction_matrix = [[0.0] * number_otus for i in range(number_otus)]
    for i in range(number_otus):
        for j in range(number_otus):
            cov_ij = var_covar_matrix[i][j]
            std_i = math.sqrt(var_covar_matrix[i][i])
            std_j = math.sqrt(var_covar_matrix[j][j])

            denom = (std_i * std_j)

            if denom == 0:
                interaction_matrix[i][j] = 0.0
            else:
                interaction_matrix[i][j] = cov_ij / (std_i * std_j)

    return interaction_matrix

# time it

print("\nTiming for naive correlation function:")

## with the ipython shell:
#%timeit  np.corrcoef(abundance_matrix, rowvar=0)

## within this script its slightly more complicated:
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("timeit infer_interactions(abundance_matrix)")


print("\nTiming for numpy correlations:")
# compare to timing from numpy function
#%timeit  np.corrcoef(abundance_matrix, rowvar=0) # OR
ipython.magic("timeit np.corrcoef(abundance_matrix, rowvar=0)")
