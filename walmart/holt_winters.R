#install.packages("forecast")
library(forecast)
setwd('/Users/kanna/Sandbox/kaggle/walmart')
#plot.ts(tmp_1_1_ts)
#plot(tmp_1_1_ts_forecasts)
#plot.forecast(tmp_1_1_ts_forecasts_result)

train = read.csv('train_data_all.csv')
#for (i in 1:45) {
 # for (j in 1:99) {
for (i in 1:45) {
  for (j in 1:99) {
    print(i)
    print(j)
    sales = train[(train$Store==i) & (train$Dept==j),4]
    sales_ts = ts(sales, frequency=52, start=c(2010,5))
    #sales_forecast_model = HoltWinters(sales_ts, l.start=train[(train$Store==i) & (train$Dept==j) & (train$Date=="2010-02-05"),4], b.start=train[(train$Store==i) & (train$Dept==j) & (train$Date=="2010-02-12"),4] - train[(train$Store==i) & (train$Dept==j) & (train$Date=="2010-02-05"),4])
    sales_forecast_model = HoltWinters(sales_ts)
    sales_forecast_predict = forecast.HoltWinters(sales_forecast_model, h=39)
    #plot.forecast(sales_forecast_predict)
    write.table(sales_forecast_predict, file='kanna.csv', sep=',', col.names=FALSE, append=TRUE)
  }
}