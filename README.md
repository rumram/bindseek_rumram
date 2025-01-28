# bindseek

Bindseek is a workflow that enables the identification of miRNA binding sites to the sequences of the 3'UTR of mRNA target genes. The workflow can be successfully used to search for miRNA binding sites in non-model organisms.

## Table of Contents
- [System Requirements](#system-requirements)
- [Input Files](#input-files)
  - [Gene List](#gene-list)
  - [Species List](#species-list)
  - [miRNA Seed Sequence](#mirna-seed-sequence)
  - [Source of Target Sequences](#source-of-target-sequences)
  - [Mature miRNA Sequence](#mature-mirna-sequence)
- [Installation and Running](#installation-and-running)
- [Output](#output)
  - [Result Table](#result-table)
- [Citation](#citation)


## System requirements
Bindseeker has been tested on Python 3.8 version. For the workflow to run, it is necessary to install: pandas, openxl and scipy Python packages, Perl and RNAhybrid.
All dependencies are included in Dockerfile (Docker installation required).


## Input files

Five inputs are required to run the workflow: 
* list of genes that should be scanned through (*.txt* file), 
* list of species of interest (*.txt* file), 
* 8-characters long miRNA seed sequence (e.g. *"UUCAAGUA"*), 
* source of target sequences (e.g. *"3utr_human"*), 
* 22-characters long sequence of mature miRNA (e.g. *"UUCAAGUAAUCCAGGAUAGGCU"*).

### gene list
The gene list should contain one gene name (Gene Symbol) per line:

```
AARS
ACADM
ACLY
ACSL4
ACTBL2
ACTN1
ACTN4
ACTR1A
ACTR3
AHCY
```
An example of gene list provided in *test_data* directory ("*gene_names_short.txt*").

### species list
The species list should contain one species name per line:

```
sus_scrofa
sus_scrofa_largewhite
sus_scrofa_berkshire
sus_scrofa_hampshire
```
The order of the given species names is important due to the fact that if the gene sequence for the first species is not found, the program will start looking for the gene in species lower on the list.
An example of gene list provided in *test_data* directory ("*sus_names.txt*").

### miRNA seed sequence

The seed sequence should be provided as 8-characters long combination of four letters (A, C, G, U). 

### source of target sequences
 	
Used for a quick estimate of extreme value distribution parameters. You can choose between 3utr_fly, 3utr_worm and 3utr_human for better equitation within these species.


### mature miRNA sequence

The sequence should be provided as 22-characters long combination of four letters (A, C, G, U). 



## Installation and running

The workflow is based on docker image.
First, clone GitHub repository:

```
git clone https://github.com/compcore-irzbz/bindseek.git
```

Change directory to bindseek and run docker image build:
```
cd bindseek
docker build -t bindseek_img .
```

Run workflow as docker container:

```
docker run -v "/path/to/input/dir:/results" bindseek_img --genes_file gene_names.txt --species_file species_file.txt --motif UCCCUGAG --rnahybrid_param 3utr_human --mirna_sequence UCCCUGAGACCCUAACUUGUGA
```

The output of the workflow will be stored in given path, like: */path/to/input/dir*.



## Output

The Bindseek workflow provides two output files. The main result is a results table called *complete_results.tsv*, which provides a detailed summary of the miRNA binding sites identified in the 3'UTR sequences of target genes. The second output file is the *utr.fa* file, which stores all the 3'UTR sequences of the provided target genes, in the FASTA format. 

### Result table:
| Gene | Binding | 22-nt binding sequence | Start | End | Length | Prob. | GC content | MFE |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| ACLY | 6mer | CAGTGTCTCTTTGTGTCAGGGG | 584 | 589 | 877 | 0.19178 | 54.545 | -18.5 |
| ACSL4 | 6mer-A1 | AATTTATCTTTGATAACAGGGA | 949 | 954 | 2724 | 0.48516 | 27.273 | -14.8 |
| ACSL4 | 6mer-A1 | AATATTGTTAAGGGACCAGGGA | 2037 | 2042 | 2724 | 0.48516 | 40.909 | -23.1 |
| ACTN4 | 6mer-A1 | TCTGGGGGGCGGGGGGCAGGGA | 135 | 140 | 1075 | 0.22992 | 81.818 | -28.8 |

Header description:
* 'Gene' - gene symbol,
* 'Binding' - type of binding identified,
* '22-nt binding sequence' - 22 nucleotide sequence derived from 3'UTR of tagrget gene (last characters include binding site),
* 'Start' - starting location of binding site in the 3'UTR sequence,
* 'End' - terminal location of binding site in the 3'UTR sequence,
* 'Length' - the length of 3'UTR of target gene,
* 'Prob.' - probability of finding a binding site motif in a 3'UTR sequence,
* 'GC content' - GC content of 22-nt binding sequence,
* 'MFE' - minimum free energy of 22-nt binding sequence and mature miRNA duplex.


## Citation
Using bindseek workflow, please cite:
```
 Myszczynski, Szuszkiewicz, Krawczynski, Sikora, Romaniewicz,  Guzewska, Zabielski, Kaczmarek The complexity of the miR-26a-5p- and miR-125b-5p-induced response of the uterine epithelium associated with early pregnancy events (in press)
```

As well as RNAhybrid:
```
Rehmsmeier, Marc and Steffen, Peter and Hoechsmann, Matthias and Giegerich, Robert Fast and effective prediction of microRNA/target duplexes RNA, RNA, 2004
```
