from Bio import AlignIO
import argparse
import re

parser = argparse.ArgumentParser(description='input and output files')
parser.add_argument('-i',action='store',dest='input', help='input file ')
parser.add_argument('-o',action='store',dest='output', help='output file ')
args = parser.parse_args()

align = AlignIO.read(args.input, "stockholm")

align_dict=dict()

 
output_str=""
for record in align:
    seq=str(record.seq).upper()
    seq=seq.replace(".","-")
    output_str=output_str+">"+record.id+"\n"+seq+"\n"
    
    
with open(args.output, "w") as myfile:
    myfile.write(output_str)
    
