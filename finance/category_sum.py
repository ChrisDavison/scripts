#!/usr/bin/env python
import os
import pandas as pd

data = pd.read_csv(os.environ['FINANCEFILE'])

print(data.groupby('category').agg(lambda x: x['cost'].sum()).sort_values(by='cost', ascending=False))
