# Exercise 1.1 : Transform an interval of numbers

print('Solution for Exercise 1.1:')
# 1.1.1 square elements of a list
interval = list(range(21)) # note that the upper range is excluded 
#interval = list(range(0, 21)) # equivalent

# Iterate and square each element in the list interval
sq_interval = []
for i in interval:
    sq_interval.append(i ** 2)
print('sq_interval:', sq_interval)

# 1.1.2 remove odd numbers from the squared list
even_sq_interval = []
for i in sq_interval:
    if i % 2 == 0:
        even_sq_interval.append(i)
print('even_sq_interval:', even_sq_interval)


# Exercise 1.2 : Transform a corrupted string

print('\n' + 'Solution for Exercise 1.2:')
# 1.2.1 remove white space and convert sequences to capital letters
some_dna = 'aACTa TtCcC acCtc\tcaTCC CGGCc\nTaTaT CTGaa'
dna_pieces = some_dna.split()
print('dna_pieces:', dna_pieces)

# 1.2.2 convert the pieces into capital letters and combine them into a multi-line string
upper_dna_pieces = []
for piece in dna_pieces:
    upper_dna_pieces.append(piece.upper())

upper_dna_string = '\n'.join(upper_dna_pieces)
print('final string:\n' + upper_dna_string)
