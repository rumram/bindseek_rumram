def convert_to_fasta(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            parts = line.strip().split('\t')  # Split line into parts
            if len(parts) == 3:
                gene_name, identifier, sequence = parts
                outfile.write(f'>{gene_name} {identifier}\n')  # Write header
                outfile.write(f'{sequence}\n')  # Write sequence
