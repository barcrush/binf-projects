## main script 

rm(list = ls())
####### pacakges #######
packages <- c("dplyr", "tidyr", "psych", "corrplot", "ROSE", "nnet", "neuralnet",
              "e1071", "caret", "rpart","randomForest", "ipred")
# dplyr: for data manipulation
# tidyr: or data wrangling
# psych: for pairs panel plot
# corrplot: for correlation matrix
# ROSE: for imputing imbalanced classes
# nnet: for NN modeling
# neuralnet: for NN modeling
# e1071: for SVM implementation
# caret: for data preparation and evaluation of model
# rpart: for decision tree regularization
# randomForest: for ensemble model-1 (random forest)
# ipred: for ensemble model-2 (bagging)

# Install packages not yet installed
installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

# Packages loading
invisible(lapply(packages, library, character.only = TRUE))


######### data review ########
nc <- read.csv("Data_Cortex_Nuclear.csv", header = TRUE)

summary(nc)
str(nc)

table(nc$Genotype)
table(nc$Treatment)
table(nc$Behavior)
table(nc$class)
# check categorical distribution

########## pre-processing #########







