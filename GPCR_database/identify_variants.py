
with open('student_project_gpcr.csv', 'r') as m3d_gpcr: # importing all the m3ddb data
    gpcr = m3d_gpcr.readlines()


def conserved_variants(id_file, c_file, v_file):

    """Returns information about damaging variant in conserved region of proteins

    
    Parameters
    ----------

    id_file : a file txt file of comma-separated Uniprot IDs

    c_file: output txt file from https://compbio.cs.princeton.edu/conservation/score.html; 
    Uniprot IDs to be inputted into conservation alignment server require a BLAST alignment file first; Uniprot IDs run through BLAST MUST be in 
    same order as the IDs in the id_file


    v_file : file containing variants in same format as extracted from M3DDB


    Returns
    -------

    Total number of damaging variants, number & percentage of which are located in conserved regions 
     """
    
    with open(id_file, 'r') as ids_file: # txt file of comma separated Uniprot IDs
        ids = ids_file.read() 
    ids = ids.strip().split(',')
    
    with open(v_file, 'r') as var: # file containing the variant information (student_project_gpcr.csv)
        variants = var.readlines()
        
    with open(c_file, 'r') as cons: # txt file containing the conservation output from website 
        cons_scores = cons.readlines()
        
        
    total_damaging_variants = 0
    total_cons_variants = 0
    
    for i in range(len(ids)):
    
        print("Analysing", str(ids[i]))
        
        vals = []
        for entry in cons_scores:
            lst = entry.split('\t')
            value = float(lst[1])
            if lst[2][i] != '-': # retrieving conservation scores for non-gap positions 
                vals.append(value)       
        
        
        cons_positions = []
        for ind, n in enumerate(vals): # finding index of most conserved positions
            if n >= 0.5:
                cons_positions.append(int(ind+1))
        
    
        
        damaging_positions = []
        for entry in variants: # extracting the Uniprot positions of damaging variants from M3DDB 
            lst = entry.split(',')
            if lst[1] == ids[i] and 'damaging' in lst[15]:
                damaging_positions.append(int(lst[5])) # adding Uniprot position number to list 
               
        
        print("Number of damaging variants in", str(ids[i]),':', str(len(damaging_positions)))        
        
        total_damaging_variants += len(damaging_positions)
        
        count = 0
        for n in damaging_positions: # counting how many damaging variants are at same index as conserved index
            if n in cons_positions:
                count += 1
                
        print('Number of damaging variants in', str(ids[i]), 'that fall in conserved region:', str(count), '\n')
        total_cons_variants += count
    
    print("Total damaging variants:", str(total_damaging_variants), '\n')
    print("Total damaging variants in conserved regions:", str(total_cons_variants), '\n')
    print('Percent of damaging variants in conserved regions:')
    return (total_cons_variants/total_damaging_variants) * 100
    
