# based on https://www.kaggle.com/tqchen/otto-group-product-classification-challenge/understanding-xgboost-model-on-otto-data/code

setwd("/Users/kanna/Sandbox/kaggle/walmart_trip_type/")

require(xgboost)
require(methods)
require(data.table)
require(magrittr)
require(plyr)
train <- fread('train_keras_extra_features_weekday.csv', header = T, stringsAsFactors = F)
test <- fread('test_keras_extra_features_weekday.csv', header = T, stringsAsFactors = F)

dim(train)
train[1:6,1:5, with =F]
test[1:6,1:5, with =F]

visit_number = test[['VisitNumber']]
train[,VisitNumber := NULL]
test[,VisitNumber := NULL]

y <- mapvalues(train[['TripType']], from=c(3, 4, 5, 6, 7, 8, 9, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 999), to=c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37))

#We remove label column from training dataset, otherwise **XGBoost** would use it to guess the labels!
train[, TripType :=NULL]

#data.table is an awesome implementation of data.frame, unfortunately it is not a format supported natively by **XGBoost**. We need to convert both datasets (training and test) in numeric Matrix format.
trainMatrix <- train[,lapply(.SD,as.numeric)] %>% as.matrix
testMatrix <- test[,lapply(.SD,as.numeric)] %>% as.matrix

# Cross Validation
# Basically **XGBoost** will divide the training data in `nfold` parts, then **XGBoost** will retain the first part and use it as the test data. Then it will reintegrate the first part to the training dataset and retain the second part, do a training and so on...
numberOfClasses <- max(y) + 1
param <- list("objective" = "multi:softprob",
              "eval_metric" = "mlogloss",
              "num_class" = numberOfClasses)

cv.nround <- 5
cv.nfold <- 3

bst.cv = xgb.cv(param=param, data = trainMatrix, label = y, 
                nfold = cv.nfold, nrounds = cv.nround)

nround = 100
bst = xgboost(param=param, data = trainMatrix, label = y, nrounds=nround)

# Make prediction
pred = predict(bst,testMatrix)
pred = matrix(pred,numberOfClasses,length(pred)/numberOfClasses)
pred = t(pred)

# Output submission
#pred = format(pred, digits=2,scientific=F) # shrink the size of submission
#pred = data.frame(1:nrow(pred),pred)
pred = data.frame(visit_number, pred)
names(pred) = c("VisitNumber","TripType_3","TripType_4","TripType_5","TripType_6","TripType_7","TripType_8","TripType_9","TripType_12","TripType_14","TripType_15","TripType_18","TripType_19","TripType_20","TripType_21","TripType_22","TripType_23","TripType_24","TripType_25","TripType_26","TripType_27","TripType_28","TripType_29","TripType_30","TripType_31","TripType_32","TripType_33","TripType_34","TripType_35","TripType_36","TripType_37","TripType_38","TripType_39","TripType_40","TripType_41","TripType_42","TripType_43","TripType_44","TripType_999")
write.csv(pred,file='submission_xgb2.csv', quote=FALSE, row.names=FALSE)




