training = read.csv("TrainingDataset.csv", na.strings="NaN")
test = read.csv("TestDataset.csv", na.strings="NaN")

#Sample submission-- column means
submission_colMeans = data.frame(id = test[,1])
for (var in names(training)[1:12]) {
  submission_colMeans[,var] = mean(training[,var], na.rm=TRUE)
}
write.csv(submission_colMeans, "sample_submission_using_training_column_means.csv", row.names=FALSE)


#randomForest benchmark submission:
library(randomForest)

#function for adding NAs indicators to dataframe and replacing NA's with a value---"cols" is vector of columns to operate on
#   (necessary for randomForest package)
appendNAs <- function(dataset, cols) {
  append_these = data.frame( is.na(dataset[, cols] ))
  names(append_these) = paste(names(append_these), "NA", sep = "_")
  dataset = cbind(dataset, append_these)
  dataset[is.na(dataset)] = -1
  return(dataset)
}

#replacements:
training <- appendNAs(training,13:ncol(training))
test <- appendNAs(test,2:ncol(test))

#begin building submission data frame:
submission_rf = data.frame(id = test$id)

#train a random forest (and make predictions with it) for each prediction column
for (var in names(training)[1:12]) {
  print(var)
  rf = randomForest(training[,13:ncol(training)],training[,var], do.trace=TRUE,importance=TRUE, sampsize = 100, ntree = 500)
  submission_rf[,var] = predict(rf, test[,2:ncol(test)])
}

write.csv(submission_rf, "RandomForestBenchmark.csv", row.names=FALSE)
