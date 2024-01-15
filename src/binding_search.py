import argparse
import re
import pandas as pd
import math
from scipy import stats


def reverse_complement(dna_sequence):
    complement_dict = {'A': 'T', 'U': 'A', 'C': 'G', 'G': 'C'}
    reverse_comp_seq = ''.join(complement_dict[base] for base in reversed(dna_sequence))
    return reverse_comp_seq


def run_binding_site_analysis(input_file, motif, output_file):
    sq_file = pd.read_table(input_file, sep='\t', header=None)
    flat = []

    for j in range(len(sq_file[2])):
        aa = searchin(motif, sq_file[2][j], sq_file[0][j])
        if aa:
            for z in aa:
                flat.extend(z)

    list_of_lists = [flat[i:i + 8] for i in range(0, len(flat), 8)]
    df = pd.DataFrame(list_of_lists, columns=['Gene', 'Binding', '22-nt binding sequence', 'Start', 'End', 'Length', 'Prob.', 'GC content'])
    df.to_csv(output_file, sep="\t", index=False)


def gc_content(seq):
    gc_count = seq.count('G') + seq.count('C')
    return gc_count / len(seq) if len(seq) > 0 else 0


def prob(seq_len, mot_len):
    n_sub = len(seq_len) - mot_len + 1
    prob_match = math.pow(4, - mot_len)
    return stats.binomtest(1, n_sub, p=prob_match)


def find_start_positions(motif, sequence):
    substring = motif[2:6]
    return [m.start() - 1 for m in re.finditer(substring, sequence)]


def check_motif_conditions(motif, sequence, i, name):
    seq_segment = sequence[i-15:i+7]
    gc_cont = gc_content(seq_segment)
    motif_type = None
    start_pos = i
    end_pos = None

    if sequence[i-1:i+1] == motif[0:2] and len(sequence[i:]) >= 7:
        if re.search(motif[6] + 'A', sequence[i+5:i+7]):
            motif_type = '8mer'
            end_pos = i + 7
        elif re.search(motif[6] + r"[ACGT]", sequence[i+5:i+7]):
            motif_type = '7mer-m8'
            end_pos = i + 6
        else:
            motif_type = '6mer-m8'
            end_pos = i + 5
    elif re.search(r"[ACGT]", sequence[i-1]) and len(sequence[i:]) >= 7:
        start_pos = i + 1  # Increment start position by 1 for these cases
        if re.search(motif[6] + 'A', sequence[i+5:i+7]) and re.search(motif[1], sequence[i]):
            motif_type = '7mer-A1'
            end_pos = i + 7
        elif re.search(motif[6], sequence[i+5]) and re.search(motif[1], sequence[i]):
            motif_type = '6mer'
            end_pos = i + 6
        elif re.search(motif[6] + 'A', sequence[i+5:i+7]):
            motif_type = '6mer-A1'
            end_pos = i + 6

    if motif_type:
        motif_length = end_pos - start_pos + 1  # Adjusted to include the character at end_pos
        return [name, motif_type, seq_segment, start_pos, end_pos, len(sequence), round(prob(sequence, motif_length).pvalue, 5),
                round(gc_cont*100, 3)]
    else:
        return None


def searchin(motif, sequence, name):
    found = []
    start_positions = find_start_positions(motif, sequence)
    for i in start_positions:
        result = check_motif_conditions(motif, sequence, i, name)
        if result:
            found.append(result)
    return found

