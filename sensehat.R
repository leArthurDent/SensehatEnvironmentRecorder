#Copyright (C) 2017  Sascha Manier (SaschaManier@posteo.de)
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation version 3 of the License.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program. If not, see http://www.gnu.org/licenses/.

library("ggplot2")
setwd("/home/pi/Sensehat")
t<-Sys.time()
t2<-t-86400
fname<-strftime(t2, "%Y%m%d")
table<-read.csv(file=paste0("data/",fname,".csv"), header=T)
time<-table[,1]
temp<-table[,2]
press<-table[,3]
humid<-table[,4]
data<-as.data.frame(time)
data$temp<-temp
data$press<-press
data$humid<-humid
p.temp<-ggplot(data, aes(time, temp)) +
	geom_line(colour="red") +
	ggtitle("Temperatur") +
	xlab("Zeit, min") +
	ylab("Temperatur, °C") +
	theme_bw()
p.humid<-ggplot(data, aes(time, humid)) +
	geom_line(colour="blue") +
	ggtitle("Luftfeuchtigkeit") +
	xlab("Zeit, min") +
	ylab("rel. Luftfeuchtigkeit, %") +
	ylim(0,100) +
	geom_hline(yintercept=40) +
	geom_hline(yintercept=60) +
	theme_bw()
p.press<-ggplot(data, aes(time, press)) +
	geom_line(colour="green") +
	ggtitle("Luftdruck") +
	xlab("Zeit, min") +
	ylab("Luftdruck, pa") +
	theme_bw()
pdf(paste0("graphs/",fname,".pdf"), paper="a4")
p.temp
p.humid
p.press
dev.off()