import csv

def generate_variant_data(protein_pos_file, variant_file, variant_out_name):

    with open(variant_file, 'r') as variants:
        var = variants.readlines()
        var = var[1:]

    with open(protein_pos_file, 'r') as pp_file:
        pp = pp_file.readlines()
        pp = pp[1:]

    for line in pp:
        prot_lst = line.split(';')
        uniprot_id = prot_lst[1]
        uniprot_pos = int(prot_lst[3])

        for variant in var:
            var_lst = variant.split(',')

            if var_lst[1] == uniprot_id and int(var_lst[4]) == uniprot_pos:
                
                variant_id = int(var_lst[0]) 
                structure = var_lst[2]
                struc_type = var_lst[3]
                wt_res = var_lst[5]
                mut_res = var_lst[6]
                m3d_pred = var_lst[7]
                humsavar = var_lst[8]
                clinvar = var_lst[9]

                if var_lst[10] != '-':
                    sift = var_lst[10].split('(')
                    sift_pred = sift[0]
                    sift_score = float(sift[1].replace(')', ''))
                else:
                    sift_pred = '-'
                    sift_score = 9.99

                if var_lst[11] != '-\n':
                    polyp = var_lst[11].split('(')
                    polyp_pred = polyp[0]
                    polyp_score = float(polyp[1].replace(')', '').replace('\n', ''))
                else:
                    polyp_pred = '-'
                    polyp_score = 9.99

                final_lst = [variant_id, uniprot_pos, structure, struc_type, wt_res, mut_res, m3d_pred, sift_pred, sift_score,
                             polyp_pred, polyp_score, clinvar, humsavar]

                with open(variant_out_name, 'a', newline='') as var_file:
                    vari_writer = csv.writer(var_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
                    vari_writer.writerow(final_lst)
            else:
                continue


prot_file = 'protein_pos_table2.csv'
variant_file = 'variant_test_data.csv'

generate_variant_data(prot_file, variant_file, 'variant_test_out.csv')
