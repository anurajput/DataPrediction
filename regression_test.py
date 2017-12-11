import pandas as pd
import quandl

df = quandl.get('WIKI/GOOGL')

df = df[[
    'Adj. Open',
    'Adj. High',
    'Adj. Low',
    'Adj. Close',
    'Adj. Volume',
        ]]

df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low'])/ df['Adj. Low'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open'])/ df['Adj. Open'] * 100.0

df = df[[
    'Adj. Close',
    'PCT_change',
    'HL_PCT',
    'Adj. Volume',
        ]]

#print df
print df.head()
