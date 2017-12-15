#
# script to predict when we will go out of stock on an item and
# for how long
#

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

from models import Hekman, get_session
from utils import query_to_dict


style.use('ggplot')


class PredictItem:

    def __init__(self, model_number):
        self.model_number = model_number
        self.df = None

    def _log(self, msg):
        print "[PredictItem] :: %s" % msg

    def populate_dataframe(self):
        """
        function read all records for model_number and
        fills the pandas dataframe
        """
        self._log("reading all record for this item from db")

        session = get_session()

        # query all records by model_number
        result_set = session.query(Hekman).all()

        # NOTE: dataframe will not well be ordered (e.g. 'id' is not the first)
        df = pd.DataFrame(query_to_dict(result_set))
        df = df[[ 'available_qty', 'next_produce_qty', 'next_schedule_produce_qty', 'retail', 'pricing', ]]

        # we cant use NaN data, filling then with some default value
        df.fillna(-99999, inplace=True)

        self.df = df

        print(self.df)

    def create_classifier(self):
        forecast_col = 'available_qty'
        forecast_out = int( math.ceil( 0.1 * len(self.df) ) )

        self.df['label'] = self.df[forecast_col].shift(-forecast_out)

        # Return new object with labels in requested axis removed
        X = np.array(self.df.drop(['label'], 1)) # axis=1

        X = preprocessing.scale(X)
        X = X[:-forecast_out]
        X_lately = X[-forecast_out:]

        self.df.dropna(inplace=True)

        y = np.array(self.df['label'])

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

        #clf = LinearRegression()
        clf = svm.SVR()
        #clf = svm.SVR(kernel='poly') # defualt kernel is linear
        #clf = LinearRegression(n_jobs=10)
        #clf = LinearRegression()
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)

        print "accuracy:", accuracy

    def forecast(self):

        # step-1 : read all record for this item from db
        self.populate_dataframe()
        assert len(self.df), "Forecast cant be made without some data in dataframe"

        # step-2: # define classifier, train it
        self._log("defining classifier and training it")
        self.create_classifier()
        
        
        #FIXME - not sure if need to serialize this classifier,
        #in order to save time of training the classifier for each prediction of this item
        
        
        # step - 5
        # predict the data for given time range, days/months etc
        self._log("predictingthe data for given time range, days/months etc")
        
        # step - 6
        # visualize the data
        self._log("visualizing the data")
        
        
        
if __name__ == "__main__":
    # item to be predicted
    model_number = "29212"
    pi = PredictItem(model_number)
    pi.forecast()
