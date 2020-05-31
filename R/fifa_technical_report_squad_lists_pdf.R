library(pdftools)
library(stringr)

# Location of WARN notice pdf file
location <- "https://resources.fifa.com/image/upload/fu20wwc2018-tsg-report.pdf?cloudid=khspkuf4mopr1nd2i1xr"

txt <- pdf_text(location)

output <- NULL

for (pg in 1:length(txt)) {
  table <- txt[[pg]]
  table <- str_split(table, "\n", simplify = TRUE)
  table_start <- intersect(str_which(table, "NUM"), str_which(table, "NAME"))
  nation <- str_trim(str_split(table[, 3], "/", simplify = TRUE)[1], side="both")

  if (length(table_start) > 0) {
    table_end <- intersect(str_which(table, "NUM"), str_which(table, "="))
    table <- table[1, (table_start +1 ):(table_end - 1)]
    table <- str_trim(table, side = "both")
    table <- str_split(table, "  ", simplify = TRUE)
    table_df <- as.data.frame(table, stringsAsFactors = FALSE)
    
    remove_blanks <- function(row) {
      out <- NULL
      for (i in row){ if (str_trim(i, side="both") != ""){ out <- c(out, i) }}
      return(out)
    }
    
    table_df <- lapply(split(table_df,1:nrow(table_df)),function(row) remove_blanks(row))
    table_df <- do.call(rbind, Filter(function(x) length(x)>=6, table_df))
    table_df <- as.data.frame(table_df, stringsAsFactors = FALSE)
    table_df <- table_df[, 1:6]
    table_df[, 7] <- nation 
    names(table_df) <- c("NUM", "NAME", "CLUB (COUNTRY)", "MINS", "G", "A", "Nation")
    output <- rbind(output, table_df)
  }
}

