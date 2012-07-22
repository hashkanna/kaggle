
test  <- read.csv("test.csv")
train  <- read.csv("train.csv")

uniformPredictions  <- rep(mean(train$Rating), nrow(test))

library(plyr)
userMeans  <- ddply(train, "User", function(df) mean(df$Rating))
test$id  <- 1:nrow(test)
testWithUserMeans  <- merge(test, userMeans, all.x = T)
testWithUserMeans = testWithUserMeans[order(testWithUserMeans$id),]
testWithUserMeans[is.na(testWithUserMeans$V1),]  <- uniformPredictions[1]
summary(testWithUserMeans)

artistMeans  <- ddply(train, "Artist", function(df) mean(df$Rating))
testWithArtistMeans  <- merge(test, artistMeans, all.x = T)
testWithArtistMeans = testWithArtistMeans[order(testWithArtistMeans$id),]
testWithArtistMeans[is.na(testWithArtistMeans$V1),]  <- uniformPredictions[1]
summary(testWithUserMeans)


write.csv(testWithUserMeans$V1, file = "userMeans.csv", row.names = F)
write.csv(testWithArtistMeans$V1, file = "ArtistMeans.csv", row.names = F)
write.csv(uniformPredictions, file = "uniform.csv", row.names = F)
