
import os

os.chdir('/Users/ymaithania/Academics/Data/database_data')

def create_seq_file(fasta_file, formatted_fasta):
    
    '''takes a fasta file of sequences and tags, and creates a new formatted file where the sequences have no whitespace'''

    with open(fasta_file, 'r') as fasta:
        f_seq = fasta.readlines()



    all_seqs = []
    seq = ''
    for entry in f_seq:
        if entry.startswith('>sp'):
            if seq:
                all_seqs.append(seq)
                seq = ''
            name = entry.strip()
            all_seqs.append(name)
        else:
            string = entry.strip()
            seq += string
    all_seqs.append(seq)   
        
    for line in all_seqs:
        with open(formatted_fasta, 'a') as file:
            l = line + '\n'
            file.write(l)


def create_protein_data(protein_out, protein_pos_out, variant_out, variant_file, formatted_fasta):
    
    '''When given the names of the 3 files to be outputted, a file of variant data and formatted fasta sequences,
    creates three protein-related output files that contain data to be uploaded to database'''
    
    import re
    import csv
    
    with open(formatted_fasta) as ff_sequences:
        sequences = ff_sequences.readlines()

    with open(variant_file, 'r') as variants:
        var = variants.readlines()
        var = var[1:]
        
    with open(protein_out, 'a') as f:
        prot_writer = csv.writer(f, delimiter  =';', quoting = csv.QUOTE_ALL, lineterminator = '\n')
        prot_writer.writerow(["uniprot_id","gene_name"])
        
    with open(protein_pos_out, 'a') as pp_file:
        pp_writer = csv.writer(pp_file, delimiter = ';', quoting = csv.QUOTE_ALL)
        pp_writer.writerow(["protein_pos_id","uniprot_id","residue","uniprot_pos"])
        
    with open(variant_out, 'a') as var_file:
        vari_writer = csv.writer(var_file, delimiter = ';', quoting = csv.QUOTE_ALL, lineterminator = '\n')
        vari_writer.writerow(["variant_id","protein_pos_id","structure","structure_type","residue_wt","residue_mut",
                             "m3d_prediction","sift_prediction","sift_score","polyphen_prediction","polyphen_score",
                             "clinvar","humsavar"])


    for i in range(0, len(sequences), 2):
        desc = sequences[i]
        aa_seq = sequences[i+1]

        uniprot_id = (re.search(r'\|(.*?)\|', desc)).group()
        uniprot_id = uniprot_id.replace('|', '') 

        gn = (re.search(r'GN=(.*)\s', desc)).group()

        gn = gn.split(' ')
        gene_name = gn[0][3:]

        with open(protein_out, 'a') as f:
            prot_writer = csv.writer(f, delimiter=';', quoting = csv.QUOTE_ALL, lineterminator = '\n')
            prot_writer.writerow([uniprot_id, gene_name])


        for ind in range(len(aa_seq)):
            pos = ind+1 
            res = aa_seq[ind]
            prot_pos_id = uniprot_id + '_' + str(pos)

            if res != '\n':

                entry = [prot_pos_id, uniprot_id, res, pos]

                with open(protein_pos_out, 'a') as pp_file:
                    pp_writer = csv.writer(pp_file, delimiter = ';', quoting = csv.QUOTE_NONNUMERIC)
                    pp_writer.writerow(entry)


            for line in var:
                lst = line.split(',')
                if lst[1] == uniprot_id and int(lst[4]) == pos:

                    variant_id = int(lst[0])
                    structure = lst[2]
                    struc_type = lst[3]
                    wt_res = lst[5]
                    mut_res = lst[6]
                    m3d_pred = lst[7]
                    humsavar = lst[8]
                    clinvar = lst[9]

                    if lst[10] != '-':
                        sift = lst[10].split('(')
                        sift_pred = sift[0]
                        sift_score = float(sift[1].replace(')',''))
                    else:
                        sift_pred = '-'
                        sift_score = 9.99

                    if lst[11] != '-\n':
                        polyp = lst[11].split('(')
                        polyp_pred = polyp[0]
                        polyp_score = float(polyp[1].replace(')','').replace('\n',''))
                    else:
                        polyp_pred = '-'
                        polyp_score = 9.99


                    final_lst = [variant_id, prot_pos_id, structure, struc_type, wt_res, mut_res,
                    m3d_pred,sift_pred,sift_score,polyp_pred,polyp_score,clinvar,humsavar]

                    with open(variant_out, 'a') as var_file:
                        vari_writer = csv.writer(var_file, delimiter = ';', quoting = csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                        vari_writer.writerow(final_lst)
                else:
                    continue
                        
                        


#fasta_file = 'all_gpcrs.txt'
variant_file = 'db_variants.csv'
formatted_fasta = 'fasta_formatted.txt'
protein_out = 'protein_table2.csv'
protein_pos_out = 'protein_pos_table2.csv'
variant_out = 'variant_table2.csv'


#create_seq_file(fasta_file, formatted_fasta)
create_protein_data(protein_out, protein_pos_out,variant_out,variant_file,formatted_fasta)
