show_data<-function(measurement,number){
  
  result <- influx_select(con = con, 
                          db = "HZN_test", 
                          field_keys = "*", 
                          measurement = measurement,
                          group_by =  "*",
                          limit = number, 
                          order_desc = TRUE, 
                          return_xts = FALSE, 
                          simplifyList = TRUE)
  result
  
}