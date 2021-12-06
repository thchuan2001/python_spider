import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
csv=pd.read_csv("./BeijingPM20100101_20151231.csv")
csv['PM'] = csv[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].mean(axis=1)
year_avg=csv[['year', 'PM']].groupby('year')['PM'].mean()
year_avg.plot()
plt.savefig("./year_avg.png")
month_avg = csv[['year', 'month', 'PM', 'TEMP']].groupby(['year','month'])[['PM','TEMP']].mean()
month_avg.plot()
plt.savefig("./month_avg.png")
