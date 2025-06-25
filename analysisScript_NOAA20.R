#####################
#Analysis of potential cloud changes from 2020 IMO regulations
#####################
rm(list = ls())
set.seed(103) #pseudo-random number generator
library("ncdf4")
library("fields")
library("viridis")
library("RColorBrewer")
library("leaps")
source("/Users/michaeldiamond/Code/ShipClosure/analysisFns.R")

#Set variogram covariance model
covModel <- "exp"

#Set region
regName = "Cx"

#Set months
months = c(9:10)

#Set colors
nColors <- 10

#Load data and region information
all <- nc_open("/Users/michaeldiamond/Documents/Data/VIIRS/NOAA20_shipkrige.nc")
lat <- rev(ncvar_get(all, "lat"))
lon <- ncvar_get(all, "lon")
load("/Users/michaeldiamond/Documents/Projects/ERB23_ShipTracks4MCB/ShipClosure/processed/regInfo.rda")

#
###Analysis scripts
#

#
###NOAA20: 2018
#
covars <- c("ERSST_2018")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2018"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 35, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2019
#
covars <- c("ERSST_2019")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2019"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 30, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2020
#
covars <- c("ERSST_2020")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2020"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 35, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2021
#
covars <- c("ERSST_2021")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2021"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 35, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2022
#
covars <- c("ERSST_2022")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2022"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 35, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2023
#
covars <- c("ERSST_2023")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2023"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 25, 
                months, lon, lat, nColors,savenc=TRUE)

#
###NOAA20: 2024
#
covars <- c("ERSST_2024")
tran = "none"
temp <- analyze(respName = sprintf("NOAA20_Nad_2024"), regName, covars,
                covModel, iniPhi = 1, iniSigma2 = 40, 
                months, lon, lat, nColors,savenc=TRUE)
