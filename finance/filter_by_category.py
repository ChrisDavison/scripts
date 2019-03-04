#!/usr/bin/env python
import os
import sys
import pandas as pd

if '-h' in sys.argv[1:]:
    print("""usage: filter_by_category.py CATEGORY""")
    sys.exit(0)

category = " ".join(sys.argv[1:])

data = pd.read_csv(os.environ['FINANCEFILE']).sort_values(by='date')
data['year'] = data['date'].apply(lambda x: str(x)[:4])
data = data[data.category == category]

print(data[['date', 'cost', 'description']])

print("\nYEARLY")
print(data.groupby('year')['cost'].agg(['sum', 'count']))

