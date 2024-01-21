# bindseek

## System requirements
Bindseeker has been tested on Python 3.8 version. For the workflow to run, it is necessary to install: pandas, openxl and scipy Python packages, Perl and RNAhybrid.
All dependencies are included in Dockerfile (Docker installation required).

## Input files

Five inputs are required to run the workflow: 
* list of genes that should be scanned through, 
* list of species of interest, 
* 8-characters long miRNA seed sequence, 
* source of target sequences, 
* 22-characters long sequence of mature miRNA.

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
An example of gene list provided in *data* directory ("*gene_names_short.txt*").

### species list
The species list should contain one species name per line:

```
sus_scrofa
sus_scrofa_largewhite
sus_scrofa_berkshire
sus_scrofa_hampshire
```
The order of the given species names is important due to the fact that if the gene sequence for the first species is not found, the program will start looking for the gene in species lower on the list.
An example of gene list provided in *data* directory ("*sus_names.txt*").

### miRNA seed sequence

The seed sequence should be provided as 8-characters long combination of four letters (A, C, G, U). 

### source of target sequences
 	
Used for a quick estimate of extreme value distribution parameters. You can choose between nothing, 3utr_fly, 3utr_worm and 3utr_human for better equitation within these species.


### mature miRNA sequence

The sequence should be provided as 22-characters long combination of four letters (A, C, G, U). 

## Install

The workflow is based on docker image.
First, clone GitHub reposotiry:
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

## Usage example

```
python bindseek.py --genes_file gene_names_short.txt --species_file sus_names.txt --motif UUCAAGUA --rnahybrid_param 3utr_human --mirna_sequence UUCAAGUAAUCCAGGAUAGGCU
```

## Citation
Using bindseek workflow please cite:
```
 Myszczynski, Szuszkiewicz, Krawczynski, Sikora, Romaniewicz,  Guzewska, Zabielski, Kaczmarek The complexity of the miR-26a-5p- and miR-125b-5p-induced response of the uterine epithelium associated with early pregnancy events (in press)
```

As well as RNAhybrid:
```
Rehmsmeier, Marc and Steffen, Peter and Hoechsmann, Matthias and Giegerich, Robert Fast and effective prediction of microRNA/target duplexes RNA, RNA, 2004
```
