

setwd ("C:\\Users\\Lu Qin\\Dropbox\\AA_HARVARD APPLICATION\\S14A\\S14A2022-Final-Group-Beta")

dat = read.csv("UNdata_Export_20220704_182316113.csv")
colnames(dat) = c("country", "activity", "year","unit","quantity","note")
head(dat)
dat2 = dat[,c('country',"activity","year","quantity")]
dat2$activity = as.factor(dat2$activity)
dat2$country = as.factor(dat2$country)

dat3 = subset(dat2, (country == "Belgium" |
                    country == "Russian Federation" |
                    country == "Iceland" |
                    country == "United States" |
                    country == "New Zealand" |
                    country == "Japan" ) &
              (year >=  1995 & year <= 2019))

#Shared Activities among countries selected
#rownames(table(dat3$activity, dat3$year)[rowSums(table(dat3$activity, dat3$year)) == 25,])





#write.csv(dat2_sub_clean, "HeatDataforML.csv", row.names = FALSE)

        