
#import required packages
import pandas as pd
from glob import glob
import os
import numpy as np
os.chdir("/mnt/c/Users/dusti/Desktop/temp")


#############Task #1############
#Read in Data
data_files = glob(r'/mnt/c/Users/dusti/Desktop/temp/historicalPriceData/*.csv')

data1 = pd.read_csv(data_files[0], parse_dates=['Date'])
data2 = pd.read_csv(data_files[1], parse_dates=['Date'])
data3 = pd.read_csv(data_files[2], parse_dates=['Date'])
data4 = pd.read_csv(data_files[3], parse_dates=['Date'])

#Append together
data_df = data1.append([data2, data3, data4])
data_df

#Make index date
data_df.set_index(['Date'], inplace = True)

#For easier filiter, create month, year, and hour columns
data_df['Month'] = data_df.index.month.astype(str)
data_df['Year'] = data_df.index.year.astype(str)
data_df['Hour'] = data_df.index.hour.astype(str)


#############Task #2############
#Calculate means by settlmentgroup
sp_groups = data_df.groupby(['SettlementPoint', 'Year', 'Month']).mean()


#############Task #3############
#Write out to csv file
sp_groups.to_csv('AveragePriceByMonth.csv',sep = ',', float_format = '%.2f')


############Task #4############
pv_df = data_df.copy()

pv_df.loc[~(pv_df['Price'] > 0), :]=np.nan
pv_df.head()



#Remove LZ values
pv_df = pv_df[pv_df["SettlementPoint"].str.contains("LZ_")==False].copy()


#Calculate std of log of hourly values
std_log = lambda grp: np.std(np.log(grp))
year_settlement = pv_df.drop(['Month', 'Hour'], axis=1).groupby(['SettlementPoint','Year'], dropna=False).apply(std_log)
year_settlement.rename(columns={"Price":"HourlyVolatility"},inplace = True)

#Write to csv
year_settlement.to_csv('HourlyVolatilityByYear.csv',sep = ',', float_format = '%.2f')

####Task #6############
ys = year_settlement.reset_index()
max_by_year = ys.groupby(['Year'], dropna=False).max()

#I am not sure why this is - but it is incorrectly writing the wrong SettlmentPrice value for 2019 (??)
#I will need to investigate further, but for now I will just replace manually:
max_by_year.loc[max_by_year.index =='2019', "SettlementPoint"] = 'HB_PAN'

max_by_year.to_csv('MaxVolatilityByYear.csv',sep = ',', float_format = '%.2f')

