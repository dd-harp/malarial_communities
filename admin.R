library(raster)
library(sf)

# Using https://geocompr.robinlovelace.net/read-write.html
read.shapes <- function(data.dir) {
  list(
    africa=st_read(dsn = file.path(data.dir, "Africa.shp")),
    landscan=raster(file.path(data.dir, "LandScan Global 2017", "lspop2017"))
    )
}


data.dir <- "./data"
input.data <- read.shapes(data.dir)
africa = input.data$africa
