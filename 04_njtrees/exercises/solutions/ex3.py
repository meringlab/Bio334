#!/opt/conda/bin/python

# BIO334 - Practical Bioinformatics Block Course
# session 4 - Phylogentic trees with UPGMA
# exercise 3 - calculating sequence distances from multiple alignments

# NOTE: converting identifiers containing >*OX=number* to >number

import sys

if len(sys.argv) != 2:
    print('Please specify the an input file to convert')
else:
    input_file = sys.argv[1]
    with open(input_file) as f:
        for line in f:
            # Check if line is an identifier line
            if line.startswith('>'):
                # Check if the line contains an ID
                if 'OS=' in line:
                    print('>' + line.split('OS=')[1].split(' OX=')[0])
                else:
                    # inform the user that OS= was not found
                    print('WARNING: No OS= found in identifier! ' + line,file=sys.stderr)
                    sys.exit()
            else:
                print(line, end='')
        print()
