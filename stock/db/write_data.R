write_data<-function(tag,name){
  data <- dplyr::bind_cols(time = as.POSIXct(index(get(tag))),data.frame(get(tag)))
  
  influx_write(con = con, 
               db = "HZN_test",
               x = data,
               time_col = "time",
               measurement = name)
  
}