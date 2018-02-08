import pandas as pd
f2 = pd.read_csv('560140094-sfd.csv', usecols=['Date','supply_for_days'])
f1 = pd.read_csv('560140094-aq.csv', usecols=['Date', 'available_qty'])
f3 = pd.read_csv('560140094-ro.csv', usecols=['Date', 'runs_out_before_next_stock'])

# merging f1 and f2 on basis of 'Date' column
f4 = pd.merge(left=f1, right=f2, how='left', on='Date')

# merging f4 and f3 on basis of 'Date' column
f5 = pd.merge(left=f4, right=f3, how='left', on='Date')

# converting col. type to init
f5.runs_out_before_next_stock = f5.runs_out_before_next_stock.astype(int)

print (f5)

# writing final output csv
file_name = "560140094-forecast.csv"
#f5.to_csv(file_name, sep='\t')
f5.to_csv(file_name)

# To use a specific encoding (e.g. 'utf-8') use the encoding argument
# f5.to_csv(file_name, sep='\t', encoding='utf-8')
