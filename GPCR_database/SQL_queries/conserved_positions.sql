SELECT 	ref_totals.family_group,
		#ref_totals.alignment_member_pos,
        #ref_totals.deleterious,
		#ref_totals.tolerated,
		SUM(IF(ref_totals.deleterious > ref_totals.tolerated,1,0)) AS 'del_positions',
        SUM(IF(ref_totals.deleterious < ref_totals.tolerated,1,0)) AS 'tol_positions',
        COUNT(*) total_positions
FROM
	(SELECT ref_tab.alignment_member_pos,
		SUBSTRING_INDEX(ref_tab.alignment_member_pos, '_',1) AS 'family_group',
		SUM(IF(ref_tab.sift_prediction = 'deleterious',1,0)) AS 'deleterious',
		SUM(IF(ref_tab.sift_prediction = 'tolerated',1,0)) AS 'tolerated',
		COUNT(*) var_count
	FROM
		(SELECT ref_positions.alignment_member_pos,
			variant.variant_id,
			variant.sift_prediction,
			variant.polyphen_prediction,
			variant.m3d_prediction
			FROM	variant,
				protein_pos,
				alignment_member_pos,
				(SELECT 
					alignment_member_pos, conservation_score
				 FROM 
					conservation_score
				 WHERE
					conservation_score.conservation_score >= 0.7
				 GROUP BY 
					alignment_member_pos, conservation_score) AS ref_positions
			WHERE
					variant.protein_pos_id = protein_pos.protein_pos_id
			AND		protein_pos.protein_pos_id = alignment_member_pos.protein_pos_id
			AND		alignment_member_pos.alignment_member_pos = ref_positions.alignment_member_pos
			AND 	variant.sift_prediction != '-') AS ref_tab 
				
	GROUP BY alignment_member_pos
	ORDER BY alignment_member_pos) AS ref_totals
GROUP BY family_group
ORDER BY family_group
; 