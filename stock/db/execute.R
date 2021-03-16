library(dplyr)
library(influxdbr)
library(quantmod)
library(xts)


#path="~/Desktop/MacroR/test-1"


source("~/Desktop/MacroR/test-1/db_interaction/get_connection.R")
source("~/Desktop/MacroR/test-1/db_interaction/write_data.R")
source("~/Desktop/MacroR/test-1/db_interaction/show_data.R")






con<-get_connection("macroview.team")
create_database(con,"HZN_test")

getSymbols("FEDFUNDS",src="FRED")
write_data("FEDFUNDS","FEDFUNDS_data")

getSymbols("DFEDTARU",src="FRED")
write_data("DFEDTARU","DFEDTARU_data")

getSymbols("DFEDTARL",src="FRED")
write_data("DFEDTARL","DFEDTARL_data")

show_data("FEDFUNDS_data",15)
show_data("DFEDTARU_data",15)
show_data("DFEDTARL_data",15)

