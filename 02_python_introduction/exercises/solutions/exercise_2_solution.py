# Exercise 2 : Nucleotide counting

print('Solution for Exercise 2:\n')
## 2.1 Create the function
def count_nucleotides(file_name):
    print(file_name)
    
## 2.2 Read the .txt file
def count_nucleotides(file_name):   
    dna_file = open(file_name, 'r')
    DNA = ''
    for line in dna_file:
        dna_line = line.strip()
        DNA += dna_line
    dna_file.close()
    print(DNA)
    return DNA

## 2.3 Scan the sequence and count nucleotides

## using 4 variables
file_name = r"../files/exercise_2/strange_dna.txt"
DNA = count_nucleotides(file_name)
A = 0
C = 0
G = 0
T = 0
for nucleotide in DNA:
    if nucleotide == 'A':
        A += 1
    elif nucleotide == 'C':
        C += 1
    elif nucleotide == 'G':
        G += 1
    elif nucleotide == 'T':
        T += 1

## using a dict
nucleotide_counts = {'A': 0, 'C':0, 'G':0, 'T':0}
for nucleotide in DNA:
    nucleotide_counts[nucleotide] += 1

## 2.4 Report the results
## using 4 variables (commented out to prevent cluttering of screen)
print("\nusing 4 variables")
print('Number of A:', A)
print('Number of C:', C)
print('Number of G:', G)
print('Number of T:', T)

## using a dict
print("\nusing a dict")
for key_value_pair in nucleotide_counts.items():
    nucleotide = key_value_pair[0]
    count = key_value_pair[1]
    print('Number of', nucleotide, ':', count)



