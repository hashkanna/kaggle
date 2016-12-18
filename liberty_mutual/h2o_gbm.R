
# This script creates a sample submission using a GBM on H2O
#
# Click "fork" to run this script yourself and make tweaks

setwd("/Users/kanna/Sandbox/kaggle/liberty_mutual")
library(readr)
library(h2o)
set.seed(1)

cat("Reading data\n")
train <- read_csv("train.csv")
test <- read_csv("test.csv")

# We'll convert all the characters to factors so we can train a randomForest model on them
extractFeatures <- function(data) {
  character_cols <- names(Filter(function(x) x=="character", sapply(data, class)))
  for (col in character_cols) {
    data[,col] <- as.factor(data[,col])
  }
  return(data)
}

trainFea <- extractFeatures(train)
testFea  <- extractFeatures(test)

localH2O<-h2o.init()
h2o_train <- as.h2o(localH2O,train)
h2o_test<-as.h2o(localH2O,extractFeatures(testFea[,2:33]))

cat("Training model\n")
gbm = h2o.gbm(x = 3:34, y = 2, 
              training_frame = h2o_train,
              distribution="AUTO",
              nfolds = 1,
              seed = 666,
              ntrees = 700,
              max_depth = 7,
              min_rows = 5,
              learn_rate = 0.02)

cat("Making predictions\n")
submission <- data.frame(Id=test$Id)
pred<-as.data.frame(h2o.predict(gbm, h2o_test))
submission$Hazard <- pred$predict
write_csv(submission, "1_h2o_gbm_benchmark.csv")
