KWScore <- function(text_col = hair_dryer_ratio$review_body, keywords =  c("cord", "cold", "quickly","settings","price")) {
  text_length = length(text_col)
  scores <- rep(0, text_length)
  for (i in 1:text_length){
    word_counter <- rep(0, length(keywords))
    # count words
    for (j in 1:length(keywords) ){
      # num of a keyword occurence in the text
      word_counter[j] = sum(str_count(text_col[i], keywords[j]))
    }
    scores[i] = sum(word_counter)
  }
  return (scores)
}
