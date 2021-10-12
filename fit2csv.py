#!/usr/bin/env python3
import fitdecode
import pandas as pd
import sys

fields = ["timestamp", "power", "heart_rate", "cadence", "speed"]

file = sys.argv[1]

file = "6179724360.fit"

rows = [[r.get_value(f) for f in fields] 
        for r in fitdecode.FitReader(file)
        if isinstance(r, fitdecode.records.FitDataMessage)
            and r.has_field("power")]

df = pd.DataFrame(rows, columns=fields)
print(df.head())
