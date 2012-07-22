############ Prepare and Predict ############

############ 
	Prepare
############
# Prepare data by cleaning up various data and get it ready for prediction
# Training Linear Model based on just three parameters Artist, Track, User and Time of Rating
train = read.csv("train.csv")
clean_users = read.csv("clean_users.csv")
words = read.csv("words.csv")
test = read.csv("test.csv")

# Create a Mean Function for replacing NA values
mean_function=function(x) {
	x[is.na(x)] = mean(x, na.rm=TRUE)
	x
}

# Join Training Set with User Demographics
# Replace NA values in each column with their respective mean
train_users <- merge(train, clean_users, by.x="User", by.y="RESPID", all.x=T)
train_users <- data.frame(apply(train_users, 2, mean_function))

# Join Test Set with User Demographics
# Replace NA values in each column with their respective mean
test_users <- merge(test, clean_users, by.x="User", by.y="RESPID", all.x=T)
test_users <- data.frame(apply(test_users, 2, mean_function))

############ 
	Predict
############

# Prediction based on the cleaned data
# Using Linear models for Regression

# Train the model based on cleaned Training data
train_model = lm(formula = Rating ~ User + Artist + Track + Time + GENDER + AGE + WORKING + REGION + MUSIC + LIST_OWN + LIST_BACK + Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 + Q11 + Q12 + Q13 + Q14 + Q15 + Q16 + Q17 + Q18 + Q19, train_users)

# Apply the model on test set and calculate the Ratings 
test_predict = predict(train_model,test_users[c("User","Artist","Track","Time","GENDER","AGE","WORKING","REGION","MUSIC","LIST_OWN","LIST_BACK","Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15","Q16","Q17","Q18","Q19")])

# Write the Output to a CSV file for submission
write.csv(test_predict, file = "predict1.csv", row.names = F)