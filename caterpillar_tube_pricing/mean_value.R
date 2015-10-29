setwd("/Users/kanna/Sandbox/kaggle/caterpillar_tube_pricing/competition_data/")
# Read the csv file
train = read.csv("train_set.csv")
mean(train$cost)
test = read.csv("test_set.csv")

output = read.csv("../sample_submission.csv")
output$cost = output$cost + mean(train$cost)

write.csv(output, file = "../output1_avg.csv", row.names = FALSE, quote = FALSE)