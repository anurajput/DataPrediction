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
from utils import query_to_dict, days_left_for_next_produce


style.use('ggplot')


class PredictItem:

    def __init__(self, model_number):
        self.model_number = model_number
        self.df = None
        self.clf = None

    def _log(self, msg):
        print "[PredictItem] :: %s" % msg

    def show_result_set(self, result_set):
        """
        convenience fn to see contents of result_set
        """
        for query in result_set:

            self._log('date: %s' % query.date)
            self._log('model_number: %s' % query.model_number)
            self._log('description: %s' % query.description)
            self._log('supply_for_days: %s' % query.supply_for_days)
            self._log('available_qty: %s' % query.available_qty)
            self._log('next_produce_qty: %s' % query.next_produce_qty)
            self._log('next_produce_date: %s' % query.next_produce_date)
            self._log('next_schedule_produce_qty: %s' % query.next_schedule_produce_qty)
            self._log('next_schedule_produce_date: %s' % query.next_schedule_produce_date)

    def show_dataframe(self, dataframe):
        for index, row in dataframe.iterrows():
            print "%d -> %s" % (index, row)

    def normalize_dataframe(self, dataframe):
        dataframe['supply_for_days'].replace('S-0/15',  7, inplace=True)
        dataframe['supply_for_days'].replace('S-15/30', 20, inplace=True)
        dataframe['supply_for_days'].replace('S-30/60', 45, inplace=True)
        dataframe['supply_for_days'].replace('S-60+',   65, inplace=True)
        dataframe['supply_for_days'].replace('0',       0, inplace=True)
        return dataframe

    def populate_dataframe(self):
        """
        function read all records for model_number and
        fills the pandas dataframe
        """
        self._log("reading all record for this item from db")

        session = get_session()

        # query all records by model_number
        result_set = session.query(Hekman).filter(Hekman.model_number == self.model_number).order_by(Hekman.date).all()
        self.show_result_set(result_set)

        # note: dataframe will not well be ordered (e.g. 'id' is not the first)
        df = pd.DataFrame(query_to_dict(result_set))

        # NORMALIZE DATA
        df = self.normalize_dataframe(df)

        ###############################
        #
        # Define data relations here
        #
        ###############################

        # relation-1
        # days left for next production of item
        # next_produce_date - date

        df['DL_F_NP'] = df.apply(lambda row: days_left_for_next_produce(row['next_produce_date'], row['date'], row['supply_for_days']), axis=1)

        # consumption rate = qty/days
        df['CR'] = (df['available_qty'])/ df['supply_for_days'] * 100.0

        self.show_dataframe(df)

        #df = df[['date', 'next_produce_date', 'next_produce_qty', 'available_qty', 'next_schedule_produce_qty']]
        df = df[['supply_for_days', 'next_produce_qty', 'available_qty', 'DL_F_NP', 'CR']]

        # Available <=> Next Produce Relation
        #df['A_NP_PCT'] = (df['next_produce_qty'] - df['available_qty'])/ df['next_produce_qty'] * 100.0
        #df['A_NP_PCT'] = (df['next_produce_qty'] - df['available_qty'])/ df['available_qty'] * 100.0

        # we cant use NaN data, filling then with some default value
        #df.fillna(-99999, inplace=True)
        df.dropna(inplace=True)

        self.df = df

        print(self.df)

    def create_classifier(self):
        self._log("defining classifier and training it")

        #forecast_col = 'available_qty'
        forecast_col = 'supply_for_days'
        forecast_out = int( math.ceil( 0.1 * len(self.df) ) )

        self.df['label'] = self.df[forecast_col].shift(-forecast_out)

        # Return new object with labels in requested axis removed
        X = np.array(self.df.drop(['label'], 1)) # axis=1

        X = preprocessing.scale(X)
        X = X[:-forecast_out]
        self.X_lately = X[-forecast_out:]

        self.df.dropna(inplace=True)

        y = np.array(self.df['label'])

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.9)

        #clf = LinearRegression()
        clf = svm.SVR()
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)

        print "\n------------------------------------------"
        print "))---> Accuracy:", accuracy
        print "------------------------------------------\n"

        self.clf = clf
        self._log("classifier created and trained")

        #FIXME - not sure if need to serialize this classifier,
        #in order to save time of training the classifier for each prediction of this item

    def predict_data(self):
        forecast_set = self.clf.predict(self.X_lately)

        print "forecast_set", forecast_set

        self.df['Forecast'] = np.nan

        last_date = self.df.iloc[-1].name
        self._log("last_date: %s" % last_date)

        last_unix = time.mktime(last_date.timetuple())
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix+= one_day
            self.df.loc[next_date] = [np.nan for _ in range(len(self.df.columns)-1)] + [i]

        self.df['supply_for_days'].plot()
        self.df['Forecast'].plot()
        plt.legend(loc=4)
        plt.xlabel('Date')
        plt.ylabel('Availability')
        plt.show()

    def forecast(self):

        # step-1 : read all record for this item from db
        self.populate_dataframe()
        assert len(self.df), "Forecast cant be made without some data in dataframe"

        # step-2: define classifier, train it
        self.create_classifier()
        assert self.clf, "Forecast cant be made without a classifier"
        
        # step-3
        # predict the data for given time range, days/months etc
        self._log("predicting the data for given time range, days/months etc")
        self.predict_data()
        
        # step-4
        # visualize the data
        #self._log("visualizing the data")
        
        
        
if __name__ == "__main__":
    # item to be predicted
    model_number = "11100"
    pi = PredictItem(model_number)
    pi.forecast()
