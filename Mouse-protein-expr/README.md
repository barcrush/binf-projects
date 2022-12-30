## Summary

The data set consists of the expression levels of 77 proteins/protein modifications that produced detectable signals in the nuclear fraction of the cortex. There are 38 control mice and 34 trisomic mice (Down syndrome), for a total of 72 mice. In the experiments, 15 measurements were registered of each protein per sample/mouse. Therefore, for control mice, there are 38x15, or 570 measurements, and for trisomic mice, there are 34x15, or 510 measurements. The dataset contains a total of 1080 measurements per protein. Each measurement can be considered as an independent sample/mouse. The eight classes of mice are described based on genotype, behavior, and treatment features. 

According to genotype, mice can be controlled or trisomic. According to behavior, some mice have been stimulated to learn (context-shock) and others have not (shock-context) and to assess the effect of the drug memantine in recovering the ability to learn in trisomic mice, some mice have been injected with the drug and others have not.

Graphical interpretation of the study is show below:
![tileshop](https://user-images.githubusercontent.com/90593831/210114119-2b9084d6-6adc-43bf-a32d-a9cc6e0441b2.jpeg)

Firstly, we tried to extract features (genes) that were potentially responsible for a particular learning outcome and tried to compare our results with the previous studies using Filtration and extraction methods to select features of defined learning outcomes, and then we qualitatively isolated features from PCA.

Secondly, for multi-class classification, the initial pre-processing involves handling missing values, sub-setting data for classification, and reducing features for improving our analysis. We used 4 models for classification analysis – Naïve Bayes, ANN, Multinomial logistic regression, and randomForest for the stacked learner. For evaluation, we monitored metrics such as accuracy, precision, F1-score, ROC curve, and AUC for all the models and choose the ideal model that generalizes the data set and reflects the best performance by considering the above metrics.


### References
1. Data generated: https://archive.ics.uci.edu/ml/datasets/Mice+Protein+Expression
2. 

