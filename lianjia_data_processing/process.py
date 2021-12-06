import pandas as pd
import numpy as np
csv=pd.read_csv("./result.csv")
print(type(csv))
total_price_max_id = csv.loc['tot_price']
print(total_price_max_id)
