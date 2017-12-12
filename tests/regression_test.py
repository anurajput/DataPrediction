import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

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
df.dropna(inplace=True)

print df.head()
print df.tail()

X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])
X = preprocessing.scale(X)
y = np.array(df['label'])

print "X Len:", len(X)
print "y Len:", len(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#clf = LinearRegression()
#clf = svm.SVR()
#clf = svm.SVR(kernel='poly') # defualt kernel is linear
clf = LinearRegression(n_jobs=10)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print "accuracy:", accuracy
