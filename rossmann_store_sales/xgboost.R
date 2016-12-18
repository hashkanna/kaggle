library(data.table)  
library(xgboost)

setwd("/Users/kanna/Sandbox/kaggle/rossmann_store_sales/")
cat("reading the train and test data (with data.table) \n")
train <- fread("train.csv",stringsAsFactors = F)
test  <- fread("test.csv",stringsAsFactors = F)
store <- fread("store.csv",stringsAsFactors = F)

# There are some NAs in the integer columns so conversion to zero
train[is.na(train)]   <- 0
test[is.na(test)]   <- 0
store[is.na(store)]   <- 0

train <- train[Sales > 0,]  ## We are not judged on 0 sales records in test set
## See Scripts discussion from 10/8 for more explanation.
train <- merge(train,store,by="Store")
test <- merge(test,store,by="Store")


cat("train data column names and details\n")
summary(train)
cat("test data column names and details\n")
summary(test)

## more care should be taken to ensure the dates of test can be projected from train
## decision trees do not project well, so you will want to have some strategy here, if using the dates
train[,Date:=as.Date(Date)]
test[,Date:=as.Date(Date)]

# seperating out the elements of the date column for the train set
train[,day:=as.integer(format(Date, "%d"))]
train[,month:=as.integer(format(Date, "%m"))]
train[,year:=as.integer(format(Date, "%y"))]
train[,Store:=as.factor(as.numeric(Store))]

test[,day:=as.integer(format(Date, "%d"))]
test[,month:=as.integer(format(Date, "%m"))]
test[,year:=as.integer(format(Date, "%y"))]
test[,Store:=as.factor(as.numeric(Store))]

## log transformation to not be as sensitive to high sales
## decent rule of thumb: 
##     if the data spans an order of magnitude, consider a log transform
train[,logSales:=log1p(Sales)]

cat("assuming text variables are categorical & replacing them with numeric ids\n")
for (f in colnames(train)) {
  if (class(train[[f]])=="character") {
    levels <- unique(c(train[[f]], test[[f]]))
    train[[f]] <- as.integer(factor(train[[f]], levels=levels))
    test[[f]]  <- as.integer(factor(test[[f]],  levels=levels))
  }
}

## Set up variable to use all features other than those specified here
features<-colnames(train)[!(colnames(train) %in% c("Id","Date","Sales","logSales","Customers"))]

# Define RMPSE function for evaluation during xgb training
RMPSE<- function(preds, dtrain) {
  labels <- getinfo(dtrain, "label")
  elab<-exp(as.numeric(labels))-1
  epreds<-exp(as.numeric(preds))-1
  err <- sqrt(mean((epreds/elab-1)^2))
  return(list(metric = "RMPSE", value = err))
}

tra<-train[, .SD, .SDcols=features]
nrow(train)
h<-sample(nrow(train),10000)

dval<-xgb.DMatrix(data=data.matrix(tra[h,]),label=log(train$Sales+1)[h])
dtrain<-xgb.DMatrix(data=data.matrix(tra[-h,]),label=log(train$Sales+1)[-h])

watchlist<-list(val=dval,train=dtrain)
param <- list(  objective           = "reg:linear", 
                booster = "gbtree",
                eta                 = 0.02, # 0.06, #0.01,
                max_depth           = 10, #changed from default of 8
                subsample           = 0.9, # 0.7
                colsample_bytree    = 0.7 # 0.7
                #num_parallel_tree   = 2
                # alpha = 0.0001, 
                # lambda = 1
)

clf <- xgb.train(   params              = param, 
                    data                = dtrain, 
                    nrounds             = 3000, #300, #280, #125, #250, # changed from 300
                    verbose             = 0,
                    early.stop.round    = 100,
                    watchlist           = watchlist,
                    maximize            = FALSE,
                    feval=RMPSE
)
pred1 <- exp(predict(clf, data.matrix(test[, .SD, .SDcols=features]))) -1
submission <- data.frame(Id=test$Id, Sales=pred1)
cat("saving the submission file\n")
write.csv(submission, "result10_rounds6000_xgb.csv", row.names = F)