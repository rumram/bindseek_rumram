#!/usr/bin/env python3

import os
import argparse
import subprocess
import pandas as pd
from binding_search import run_binding_site_analysis
from mfe_calculate import run_rnahybrid_analysis
from binding_search import reverse_complement
from fasta_convert import convert_to_fasta


def run_module1(genes_file, species_file, output_file):
    # Run the Perl script (Module 1) using subprocess
    subprocess.run(["perl", "/src/get_3utr.pl", "--species_file", species_file, "--genes_file", genes_file, "--output_file", output_file], check=True)


def main():
    parser = argparse.ArgumentParser(description='Run the complete 3\'UTR analysis workflow.')
    parser.add_argument('--genes_file', type=str, required=True, help='File containing gene names')
    parser.add_argument('--species_file', type=str, required=True, help='File containing species names')
    parser.add_argument('--motif', type=str, required=True, help='Motif for binding site analysis')
    parser.add_argument('--rnahybrid_param', type=str, required=True, help='RNAhybrid parameter')
    parser.add_argument('--mirna_sequence', type=str, required=True, help='miRNA sequence for RNAhybrid')
    args = parser.parse_args()

    # File paths
    output_file_module1 = "output_data.txt"
    output_file_module2 = "binding_sites.tsv"
    output_file_module3 = "mfe_output.tsv"
    merged_output_file = "complete_results.tsv"

    # Run Module 1 (Perl script)
    run_module1(genes_file=args.genes_file, species_file=args.species_file, output_file=output_file_module1)

    print(f"Identifying binding sites within 3'UTR sequences.")
    # Run Module 2 (Python for binding site analysis)
    run_binding_site_analysis(input_file=output_file_module1, motif=reverse_complement(args.motif), output_file=output_file_module2)

    print(f"Calculating MFE.")
    # Run Module 3 (Python for RNAhybrid analysis)
    run_rnahybrid_analysis(input_file=output_file_module2, rnahybrid_param=args.rnahybrid_param, mirna_sequence=args.mirna_sequence)

    # Read the outputs of Module 2 and Module 3
    module2_data = pd.read_csv(output_file_module2, sep='\t')
    module3_data = pd.read_csv(output_file_module3, sep='\t')  # The file name is hardcoded in Module 3

    # Merge the dataframes side by side
    merged_data = pd.concat([module2_data, module3_data['MFE']], axis=1)

    # Save the merged test_data to a TSV file
    merged_data.to_csv(merged_output_file, sep='\t', index=False)

    # Create fasta file and do some clean up
    convert_to_fasta(output_file_module1, "genes.fa")
    os.remove("binding_sites.tsv")
    os.remove("mfe_output.tsv")
    os.remove("output_data.txt")
    print(f"Workflow completed. Results stored in: {merged_output_file}")


if __name__ == "__main__":
    main()
