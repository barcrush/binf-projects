# loading libraries
# integrates transcript-level abundance estimates
library(tximport)
# it allows us to read tabular data quickly
library(readr)	
# carry out differential analysis of count data using shrinkage estimation for dispersion and fold changes
library(DESeq2)
# Loading the kable library to display formatted tables
library(knitr)

# Load BLAST results as a table
blastFile <- "/scratch/SampleDataFiles/Annotation/transcriptBlast.txt"
keggFile <- "/scratch/SampleDataFiles/Annotation/kegg.txt"
koFile <- "/scratch/SampleDataFiles/Annotation/ko.txt"

blast <- read.table(blastFile, sep="\t", header=FALSE)
# Set column names to match fields selected in BLAST
colnames(blast) <- c("trans", "sp", "qlen", "slen", "bitscore", 
                     "length", "nident", "pident", "evalue", "ppos")
# Calculate the percentage of identical matches relative to subject length
blast$cov <- blast$nident/blast$slen
# Filter for at least 50% coverage of subject(SwissProt) sequence
blast <- subset(blast, cov > .5)
# Check the blast table
kable(head(blast))

# Load SwissProt to KEGG as a table
kegg <- read.table(keggFile, sep="\t", header=FALSE)
# Set the Swissprot to KEGG column names
colnames(kegg) <- c("sp", "kegg")
# Remove the up: prefix from sp column
kegg$sp <- gsub("up:", "", kegg$sp)
# Check the kegg table
kable(head(kegg))

# Merge BLAST and SwissProt-to-KEGG
blastKegg <- merge(blast, kegg)
# Check the merged table
kable(head(blastKegg))

# Load KEGG to KO as a table
ko <- read.table(koFile, sep="\t", header=FALSE)
# Set column names
colnames(ko) <- c("kegg", "ko")
# Check the ko table
kable(head(ko))

# Merge KOs
blastKo <- merge(blastKegg, ko)
# Check the blast ko table
kable(head(blastKo))

tx2gene <- unique(subset(blastKo, select=c(trans, ko)))
# Check the tx2gene table
kable(head(tx2gene))

# Write as a csv file, excluding row.names
write.csv(tx2gene, file="tx2gene.csv", row.names=FALSE)


#### Differential expression analysis ####


# reading the merged transcript-ko file (tx2gene) from mergeKo script
tx2gene <- read.csv("tx2gene.csv")
# head(tx2gene) - for checking the csv file

samples <- read.csv("pallida_A.csv", header=TRUE)
# head(samples) - for checking the sample

# setting file path to quant/ having quant.sf (consists of salmon abundance estimatio of each sample)
files <- file.path("quant", samples$Sample, "quant.sf")
# differential analysis of estimates
txip <- tximport(files, type="salmon", tx2gene=tx2gene)

dds <- DESeqDataSetFromTximport(txip, colData = samples, design = ~ Menthol + Vibrio)

# using counts and average transcript lengths from tximport
dds$Vibrio <- relevel(dds$Vibrio, ref = "Control")
dds$Menthol <- relevel(dds$Menthol, ref = "Control")
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]
dds <- DESeq(dds)

padj <- .05
minLog2FoldChange <- .5
dfAll <- data.frame()
# Get all DE results except Intercept, and "flatten" into a single file.
for (result in resultsNames(dds)){
  if(result != 'Intercept'){
    res <- results(dds, alpha=.05, name=result)
    dfRes <- as.data.frame(res)
    dfRes <- subset(subset(dfRes, select=c(log2FoldChange, padj)))
    dfRes$Factor <- result
    dfAll <- rbind(dfAll, dfRes)
  }
}
# head(kable(dfAll))

# filterin dfAll to make padj value are less than 0.05
filterAll <- subset(dfAll, padj < 0.05)
filterAll <- cbind(rownames(filterAll), data.frame(filterAll, row.names=NULL))
colnames(filterAll)[1] <- "ko"
# check
# head(kable(filterAll))

# load the pathways as table
path2File <- "/scratch/SampleDataFiles/Annotation/path.txt"
pathways <- read.table(path2File, sep='\t', header=F)
colnames(pathways) <- c("ko", "Pathways")

# load pathway names as table
ko_pathway <- "/scratch/SampleDataFiles/Annotation/ko"
pathwayNames <- read.table(ko_pathway, sep="\t", header=F)
colnames(pathwayNames) <- c("Pathways", "Pathway names")

# Merge pathways and pathways names 
mergePaths <- merge(pathways, pathwayNames)

# merging merge_paths with filtering data
deAnnotated <- merge(mergePaths, filterAll)
# check the final table before writing it
# kable(deAnnotated)

# write the output
write.csv(deAnnotated, file="deAnnotated.csv")
