#!/usr/bin/env python3

import subprocess

# Function to run RNAhybrid and process its output
def run_rnahybrid(sequence, mirna_sequence, rnahybrid_param="3utr_human"):
    try:
        # Run RNAhybrid command with user-provided parameters
        result = subprocess.check_output(
            ["RNAhybrid", "-c", "-s", rnahybrid_param, sequence, mirna_sequence],
            universal_newlines=True
        )
        fields = result.split(":")
        return fields[4].strip(), fields[5].strip()
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None, None


def run_rnahybrid_analysis(input_file, mirna_sequence, rnahybrid_param):
    output_file = 'mfe_output.tsv'
    with open(input_file, 'r') as file, open(output_file, 'w') as outfile:
        next(file)  # Skip the first line if it's a header
        outfile.write("Gene\tMFE\n")  # Write column names for the output file
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:  # Ensure there are at least 3 columns (Gene, Binding, Sequence)
                name, sequence = parts[0], parts[2]  # Assuming the sequence is in the third column
                mfe_value, _ = run_rnahybrid(sequence, mirna_sequence, rnahybrid_param)
                if mfe_value is not None:
                    outfile.write(f"{name}\t{mfe_value}\n")

