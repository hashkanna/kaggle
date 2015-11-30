############################################
## Use H2O to create random forest 
## against the entire dataset in 
## just a couple minutes
##
## This is a starter script, using defaults
## so it can be improved. And RF may not be
## the best algorithm for this problem. But
## the script shows that it can be done in 
## R fairly quickly, in fact. And it will scale
## well to adding many more columns. 
##
## To better fit MAE, the log of the 
## target has been used: log1p/expm1
## 
## The final step blends with the Marshall-Palmer 
## benchmark 50/50.
##
## The API for h2O.randomForest is shown at the 
## bottom of the script

library(h2o)
library(data.table)
library(Metrics)
h2o.init(nthreads = -1)

## use data table to only read the Estimated, Ref, and Id fields
print(paste("reading training file:",Sys.time()))
train<-fread("../input/train.csv",select=c(1,4,24))

trainHex<-as.h2o(train[,.(
  target = log1p(mean(Expected)),
  meanRef = mean(Ref,na.rm=T),
  sumRef = sum(Ref,na.rm=T),
  records = .N,
  naCounts = sum(is.na(Ref))
),Id][records>naCounts,],destination_frame="train.hex")

rfHex<-h2o.randomForest(x=c("meanRef","records","naCounts"),
                        y="target", ntrees = 100, max_depth=40, training_frame=trainHex,model_id="rfStarter.hex")

rfHex

rm(train)

test<-fread("../input/test.csv",select=c(1,4))
testHex<-as.h2o(test[,.(
  meanRef = mean(Ref,na.rm=T),
  sumRef = sum(Ref,na.rm=T),
  records = .N,
  naCounts = sum(is.na(Ref))
),Id],destination_frame="test.hex")

submission<-fread("../input/sample_solution.csv")
predictions<-as.data.frame(h2o.predict(rfHex,testHex))
submission$Expected<-expm1(predictions$predict)*0.5+submission$Expected*0.5

summary(submission)
write.csv(submission,"randomForest_starter.csv",row.names=F)
