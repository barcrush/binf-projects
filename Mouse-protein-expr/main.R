## main script 

nc <- read.csv("Data_Cortex_Nuclear.csv", header = TRUE)

summary(nc)
str(nc)

table(nc$Genotype)
table(nc$Treatment)
table(nc$Behavior)
table(nc$class)
# check categorical distribution

library(rpart)

ncClass <- nc$class




