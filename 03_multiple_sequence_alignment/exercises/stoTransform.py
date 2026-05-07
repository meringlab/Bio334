from Bio import AlignIO
import argparse
import io
import re

parser = argparse.ArgumentParser(description='input and output files')
parser.add_argument('-i',action='store',dest='input', help='input file ')
parser.add_argument('-o',action='store',dest='output', help='output file ')
args = parser.parse_args()

with open(args.input, "rb") as raw:
    data = raw.read()

# Try common encodings for Windows/hmmalign output
for enc in ("utf-8-sig", "utf-16", "latin-1"):
    try:
        text = data.decode(enc)
        if "# STOCKHOLM" in text[:100]:
            break
    except UnicodeDecodeError:
        continue
else:
    raise ValueError("Could not decode input file")

handle = io.StringIO(text)
align = AlignIO.read(handle, "stockholm")

align_dict=dict()

 
output_str=""
for record in align:
    seq=str(record.seq).upper()
    seq=seq.replace(".","-")
    output_str=output_str+">"+record.id+"\n"+seq+"\n"
    
    
with open(args.output, "w") as myfile:
    myfile.write(output_str)
    
