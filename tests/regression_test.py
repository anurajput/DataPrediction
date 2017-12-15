import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import time

style.use('ggplot')


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

forecast_col = 'Adj. Close'

# in machine learning, you cant use NaN data,
# so, fill it will some default value
df.fillna(-99999, inplace=True)

forecast_out = int( math.ceil( 0.1 * len(df) ) )

df['label'] = df[forecast_col].shift(-forecast_out)

print df.head()
print df.tail()

# Return new object with labels in requested axis removed
X = np.array(df.drop(['label'], 1)) # axis=1

X = preprocessing.scale(X)
X = X[:-forecast_out]
X_lately = X[-forecast_out:]

df.dropna(inplace=True)

y = np.array(df['label'])

"""
Split arrays or matrices into random train and test subsets

test_size : float, int, or None (default is None)
    If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split. 
    If int, represents the absolute number of test samples. 
    If None, the value is automatically set to the complement of the train size. 
    If train size is also None, test size is set to 0.25.
"""
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#clf = LinearRegression()
#clf = svm.SVR()
#clf = svm.SVR(kernel='poly') # defualt kernel is linear
#clf = LinearRegression(n_jobs=10)
clf = LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print "accuracy:", accuracy


###############################
#                             #
# lets do some prediction now #
#                             #
###############################
forecast_set = clf.predict(X_lately)

print "forecast_set", forecast_set

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = time.mktime(last_date.timetuple())
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix+= one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
