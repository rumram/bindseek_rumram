# bindseek

## System requirements
Bindseeker has been tested on Python 3.7 version. For the workflow to run, it is necessary to install: pandas, openxl and scipy Python packages, Perl and RNAhybrid.
## Citation
Using bindseek workflow please cite:
 Myszczynski, Kaczmarek

As well as RNAhybrid:
```
Rehmsmeier, Marc and Steffen, Peter and Hoechsmann, Matthias and Giegerich, Robert Fast and effective prediction of microRNA/target duplexes RNA, RNA, 2004
```
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
An example of gene list provided in data dircetory ("gene_names_short.txt").
