#!/usr/bin/python3

# BIO334 - Practical Bioinformatics Block Course
# session 4 - Phylogentic trees with UPGMA
# exercise 1 - calculating sequence distances from multiple alignments

import sys
import numpy as np
import pandas as pd
import itertools

assert len(sys.argv) == 2, 'Need FASTA alignment file as argument!'

# Exercise 1

## PART 1: read in sequences from FASTA file
sequences={}
with open(sys.argv[1]) as f:
    sequence_id = None
    for line in f:
        if line.startswith(">"):
            if sequence_id!=None:
                sequences[sequence_id] = "".join(sequence)
            sequence_id = line.rstrip()[1:]
            sequence = []
        else:
            sequence.append(line.rstrip())
    if sequence_id!=None:
        sequences[sequence_id] = "".join(sequence)

seq_order = list(sequences.keys())
seq_order.sort()

## PART 2: compute distance matrix based on JACARD index
def compute_jaccard_index(a,b):
    """Function to compute jaccard index between to sequences of equal length"""
    assert len(a) == len(b), 'ERROR: Sequences are of unequal length!'
    shared = sum([1 for i in range(len(a)) if a[i] == b[i]])
    return shared / float(len(a))

j_matrix = np.zeros((len(sequences), len(sequences)))
for i, seq1 in enumerate(seq_order[:-1]):
    for j, seq2 in enumerate(seq_order[i+1:]):
        jaccard_distance = 1 - compute_jaccard_index(sequences[seq1],sequences[seq2])
        j_matrix[i][j+i+1] = jaccard_distance
        j_matrix[j+i+1][i] = jaccard_distance # identical opposite

### PART 3: Store distance matrix as CSV table using the pandas module
base_matrix = pd.DataFrame(j_matrix, columns=seq_order, index=seq_order)
print('Distance matrix for sequences in {input_file}:'.format(input_file=sys.argv[1]))
print(base_matrix)
matrix_csv = sys.argv[1]+'.dist_matrix.csv'
base_matrix.to_csv(matrix_csv)
print('Distance matrix saved to: '+matrix_csv)

# Exercise 2

def find_closest_nodes(matrix):
    nodes = list(matrix.columns)
    pd = []
    # find minimal distance in matrix
    for n1 in nodes:
        for n2 in nodes:
            if n1==n2:
                continue
            pd.append((matrix[n1][n2], n1, n2))
    pd.sort()
    return pd[0]

def compute_new_matrix(j1, j2, old_matrix):
    base_nodes = list(base_matrix.columns)
    nodes = list(old_matrix.columns)
    nodes.append("%s_%s" % (j1, j2))
    new_matrix = np.zeros((len(nodes), len(nodes)))
    for i, n1 in enumerate(nodes):
        for j, n2 in enumerate(nodes):
            if i<len(nodes)-1 and j<len(nodes)-1: # not last node added, we already know the distances
                new_matrix[i][j] = old_matrix[n1][n2]
                new_matrix[j][i] = old_matrix[n2][n1]
            else:
                nodes1, nodes2 = n1.split("_"), n2.split("_")
                pairs = list(itertools.product(nodes1, nodes2))
                dist = []
                for c1, c2 in pairs:
                    dist.append(base_matrix[c1][c2])
                dist = sum(dist)/float(len(dist))
                new_matrix[i][j] = dist
    new_matrix = pd.DataFrame(new_matrix, columns=nodes, index=nodes)
    # delete joined nodes from matrix
    del new_matrix[j1]
    del new_matrix[j2]
    new_matrix = new_matrix.drop([j1, j2])
    return new_matrix

new_matrix = base_matrix
while len(new_matrix.columns)>2:
    distance, id1, id2 = find_closest_nodes(new_matrix)
    print ("joining nodes %s and %s, distance = %.3f" % (id1, id2, distance/2.0))
    new_matrix = compute_new_matrix(id1, id2, new_matrix)
