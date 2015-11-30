library(h2o)
library(data.table)
library(Metrics)
library(bit64)

## use data table to read the file
print(paste("reading training file:",Sys.time()))
train<-fread("train_extra_features.csv",stringsAsFactors = T)
test<-fread("test_extra_features.csv",stringsAsFactors = T)

train[,TripType:=as.factor(as.numeric(TripType))]

#train_length_dt = train[,list(ItemCount=length(Upc)),by=VisitNumber]
#test_length_dt = test[,list(ItemCount=length(Upc)),by=VisitNumber]

# set the ON clause as keys of the tables:
#setkey(train,VisitNumber)
#setkey(test,VisitNumber)
#setkey(train_length_dt,VisitNumber)
#setkey(test_length_dt,VisitNumber)
# perform the join, eliminating not matched rows from Right
#train <- train[train_length_dt, nomatch=0]
#test <- test[test_length_dt, nomatch=0]

#train <- unique(train[, c("VisitNumber", "Weekday", "ItemCount", "TripType"), with=FALSE])
#test <- unique(test[, c("VisitNumber", "Weekday", "ItemCount"), with=FALSE])

## Use H2O's random forest
## Start cluster with all available threads
h2o.init(nthreads=-1,max_mem_size='6G')
## Load data into cluster from R
trainHex<-as.h2o(train)

#features<-colnames(train)[(colnames(train) %in% c("Weekday", "DepartmentDescription"))]
#features<-colnames(train)[(colnames(train) %in% c("Weekday", "ItemCount"))]
features<-colnames(train)

## Train a random forest using all default parameters
rfHex <- h2o.randomForest(x=features,
                          y="TripType", 
                          ntrees = 100,
                          max_depth = 30,
                          nbins_cats = 1115, 
                          training_frame=trainHex)

summary(rfHex)
cat("Predicting Trip Type\n")
## Load test data into cluster from R
testHex<-as.h2o(test)

## Get predictions out; predicts in H2O, as.data.frame gets them into R
predictions<-as.data.frame(h2o.predict(rfHex,testHex))
pred <- predictions[,1]
summary(pred)

submission <- data.frame(Id=test$VisitNumber, TripType=pred)
#res = submission[,list(TripType=max(names(which(table(TripType)==max(table(TripType)))))),by=Id]
res = submission

cat("saving the submission file\n")
write.csv(res, "result3_h2o_rf.csv.prep",row.names=F)

