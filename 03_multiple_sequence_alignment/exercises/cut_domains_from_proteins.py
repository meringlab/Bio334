#! /usr/bin/python3

## first, open the file containing the protein sequences:
input_file_handle = open("mfs_domain_proteins.fa")

## this dictionary will store the protein sequences from the file:
protein_sequence_dict = {}

## this will store the name of the current protein
protein_name = ""

for line in input_file_handle: # this loop is repeated for each line in the file

    l = line.strip()   ## remove any 'white space' characters at the end of the line

    if l.startswith(">"): ## if the line starts with ">", it holds a protein name

        identifier_line = l.split(" ")   ## splits the line containing the identifier into words.
        protein_name = identifier_line[0].strip(">")

    else:    ## the line does not start with ">" ... it holds a bit of the protein sequence

        if protein_name in protein_sequence_dict:                ## have we already stored some of that protein's sequence?
            protein_sequence_dict[protein_name] += l.strip() ## if yes, append the current sequence (after removing trailing newline)
        else:
            protein_sequence_dict[protein_name] = l.strip()  ## if no, begin a new entry in the dictionary


## ok, now we have read in all protein sequences, and stored them in a hash.

## next, open the file with the domain coordinates:
domain_input_file_handle = open("domains_found.tsv")

for line in domain_input_file_handle:

    if not line.startswith("#"):  ###### removes the line starting with hash

        l = line.strip().split() ############# for each line, split it into the various words according to the file format

        target_name = l[0]; c_evalue = l[11]; env_from = l[19]; env_to = l[20]

        corrected_evalue = float(c_evalue)

        if corrected_evalue <= 0.000001:  ## only report significant domain matches

            full_sequence = protein_sequence_dict[target_name] ## retrieve the corresponding protein sequence from our hash
            domain_start = int(env_from)
            domain_stop = int(env_to)
            domain_sequence = full_sequence[domain_start:domain_stop]
            print(">" + target_name + "." + env_from)
            print(domain_sequence)

## that's it, we're done.
