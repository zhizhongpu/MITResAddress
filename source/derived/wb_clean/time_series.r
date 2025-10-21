library(data.table)

rawDir <- "datastore/raw/world_bank/orig"
outDir <- "output/derived/wb_clean"

prepare_data <- function(gdpPath, educPath) {
  gdpDf <- fread(gdpPath, skip = 2, header = TRUE)
  educDf <- fread(educPath, skip = 2, header = TRUE)

  yearCols <- names(gdpDf)[5:ncol(gdpDf)]

  gdpLong <- melt(
    gdpDf[, c("Country Name", ..yearCols), with = FALSE],
    id.vars = "Country Name",
    variable.name = "Year",
    value.name = "GDP",
    na.rm = TRUE
  )

  educLong <- melt(
    educDf[, c("Country Name", ..yearCols), with = FALSE],
    id.vars = "Country Name",
    variable.name = "Year",
    value.name = "Education_Exp",
    na.rm = TRUE
  )

  mergedDf <- merge(
    gdpLong,
    educLong,
    by = c("Country Name", "Year"),
    all = FALSE
  )

  return(mergedDf)
}

gdpPath <- file.path(rawDir, "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_1740213.csv")
educPath <- file.path(rawDir, "API_SE.XPD.TOTL.GD.ZS_DS2_en_csv_v2_1740282.csv")

mergedDf <- prepare_data(gdpPath, educPath)

yearAgg <- mergedDf[, .(
  Mean_GDP = mean(GDP, na.rm = TRUE),
  Mean_Education_Exp = mean(Education_Exp, na.rm = TRUE)
), by = Year]

fwrite(yearAgg, file.path(outDir, "gdp_education_by_year.csv"))
