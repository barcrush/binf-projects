### Summary

**UniGene**
It is an experimental system of partitioning GenBank entries into a non-redundant set of gene-oriented clusters
A gene-oriented grouping of transcript sequences in the absence of reference genomes for a broad range of organisms.
Each UniGene cluster contains sequences that represent unique gene and information related to its expression 
profiles linked to which tissue type and map location.
A total of 59,500 UNIGENE clusters have been mapped.

Here, we would like to retrieve the information from these files (or perhaps from species files from UniGene, 
having the same format) for further manipulation and use. We will have to read each of the gene files, parse the 
lines using regular expressions, and deliver the retrieved data to a function that will further manipulate it. 
If we need to do that, it would be a good idea to store the data for each gene in a data structure, 
and then deliver the data structure to the function, or store each gene data structure in large list or dictionary for
further processing.

Furthermore, we create a script employed as a query program that assists in Unigene data annotation, i.e., providing gene information with respect to its expression profile across different tissues. In order to make this program bulletproof, we created some helper functions as well as unit testing scripts.
