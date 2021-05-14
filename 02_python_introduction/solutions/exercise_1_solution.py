# Exercise 1 : Transform an interval of numbers

print('Solution for Exercise 1.1:')
# 1.1.1
interval = range(21)
sq_interval = []

for i in interval:
    sq_interval.append(i ** 2)
print('sq_interval:', sq_interval)

# 1.1.2
even_sq_interval = []
for i in sq_interval:
    if i % 2 == 0:
        even_sq_interval.append(i)

print('even_sq_interval:', even_sq_interval)


# Exercise 1.2 : Transform a corrupted string

print('\n' + 'Solution for Exercise 1.2:')
# 1.2.1
some_dna = 'aACTa TtCcC acCtc\tcaTCC CGGCc\nTaTaT CTGaa'
dna_pieces = some_dna.split()
print('dna_pieces:', dna_pieces)

# 1.2.2
upper_dna_pieces = []
for piece in dna_pieces:
    upper_dna_pieces.append(piece.upper())

upper_dna_string = '\n'.join(upper_dna_pieces)
print('final string:\n' + upper_dna_string)
