import pandas as pd
import quandl


class InventoryRegressonTest:

    csv = "inventory.csv"
    def __init__(self):

        df = pd.read_csv(self.csv, header=None) 
        print df

"""
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
"""

if __name__ == "__main__":
    irt = InventoryRegressonTest()
