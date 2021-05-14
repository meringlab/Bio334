import sys
import os
import glob
import argparse
import subprocess
import numpy as np


# Argument checker
acceptable_args = ['Skin', 'Oral', 'Feces']
    
    
# Collect all args from the command line 
parser = argparse.ArgumentParser(description='Bio334 Exercise.')
parser.add_argument('--body_site', '-bs', help="specify the body site of interest, (default:'Oral')", default='Oral', choices=acceptable_args)

parser.add_argument('--sample_dir','-sd',help="the path to the samples directory (default:'../Human_Microbiome_project/')", default='files/exercise_3/Human_Microbiome_project/')

parser.add_argument('--dataset_path','-in',help="the file path to the input data (default:'.')", default='.')

parser.add_argument('--output_path','-out', help="the file path to the output data (default: './results')", default='./results')

args = parser.parse_args()
print("My arguments are:", args)
print("My --body_site argument from the user is: ", args.body_site)


# Create the output destination if it doesn't exist
if not os.path.exists(args.output_path):
    # Make the directory
    os.makedirs(args.output_path) 

    
# List all files from the specified samples directory
p = os.path.join(args.sample_dir, "*.txt")
files = glob.glob(p)

# Create the subprocess instance
filtered_file = os.path.join(args.output_path, "filtered_samples.txt")
mk_empty_file = ["touch", filtered_file]
subprocess.run(mk_empty_file)

# Iterate over each of the files in the directory and pipe any lines containing "Oral" into filtered_samples doc
for f in files:
    extract_body_site = ["cat {} | grep {} >> {}".format(f, args.body_site, filtered_file)]
    subprocess.run(extract_body_site, shell=True)
    
# Read in the filtered_samples.txt file
with open(filtered_file) as f:
    x = f.read()
    
# Read in the file, drop Nan column
x = np.genfromtxt(filtered_file)
x = x[:, 1:]

# Get abuncances average across the samples
abundance_sums = np.sum(x, axis=1)

id_path = "files/exercise_3/microbe_identifiers.txt"
with open(id_path) as f:
    ids = f.read().split(" ")
    
# Append the id with the abundance sums
id_sums = list(zip(ids, abundance_sums))

# Sort and show the top-n
n = 10
id_sums_sorted = sorted(id_sums, key=lambda x: x[1], reverse=True) 
top_n = id_sums_sorted[0:10]
print(top_n)

# Run the exercise script  with the filtered_sampels.txt
script = "files/exercise_3/compute_microbial_interactions.py"
run_analysis = ["python {} {}".format(script, filtered_file)]
print("opening lab script")
subprocess.run(run_analysis, shell=True)




# Get min-max interaction scores
pwi = np.genfromtxt('results/pairwise_interaction_strengths.txt')
min_max_pwi = []
for i, data in enumerate(pwi):
    # Get each data entry, combine each biome id with the correct data value
    entry = list(zip(ids, data))
    entry_id = ids[i]
    
    # Sort the entries on the second element (score)
    srt_entry = sorted(entry, key=lambda x: x[1], reverse=True)
    
    # Remove the self-pairwise similarity score 
    srt_entry = srt_entry[1:]
    
    # Grab max entry
    max_entry = srt_entry[0]
    min_entry = srt_entry[-1]
    
    # Store as [entry_id: (max_id, value), (min_id: value)]
    min_max_pwi.append([entry_id, max_entry, min_entry])
print(min_max_pwi[:5])