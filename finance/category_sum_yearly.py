#!/usr/bin/env python
import os
import pandas as pd

data = pd.read_csv(os.environ['FINANCEFILE'])
data['year'] = data['date'].apply(lambda x: str(x)[:4])

print("BY CATEGORY")
print(data.groupby(['year', 'category']).agg('sum'))

print("\nYEARLY") 
print(data.groupby(['year']).agg(['sum', 'count'])['cost'].reset_index())
