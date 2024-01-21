#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long;
use Bio::EnsEMBL::Registry;
use Bio::SeqIO;
use IO::String;

print "Starting the workflow...\n";

# Command-line options
my $genes_file;
my $species_file;
my $output_file = "utr_sequence.txt";  # Default output file name

GetOptions(
    'species_file=s' => \$species_file, # File containing species names
    'genes_file=s'   => \$genes_file,   # File containing gene names
    'output_file=s'  => \$output_file   # Output file name
);

unless ($genes_file && $species_file) {
    die "Usage: perl $0 --species_file species.txt --genes_file genes.txt --output_file output.txt\n";
}

# Function to read and filter non-empty lines from a file
sub read_and_filter_file {
    my ($filename) = @_;
    my @lines;
    open my $fh, '<', $filename or die "Cannot open file $filename: $!";
    while (my $line = <$fh>) {
        chomp $line;
        push @lines, $line if $line ne '';
    }
    close $fh;
    return @lines;
}

# Read and filter species from the file
my @species = read_and_filter_file($species_file);

# Read and filter genes from the file
my @genes = read_and_filter_file($genes_file);

# Connect to Ensembl
my $registry = 'Bio::EnsEMBL::Registry';
$registry->load_registry_from_db(
    -host => 'ensembldb.ensembl.org',
    -user => 'anonymous'
);

# Open output file
open(my $FH, '>', $output_file) or die "Cannot open file $output_file: $!";

foreach my $gene_name (@genes) {
    print("Processing gene $gene_name.\n");
    my $gene_found = 0;

    foreach my $species_name (@species) {
        my $gene_adaptor = $registry->get_adaptor($species_name, 'Core', 'Gene');
        my $gene = $gene_adaptor->fetch_by_display_label($gene_name);

        if ($gene) {
            $gene_found = 1;
            my $transcript = $gene->canonical_transcript;
            next unless defined $transcript;

            my $tputr = $transcript->three_prime_utr();
            next unless defined $tputr;

            my $p1 = $gene->external_name();
            my $p2 = $transcript->stable_id;
            print $FH "$p1\t$p2\t";

            my $str;
            my $io = IO::String->new(\$str);
            my $outseq = Bio::SeqIO->new(-fh => $io, -format => 'raw');
            $outseq->write_seq($tputr);
            print $FH $str;
            print "$p1 | $p2 extracted from $species_name.\n";

            last; # Exit the loop after finding the gene
        }
    }

    # Print message if gene is not found in any species
    unless ($gene_found) {
        print "Gene $gene_name not found in any of the specified species.\n";
    }
}

close $FH;

