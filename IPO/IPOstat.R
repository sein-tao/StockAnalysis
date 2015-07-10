setwd("E:/home/StockAnalysis/IPO/")
library("fields")
data = read.table("IPO detail.txt")
data[1:5,]
data= data[,-dim(data)[2]]
colnames(data) = c("ID", "Name", "IPOID", "Amount", "Online", "ApplyLimit", 
                   "Price", "PE", "industryPE", "ApplyDate", "TotalApplyCapital", 
                   "QutationRate", "SucessRate", "CaptialPerHand", "SucessNo", "ListDate", 
                   "BenifitPerHand", "ZTNum", "details")
attach(data)
data[,"AmountPerHand"] = round(CaptialPerHand * SucessRate / Price) * 100
# RR, Return Rate
data[, "RRPerHand"] = BenifitPerHand / (Price * AmountPerHand) * 100
data[, "RRPerCapital"]= BenifitPerHand / (CaptialPerHand * 10000) * 100
attach(data)

hist(RRPerCapital)
dim(data)
quantile(RRPerCapital, 0.95)
data.sub = subset(data, RRPerCapital<6)
data.raw = data
data = data.sub
attach(data)

colnames(data)
numCol = c(4,7:9, 12:14, 17, 18, 20:22)
sCol=c("Amount", "Price", "AmountPerHand", 
       "PE", "industryPE", "QutationRate", "SucessRate", 
       "CaptialPerHand", "RRPerCapital" )
numCol= sCol
co = cor(data[, numCol])
image.plot(1:ncol(co), 1:nrow(co), co, col=topo.colors(8))
      #col=c("green", "grey", "red"), breaks=c(-1, -0.3, 0.3, 1))

co.rc = co["RRPerCapital",]
co.rc[order(abs(co.rc), decreasing=T)]
