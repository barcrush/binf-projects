## Parameters of the NNET ------------------------------------------------------
hid_neurons <- 14
#' ## TRAIN NNET --------------------------------------------------------

set.seed(367)
mod <- nnet(formula.NC,
            data = trainX,
            linear.output = TRUE,
            size = hid_neurons, trace = F)

# make predictions
nn.pred <- predict(mod, validX, type="class")
# check reference and predicted classification
nn.confmat <- confusionMatrix(as.factor(nn.pred), validX$Class)
nn.confmat

### k-fold cross-validation
my.grid <- expand.grid(.decay = c(0.5, 0.1), .size = c(5, 6, 7))
nn.fit <- train(formula.NC, data = trainX, 
                method = "nnet", 
                maxit = 1000, tuneGrid = my.grid, trace = F, linout = 1)    

nn.pred <- predict(nn.fit, validX)
# check reference and predicted classification
nn.confmat <- confusionMatrix(as.factor(nn.pred), validX$Class)
nn.confmat

## svm
svm.fit <- svm(formula.NC, data=trainX, 
              method="C-classification", kernal="radial", 
              gamma=0.1, cost=10)

svm.pred <- predict(svm.fit, validX)
svm.confmat <- confusionMatrix(svm.pred, validX$Class)
svm.confmat

# in creating the folds we specify the target feature (dependent variable) and # of folds
folds = createFolds(trainX$Class, k = 10)
# in cv we are going to applying a created function to our 'folds'
cv = lapply(folds, function(x) { # start of function
  # in the next two lines we will separate the Training set into it's 10 pieces
  training_fold = trainX[-x, ] # training fold =  training set minus (-) it's sub test fold
  test_fold = trainX[x, ] # here we describe the test fold individually
  # now apply (train) the classifer on the training_fold
  classifier = nnet(formula.NC,
                    data = trainX,
                    linear.output = TRUE,
                    size = hid_neurons, trace = F)
  # next step in the loop, we calculate the predictions and cm and we equate the accuracy
  # note we are training on training_fold and testing its accuracy on the test_fold
  y_pred = predict(classifier, newdata = test_fold, type="class")
  cm = confusionMatrix(as.factor(y_pred), test_fold$Class)
  return(cm$overall[1])
})

CV <- t(as.data.frame(cv))
mean(CV)

set.seed(232)
# fit the model
MGR.model <- multinom(formula.NC, data = trainX, trace = F)
# make predictions using valid set
MGR.pred <- predict(MGR.model, newdata=validX)
# check reference and predicted classification
MGR.cm.valid <- confusionMatrix(validX$Class, MGR.pred)
MGR.cm.valid
MGR.cm.valid$overall[1:2]
 
