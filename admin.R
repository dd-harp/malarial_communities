# Using https://geocompr.robinlovelace.net/read-write.html
read.shapes <- function(data.dir) {
  list(africa=st_read(dsn = c(data.dir, "Africa.shp")))
}


data.dir <- "./data"
africa <- read.shapes(data.dir)$africa
