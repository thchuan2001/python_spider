import pandas as pd
import numpy as np
csv=pd.read_csv("./result.csv")
print(csv)

print("总价最高的房子信息：")
total_price_max_id = csv.loc[:,"total_price"].idxmax()
print(csv.loc[total_price_max_id])


print("总价最低的房子信息：")
total_price_max_id = csv.loc[:,"total_price"].idxmin()
print(csv.loc[total_price_max_id])

print("总价中位数：")
print(csv.loc[:,"total_price"].median())

print("单价（均价）最高的房子信息：")
total_price_max_id = csv.loc[:,"avg_price"].idxmax()
print(csv.loc[total_price_max_id])

print("单价（均价）最低的房子信息：")
total_price_max_id = csv.loc[:,"avg_price"].idxmin()
print(csv.loc[total_price_max_id])


print("单价中位数：")
print(csv.loc[:,"avg_price"].median())
