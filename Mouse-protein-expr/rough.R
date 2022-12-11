###########################################
# forward selection


##varaible importance
data2 <- reduced.dataNC
### roc_curve area as score
roc_imp <- filterVarImp(x= data2[,-ncol(data2)], y = data2[,ncol(data2)])
#sort the score in decreasing order
roc_imp <- data.frame(cbind(variable = rownames(roc_imp), score = roc_imp[,1]))
roc_imp$score <- as.double(roc_imp$score)
roc_scores <- roc_imp[order(roc_imp$score,decreasing = TRUE),]
roc.filter <- sum(roc_scores[,2] > 0.7)
roc.feat <- ncortex[,roc_scores[,1][1:roc.filter]]
roc.feat$Class <- ncortex$class

ncol(roc.feat)
head(roc.feat)

### correlation
dataNC <- ncortex
# scale data
dataNC.scale <- scale(dataNC[,-ncol(dataNC)],center=TRUE,scale=TRUE)
# compute the correlation matrix
corMatNC <- cor(dataNC.scale)
# visualize the matrix, clustering features by correlation index
corrplot(corMatNC, order = "hclust")
# After inspecting the matrix, we set the correlation threshold at 0.75
# Apply correlation filter at 0.75
highlyCor <- findCorrelation(corMatNC, 0.75)
#then we remove all the variable correlated with more 0.75.
features1 <- dataNC.scale[,-highlyCor]
corMatNC <- cor(features1)
corrplot(corMatNC, order = "hclust")

Class <- dataNC$class
reduced.dataNC <- data.frame(features1, Class)

ncol(reduced.dataNC)
head(reduced.dataNC)


# Now it is possible to filter out “redundant” features by examining in detail the
# correlation matrix. Remember that the closer the correlation between two variables
# is to 1, the more related their behavior and the more redundant one is with respect to the other.

###### PCA #######
# PCA with function PCA
pca <- PCA(reduced.dataNC[,-78], scale.unit=TRUE, graph=F)
pca.var <- pca$var$cos2
pca$var$cos2
#scale all the features,  ncp: number of dimensions kept in the results (by default 5)
dimdesc(pca)
# This line of code will sort the variables the most linked to each PC. 
#  It is very useful when you have many variables.

plot(pca, choix = "var", shadow = TRUE, select = "cos2")
fviz_eig(pca, addlabels = TRUE, ylim = c(0, 50))

fviz_pca_var(pca, col.var = "cos2",
             gradient.cols = c("#FFCC00", "#CC9933", "#660033", "#330033"),
             repel = TRUE) 
ggbiplot(pca, choices = c(3,4), repel = TRUE, select.var = list(contrib = 5)) +
  ggtitle("PCA of NC dataset")+
  theme_minimal()+
  theme(legend.position = "bottom")


ggbiplot(pca, ellipse=TRUE, groups=dataNC$class) +
  scale_colour_manual(name="Origin", values= c("forest green", "red3", "dark blue",
                                               "black", "yellow", "cyan", "coral", "deeppink"))+
  ggtitle("PCA of NC dataset")+
  theme_minimal()+
  theme(legend.position = "bottom")


# calculate percentage variance explained using output from the PCA
varExp <- (pca.nc$sdev^2) / sum(pca.nc$sdev^2) * 100

# create a scree plot
qplot(1:length(varExp), varExp) + 
  geom_line() + 
  xlab("Principal Component") + 
  ylab("Variance Explained") +
  ggtitle("Scree Plot") 

sum(varExp[1:10])

## randomForest
#train random forest model and calculate feature importance
rf = RF.model <- randomForest(class ~., data = feat1)
var_imp <- varImp(rf, scale = FALSE)
#sort the score in decreasing order
var_imp_df <- data.frame(cbind(variable = rownames(var_imp), score = var_imp[,1]))
var_imp_df$score <- as.double(var_imp_df$score)
rf_scores <- var_imp_df[order(var_imp_df$score,decreasing = TRUE),]
rf.filter <- sum(rf_scores$score > 10)
rf.feat <- ncortex[,rf_scores$variable[1:rf.filter]]
rf.feat$Class <- ncortex$class

ncol(rf.feat)

ggplot(rf_scores, aes(x=reorder(variable, score), y=score)) + 
  geom_point() +
  geom_segment(aes(x=variable,xend=variable,y=0,yend=score)) +
  ylab("IncNodePurity") +
  xlab("Variable Name") +
  coord_flip()

#### final feature selection ###

# Using recursive feature extraction method
data <- feat1
colnum <- ncol(data)
x <- data[,-colnum]
y <- data[,colnum]
# Training: 80%; Test: 20%
set.seed(123)
# split 80/20
idx = sample(1:nrow(data), size=0.7*nrow(data), replace=TRUE)

# train/test set of numeric variables
x_train <- x[idx, ]
y_train <- y[idx]

# train/test set of target variable
x_test  <- x[-idx,]
y_test  <- y[-idx]


# define the control using a random forest selection function
rfe.control <- rfeControl(functions = nbFuncs, # random forest
                      method = "repeatedcv", # repeated cv
                      repeats = 5, # number of repeats
                      number = 10) # number of folds

# run RFE
rfe.results <- rfe(x = x_train, 
                   y = droplevels(y_train), 
                   sizes = c(1:24),
                   rfeControl = rfe.control)
# check the results
rfe.results

# Print the selected features
selected.feat <- predictors(rfe.results)

# Print the results visually
ggplot(data = rfe.results, metric = "Accuracy") + theme_bw()

varImp.feat <- data.frame(feature = row.names(varImp(rfe.results))[1:20],
                          importance = varImp(rfe.results)[1:20, 1])

ggplot(data = varImp.feat, 
       aes(x = reorder(feature, -importance), y = importance, fill = feature)) +
  geom_bar(stat="identity") + labs(x = "Features", y = "Variable Importance") + 
  geom_text(aes(label = round(importance, 2)), vjust=1.6, color="white", size=4) + 
  theme_bw() + theme(legend.position = "none")

##################----------------------------------
# neurannet()
nc.train <- trainX
nc.test <- testX

nn = neuralnet(Class ~., data=nc.train, hidden=9, linear.output = FALSE)
plot(nn)

tablePrediction <- function(data){ 
  predictions <- data.frame(compute(nn, data.frame(data[,-ncol(data)]))$net.result) 
  labels <- c("c-CS-m", "c-CS-s", "c-SC-m", "c-SC-s", "t-CS-m", "t-CS-s", "t-SC-m", "t-SC-s") 
  pred.label <- data.frame(max.col(predictions)) %>%  
    mutate(prediction=labels[max.col.predictions.])
  confMat <- confusionMatrix(data$Class, 
                             as.factor(pred.label[,2]))
}

train.pred <- tablePrediction(nc.train)
train.pred
test.pred <- tablePrediction(nc.test)
test.pred