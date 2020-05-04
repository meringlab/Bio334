import os
import sys
import math

input_file = sys.argv[1]
input_folder = os.path.split(input_file)[0]

data_set = []
with open(input_file, "r") as f:
    for line in f:
        data_values = line.strip().split(" ")[1:]
        data_set.append(list(map(int, data_values)))

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


interaction_matrix = infer_interactions(data_set)

with open(os.path.join(input_folder, "pairwise_interaction_strengths.txt"), "w") as f:
    for row in interaction_matrix:
        f.write(" ".join(map(lambda x: str(round(x, 4)), row)) + "\n")




