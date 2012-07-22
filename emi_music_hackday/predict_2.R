############ Prepare and Predict ############

############ 
#	Prepare #
############
# Prepare data by cleaning up various data and get it ready for prediction
# Training Linear Model based on just three parameters Artist, Track, User and Time of Rating
train = read.csv("train.csv")
clean_users = read.csv("clean_users.csv")
words = read.csv("words.csv")
test = read.csv("test.csv")

# Add id column to preserve the order of rows
train$id <- 1:nrow(train)
test$id <- 1:nrow(test)

# Create a Mean Function for replacing NA values
mean_function=function(x) {
	x[is.na(x)] = mean(x, na.rm=TRUE)
	x
}

# Join Training Set with User Demographics
# Replace NA values in each column with their respective mean
# Order the rows by id
train_users <- merge(train, clean_users, by.x="User", by.y="RESPID", all.x=T)
train_users <- data.frame(apply(train_users, 2, mean_function))
train_users <- train_users[order(train_users$id),]

# Join Test Set with User Demographics
# Replace NA values in each column with their respective mean
# Order the rows by id
test_users <- merge(test, clean_users, by.x="User", by.y="RESPID", all.x=T)
test_users <- data.frame(apply(test_users, 2, mean_function))
test_users <- test_users[order(test_users$id),]

############ 
#	Predict #
############

# Prediction based on the cleaned data
# Using Linear models for Regression

# Train the model based on cleaned Training data
train_model = lm(formula = Rating ~ Artist + Track + Time + GENDER + AGE + WORKING + REGION + MUSIC + LIST_OWN + LIST_BACK + Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 + Q11 + Q12 + Q13 + Q14 + Q15 + Q16 + Q17 + Q18 + Q19, train_users)

# Apply the model on test set and calculate the Ratings 
test_predict = predict(train_model,test_users[c("Artist","Track","Time","GENDER","AGE","WORKING","REGION","MUSIC","LIST_OWN","LIST_BACK","Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15","Q16","Q17","Q18","Q19")])

# Append the calculated output to fourth column as required by Kaggle
out <- test
out$Rating <- test_predict
new_out <- out[,c("Artist", "Track", "User", "Rating")]

# Write the Output to a CSV file for submission
write.csv(new_out, file = "predict_2.csv", row.names = F)