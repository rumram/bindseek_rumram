import argparse
import subprocess
import pandas as pd
from src.binding_search import run_binding_site_analysis
from mfe_calculate import run_rnahybrid_analysis
from src.binding_search import reverse_complement


def run_module1(genes_file, species_file, output_file):
    # Run the Perl script (Module 1) using subprocess
    subprocess.run(["perl", "get_3utr.pl", "--species_file", species_file, "--genes_file", genes_file, "--output_file", output_file], check=True)


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
    merged_output_file = "merged_output.tsv"

    # Run Module 1 (Perl script)
    run_module1(args.genes_file, args.species_file, output_file_module1)

    # Run Module 2 (Python for binding site analysis)
    run_binding_site_analysis(output_file_module1, reverse_complement(args.motif), output_file_module2)

    # Run Module 3 (Python for RNAhybrid analysis)
    run_rnahybrid_analysis(output_file_module2, args.rnahybrid_param, args.mirna_sequence)

    # Read the outputs of Module 2 and Module 3
    module2_data = pd.read_csv(output_file_module2, sep='\t')
    module3_data = pd.read_csv('final_output.tsv', sep='\t')  # The file name is hardcoded in Module 3

    # Merge the dataframes side by side
    merged_data = pd.concat([module2_data, module3_data['MFE']], axis=1)

    # Save the merged data to a TSV file
    merged_data.to_csv(merged_output_file, sep='\t', index=False)
    print(f"Workflow completed. Merged results are in: {merged_output_file}")


if __name__ == "__main__":
    main()