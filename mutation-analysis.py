"""
A program that generates Mutation data from mapped files (.bam) and
Reference sequence (.fasta) with a cut-off quality of 20
"""

import os, sys
from Bio import SeqIO
from Bio import pairwise2
from statistics import mean
from tqdm import tqdm

def sam2pairwise(bam_file, ref_file, read_qual):
    md = bam_file.split('.bam')[0] + '.CalMD.bam'

    os.system('samtools calmd -b ' + bam_file + ' ' + ref_file + ' > ' + md)

    q = md.split('.bam')[0] + '.ReadQ' + str(read_qual) + '.bam'

    os.system('samtools view -bq ' + str(read_qual) + ' ' + md + ' > ' + q)
    os.system('samtools view ' + q + ' > ' + q.replace('bam', 'sam'))

    os.system('/Users/acl/Desktop/Programs/sam2pairwise/src/sam2pairwise < ' + q.replace('bam', 'sam') + ' > ' +s
              q.split('.bam')[0] + '.pairwise')

    os.system('samtools fastq ' + q + ' > ' + q.split('.bam')[0] + '.fastq')

    return [q.split('.sam')[0] + '.pairwise', q.split('.bam')[0] + '.fastq']


def parse_fastq(pairwise_file, fastq_file, ref_file):
    pairwise = {}
    lines = open(pairwise_file).readlines()
    for i, line in enumerate(lines):
        if i % 4 == 0:
            pairwise.update(
                {line.split('\t')[0]: [lines[i + 1].strip(), lines[i + 3].strip(), int(line.split('\t')[3])]})

    recs = [rec for rec in SeqIO.parse(fastq_file, 'fastq')]
    ref = [rec for rec in SeqIO.parse(ref_file, 'fasta')][0]
    reads = list({rec.id: rec for rec in recs if rec.id != ref.id}.values())

    avg_quals = {read.id: mean(read.letter_annotations["phred_quality"]) for read in reads}

    print(list(reads[0].letter_annotations.keys()))

    print('\nGetting mutations for all reads..')
    count_by_mol = {}
    muts = []
    nucs = {'A': [], 'T': [], 'G': [], 'C': []}
    irrqual_by_read = {}
    for read in tqdm(reads):
        read_idx = -1
        ref_idx = -1
        read_muts = []
        read_nucs = {'A': [], 'T': [], 'G': [], 'C': []}
        n_muts_irrqual = 0
        for c, char in enumerate(pairwise[read.id][0]):

            if char != '-':
                read_idx += 1

            if pairwise[read.id][1][c] != '-' and pairwise[read.id][1][c] != 'N':
                ref_idx += 1

                if char != '-':
                    if char != str(ref.seq)[ref_idx + pairwise[read.id][2] - 1]:
                        n_muts_irrqual += 1

                    if char in read_nucs:
                        read_nucs[char].append(read.letter_annotations["phred_quality"][read_idx])

                    try:
                        if char != str(ref.seq)[ref_idx + pairwise[read.id][2] - 1]:
                            read_muts.append((ref_idx + pairwise[read.id][2] - 1, char, read.id,
                                              read.letter_annotations["phred_quality"][read_idx]))
                    except IndexError:
                        pass

        irrqual_by_read.update({read.id: n_muts_irrqual})
        count_by_mol.update({read.id: len(read_muts)})

        for nuc in read_nucs:
            nucs[nuc].extend(read_nucs[nuc])

        if n_muts_irrqual / len(str(read.seq)) < 0.25:
            muts.extend(read_muts)

    quals = [20, 30, 40, 50, 60, 70, 80, 90]

    print('\nWriting summary file...')
    with open('MutationData_' + fastq.split('.fastq')[0] + '.csv', 'w') as o:
        o.write('Site,Ref,Alt,Qual,Num.Mols,MF,Read.ID,Read.Mean.Qual,Ref.Bases,' + ','.join(
            ['Ref.Bases.Q' + str(qual) for qual in quals]) + ',Read.Muts,' + ','.join(
            ['Read.Muts.Q' + str(qual) for qual in quals]) + 'Start&End' + '\n')

        for mut in tqdm(muts):

            count = len([m for m in muts if
                         (m[0] == mut[0] or m[0] == mut[0] - 16299 or m[0] - 16299 == mut[0]) and m[1] == mut[1]])

            ref_allele = str(ref.seq)[mut[0]]
            try:
                ref_bases = len(nucs[ref_allele])
            except KeyError:
                continue

            if mut[0] > 16298:
                pos = mut[0] - 16298
            else:
                pos = mut[0] + 1

            o.write(str(pos) + ',' + ref_allele + ',' + mut[1] + ',' + str(mut[3]) + ',' + str(count) + ',' + str(
                count / ref_bases) + ',' + mut[2] + ',' + str(avg_quals[mut[2]]) + ',' + str(ref_bases))
            for qual in quals:
                o.write(',' + str(len([nuc for nuc in nucs[ref_allele] if nuc >= qual])))
            o.write(',' + str(irrqual_by_read[mut[2]]))
            for qual in quals:
                o.write(',' + str(len([m for m in muts if m[2] == mut[2] and m[3] >= qual])))
            o.write('\n')


if __name__ == "__main__":
    # Human Hi-fi mapped file
    bam = sys.argv[1]
    # Human mitochondrial reference sequence
    ref = sys.argv[2]
    read_qual = 20

    pairwise, fastq = sam2pairwise(bam, ref, read_qual)

    pairwise = 'Human.nDNA.aln.mapped.CalMD.ReadQ20.pairwise'
    fastq = 'Human.nDNA.aln.mapped.CalMD.ReadQ20.fastq'

    parse_fastq(pairwise, fastq, ref)

