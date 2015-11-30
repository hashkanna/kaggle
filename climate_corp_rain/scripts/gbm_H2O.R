library(h2o)
library(data.table)
library(Metrics)
h2o.init(nthreads=-1)

## use data table to only read the Estimated, Ref, and Id fields
print(paste("reading training file:",Sys.time()))
train<-fread("../input/train.csv",select=c(1,4,24))

#Cut off outliers of Expected >= 70
train <- subset(train, Expected < 69)

trainHex<-as.h2o(train[,.(
  target = log1p(mean(Expected)),
  meanRef = mean(Ref,na.rm=T),
  sumRef = sum(Ref,na.rm=T),
  records = .N,
  naCounts = sum(is.na(Ref))
),Id][records>naCounts,],destination_frame="train.hex")

gbmHex<-h2o.gbm(x=c("meanRef","records","naCounts"),
                y="target",training_frame=trainHex,model_id="gbmStarter.hex",
                distribution="AUTO",
                nfolds = 1,
                seed = 666,
                ntrees = 2000,
                max_depth = 7,
                min_rows = 10,
                learn_rate = 0.015)

rm(train)
gbmHex

test<-fread("../input/test.csv",select=c(1,4))
testHex<-as.h2o(test[,.(
  meanRef = mean(Ref,na.rm=T),
  sumRef = sum(Ref,na.rm=T),
  records = .N,
  naCounts = sum(is.na(Ref))
),Id],destination_frame="test.hex")

submission <-fread("../input/sample_solution.csv")
predictions<-as.data.frame(h2o.predict(gbmHex,testHex))
submission$Expected <- expm1(predictions$predict)*0.7 + submission$Expected*0.3

summary(submission)
write.csv(submission,"gbm_H2O.csv",row.names=F)
