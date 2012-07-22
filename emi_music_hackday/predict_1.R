# First stab
# Training Linear Model based on just three parameters Artist, Track, User and Time of Rating
train = read.csv("train.csv", na.strings="NaN")
users = read.csv("clean_users.csv", na.strings="NaN")
words = read.csv("words.csv", na.strings="NaN")
test = read.csv("test.csv", na.strings="NaN")

train_predict = lm(formula = Rating ~ Artist + Track + User + Time, train)
submission_predict = predict(train_predict,test[c("Artist", "Track", "User", "Time")])