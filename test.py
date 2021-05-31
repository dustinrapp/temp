
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

os.chdir("/mnt/c/Users/dusti/Desktop/temp")
work_dir = os.getcwd()

f = "/mnt/c/Users/dusti/Desktop/O3_010030010_annual.csv"
data = pd.read_csv(f, header=0, parse_dates = ['Starting Date'], index_col = 'Starting Date')

data.replace(-999,np.NaN, inplace = True)
data
print(data)
data['Rolling'] = data['Ozone (ppb)'].rolling(5).mean()

import matplotlib.dates as mdates

fig, ax1 = plt.subplots(figsize=(40,15))
 
#Extract out July ozone data
July_data = data['2011-07-01':'2011-07-31']  
July_data
ax1.scatter(July_data.index, July_data["Ozone (ppb)"])
ax1.plot(July_data.index, July_data["Rolling"])


#ax1.legend(loc='upper left', fontsize = 30)


ax1.set_ylabel('Ozone (ppb)', size = 30)


ax1.set_xlabel('Date', size=30)
ax1.tick_params(direction='out', length=6, width=2, grid_alpha=0.5, labelsize=30)

ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
#ax1.xaxis.set_major_locator(mdates.YearLocator())
fig.savefig(work_dir + '/test.png', bbox_inches='tight')
