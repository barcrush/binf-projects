SELECT *
FROM 
(SELECT almp1.alignment_member_pos,
	    var1.protein_pos_id,
        var1.variant_id,
	    var1.residue_wt,
	    var1.residue_mnt,
		var1.sift_prediction,
        var1.sift_score,
        pp1.uniprot_id,
        prot1.gene_name
        

FROM   alignment_member_pos almp1,
	   protein_pos pp1,
       protein prot1,
       variant var1,
       alignment al1,
       alignment_protein alp1
       
WHERE  al1.alignment_name="GPCR_A8"
AND	   alp1.alignment_id = al1.alignment_id
AND    almp1.alignment_member_id = alp1.alignment_member_id
AND    pp1.protein_pos_id = almp1.protein_pos_id
AND    var1.protein_pos_id = pp1.protein_pos_id
AND    prot1.uniprot_id = pp1.uniprot_id)  table1


WHERE EXISTS (
	SELECT * 
    FROM 
		(SELECT almp2.alignment_member_pos,
				pp2.uniprot_id,
				prot2.gene_name,
				var2.protein_pos_id,
				var2.variant_id,
				var2.residue_wt,
				var2.residue_mnt,
				var2.sift_prediction,
				var2.sift_score

		FROM    alignment_member_pos almp2,
				protein_pos pp2,
				protein prot2,
				variant var2,
				alignment al2,
				alignment_protein alp2
       
		WHERE  al2.alignment_name="GPCR_A8"
		AND	   alp2.alignment_id = al2.alignment_id
		AND    almp2.alignment_member_id = alp2.alignment_member_id
		AND    pp2.protein_pos_id = almp2.protein_pos_id
		AND    var2.protein_pos_id = pp2.protein_pos_id
		AND    prot2.uniprot_id = pp2.uniprot_id) table2
        
   
   WHERE table1.variant_id != table2.variant_id
    AND table1.residue_wt = table2.residue_wt
    AND  table1.residue_mnt = table2.residue_mnt
    AND  table1.alignment_member_pos = table2.alignment_member_pos)
ORDER BY table1.residue_wt, table1.residue_mnt, table1.sift_score, table1.alignment_member_pos ; 
