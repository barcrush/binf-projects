## Analysis of class `Genotype` using h2o
Genotype <- ncortex.raw$Genotype
dataH2o <- dataNC
dataH2o$Genotype <- Genotype


# remove the `Class` from the features
dataEns <- dataH2o %>% select(-Class)

# Split the data frame into Train and Test dataset
## 75% of the sample size
s.size <- floor(0.70 * nrow(dataEns))

## set the seed to make your partition reproducible
set.seed(214)
idx <- sample(seq_len(nrow(dataEns)), size = s.size)
# train set
train_ens <- dataEns[idx, ]
# test set
test_ens <- dataEns[-idx, ]
