## main script 

rm(list = ls())
# setwd("~/Academics/gitProjects/myProjects/Mouse-protein-expr")
####### pacakges #######
packages <- c("gdata", "readxl", "tidyverse", "psych", "corrplot",
               "nnet", "NeuralSens", "neuralnet","e1071", "caret", "randomForest", "ipred", 
              "faraway","caret", "DataExplorer", "FeatureTerminatoR", "ggplot2",
              "FactoMineR", "devtools", "ggbiplot")

# dplyr: for dataNC manipulation
# tidyr: or dataNC wrangling
# psych: for pairs panel plot
# corrplot: for correlation matrix
# ROSE: for imputing imbalancortex.rawed classes
# nnet: for NN modeling
# neuralnet: for NN modeling
# e1071: for SVM implementation
# caret: for dataNC preparation and evaluation of model
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
# define the URL -- you could dynamically build this
#URL <- "https://archive.ics.uci.edu/ml/machine-learning-databases/00342/Data_Cortex_Nuclear.xls"
# download file
#download.file(URL, destfile="Data_Cortex_Nuclear.xls")
# load the file
ncortex.raw <- as.data.frame(read_excel("Data_Cortex_Nuclear.xls"))
head(ncortex.raw)
dim(ncortex.raw)
str(ncortex.raw)
# check categorical distribution
plot_bar(ncortex.raw[,-1])


########## pre-processing - I  ##########
# since we are focusing our analysis on the `class` variable, we are going to drop
# the rest of the categorical variables from the dataNC along with the `MouseID`column
ncortex <- subset(ncortex.raw, select = -c(MouseID, Behavior, Genotype, Treatment))
# We have the numeric features (77) and a multiclass target variable (1)

# factorize target variable
ncortex$class <- as.factor(ncortex.raw$class)

# check categorical distribution
table(ncortex$class)

head(ncortex)

# imputing missing values
# check the columns with NAs
featNA <- names(which(sapply(ncortex, anyNA)))
dataNA <- ncortex[, featNA]

# total number of NAs
sum(is.na(dataNA))
# check the distribution of NAs in each column
colSums(is.na(dataNA))   
# all columns have NAs below 50% of the sample size. Hence, they can be imputed.

### Imputation ###
# computing mean of all columns using colMeans()
means <- colMeans(dataNA, na.rm = TRUE)

# replacing NA with mean value of each column
for(i in colnames(dataNA)){
  dataNA[,i][is.na(dataNA[,i])] <- means[i]
}

# check missing values in our feature dataNC frame
sum(is.na(dataNA))

# replace the imputed features with the original dataNC
ncortex[,featNA] <- dataNA

# check basic statistics
summary(ncortex)

##### Split data set ###

dataNC <- reduced.dataNC
  
# 70/30 split
set.seed(100)
# getting 70% sampled index of the data without replacement
sampleIdx <- sample(1:nrow(dataNC), size=0.7 * nrow(dataNC), replace=FALSE)

# train
ncortex.train <- dataNC[sampleIdx, ]
dim(ncortex.train)
table(ncortex.train$Class)
train.class <- ncortex.train$Class

# test
ncortex.test <- dataNC[-sampleIdx, ]
dim(ncortex.test)
table(ncortex.test$Class)
test.class <- ncortex.test$Class

# Min-max scaling/Normalization function (range 0-1 for each column)
Z.normalize <- function(x) {
  return((x- min(x)) /(max(x)-min(x)))
}

numVar.train <- ncortex.train[,-ncol(ncortex.train)]
numVar.test <- ncortex.test[,-ncol(ncortex.test)]
# normalized train/test set
trainX <- data.frame(apply(numVar.train, 2, Z.normalize), "Class"=train.class)
dim(trainX)
testX <- data.frame(apply(numVar.test, 2, Z.normalize), "Class"=test.class)
dim(testX)

### Naive Bayes ###
library(klaR)
# fit the model
NB.model <- NaiveBayes(Class ~., data = trainX)
# make predictions
NB.pred <- predict(NB.model, testX, type="class")
# check reference and predicted classification
NB.confmat <- confusionMatrix(NB.pred$class, testX$Class)
NB.confmat

### Random Forest ###
library(randomForest)

# fit the model
RF.model <- randomForest(Class ~., data= trainX)
# make predictions
RF.pred <- predict(RF.model, testX, type = "class")
# check reference and predicted classification
RF.confmat <- confusionMatrix(as.factor(RF.pred), testX$Class)
RF.confmat


### multinomial logistic regression ###
# fit the model
MGR.model <- multinom(Class ~., data = trainX)
# make predictions
MGR.pred <- predict(MGR.model, newdata=testX, type="class")
# check reference and predicted classification
MGR.confmat <- confusionMatrix(as.factor(MGR.pred), testX$Class)
MGR.confmat

### Neural network ###
# nnet()

set.seed(998)
# initialize a vector for `accuracy`
accuracy <- c()

# create NN-optimization function
NN.func <- function(nntrain, nntest, nnrange) {
  ## NN.train: training data
  ## NN.test: testing data
  ## nnrange: number of neurons
  for (count in nnrange) {
    # print no. of neuron
    print(paste("Number of neurons used for model:", count))
    # fit the neural network --some regularization
    model <- nnet(Class ~ ., data = nntrain, size = count,
                  maxit=250, decay=0.01)
    # predictions
    predictions <- predict(model, nntest, type = "class")
    # table comparison
    nntable <- table(nntest$Class, predictions)
    # estimate accuracy
    accuracy[count] <- round(sum(diag(nntable) / sum(nntable)) * 100,2)
    # print corresponding accuracy
    print(paste("Estimated accuracy is", accuracy[count]))
    
  }
  return(accuracy)
}

# call the function and print
NN.accuracy <- NN.func(nntrain = trainX, nntest = testX, nnrange = c(2:10))
NN.accuracy

p <- apply(NN.accuracy,1, FUN= "which.max")
return(p)
# extract the optimal neuron number from accuracy
opt.nnum <- which.max(NN.accuracy)

print(paste("Optimal number of neuron for the model is", opt.nnum))
## Parameters of the NNET ------------------------------------------------------
hidden_neurons <- opt.nnum
iters <- 250
decay <- 0.1
#' ## TRAIN nnet NNET --------------------------------------------------------
# Create a formula to train NNET
form <- paste(names(trainX)[1:ncol(trainX)-1], collapse = " + ")
form <- formula(paste(names(trainX)[ncol(trainX)], form, sep = " ~ "))

set.seed(367)
mod <- nnet(form,
            data = trainX,
            linear.output = TRUE,
            size = hidden_neurons,
            decay = decay,
            maxit = iters)

# make predictions
nn.pred <- predict(mod, testX, type="class")
# check reference and predicted classification
nn.confmat <- confusionMatrix(as.factor(nn.pred), testX$Class)
nn.confmat

# mod should be a neural network classification model
# sens <- SensAnalysisMLP(mod, trData = nc.test, output_name = 'Class')
# combinesens <- CombineSens(sens, "sqmean")

#### SVM
## SVM: support vector machine
set.seed(995)
# fit the model
SVM.model <- svm(form, trainX, kernel= "radial", probability = TRUE)
# SVM Predictions
SVM.pred <- as.data.frame(predict(model, testX))
# Confusion Matrix
SVM.confmat <- confusionMatrix(SVM.pred[,1], testX$Class)
SVM.confmat
