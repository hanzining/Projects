
CloudFreq<- function(text_col, removedwords = c("hair", "dryer","can","however","dryers","like","one")){
  # pass in the text column that need to generate a word cloud and frequency plot
  library("wordcloud")
  corpus <- Corpus(VectorSource(text_col))
  corpus <- tm_map(corpus,removeWords,stopwords("english"))
  corpus=tm_map(corpus,removeWords,removedwords)
  
  
  # plot word cloud
  dtm <- TermDocumentMatrix(corpus)
  m <- as.matrix(dtm)
  v <- sort(rowSums(m),decreasing=TRUE)
  d <- data.frame(word = names(v),freq=v)
  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
            max.words=200, random.order=FALSE, rot.per=0.35, 
            colors=brewer.pal(8, "Dark2"))
  
  # plot freq barplot
  p<-ggplot(data=d[c(1:30),], aes(x=reorder(word, freq), y=freq)) +
    geom_bar(stat="identity")+coord_flip() + labs(title = "", y="mean helpful ratio", x = "star rating")
  p
}
