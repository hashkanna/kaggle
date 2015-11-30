setwd('/Users/kanna/Sandbox/kaggle/walmart')
train <- read.csv('markdown_sales_train.csv')
train[is.na(train)] <- 0
test <- read.csv('markdown_sales_test.csv')
test[is.na(test)] <- 0
lmfit = lm( Weekly_Sales ~ MarkDown1 + MarkDown2 + MarkDown3 + MarkDown4 + MarkDown5, data=train )
result = predict(lmfit, newdata=test)
write.table(result, "kanna.csv", sep="\t", row.names=FALSE, col.names=TRUE) 
