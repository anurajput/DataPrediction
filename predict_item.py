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
import sys
import traceback

from models import Hekman, get_session
from utils import query_to_dict, days_left_for_next_produce, date_from_str, runs_out_before_next_stock


style.use('ggplot')


class PredictItem:

    def __init__(self, model_number, will_plot_data):
        self.model_number = model_number
        self.df = None
        self.clf = None
        self.will_plot_data = will_plot_data
        self.show_traceback = False

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
        dataframe['supply_for_days'].replace('0',       1, inplace=True)
        dataframe['supply_for_days'].replace('NaN',     1, inplace=True)
        return dataframe

    def populate_dataframe(self, forecast_col):
        """
        function read all records for model_number and
        fills the pandas dataframe
        """
        self._log("reading all record for this item from db")

        session = get_session()

        # query all records by model_number
        result_set = session.query(Hekman).filter(Hekman.model_number == self.model_number).order_by(Hekman.date).all()

        # convenience func to check a result_set
        #self.show_result_set(result_set)

        # note: dataframe will not well be ordered (e.g. 'id' is not the first)
        df = pd.DataFrame(query_to_dict(result_set))

        self.last_date = date_from_str(df.date.iloc[-1])

        # NORMALIZE DATA
        df = self.normalize_dataframe(df)

        ###############################
        #
        # Define data relations here
        #
        ###############################

        # relation-1
        # days left for next production of item
        df['DL_F_NP'] = df.apply(lambda row: days_left_for_next_produce(row['next_produce_date'], row['date'], row['supply_for_days']), axis=1)

        # runs out before next stock
        df['runs_out_before_next_stock'] = df.apply(lambda row: runs_out_before_next_stock(row['next_produce_date'], row['date'], row['supply_for_days']), axis=1)

        # we cant have 0 in DL_F_NP, or we will get divide by zero exception
        df['DL_F_NP'].replace(0, 1, inplace=True)

        # relation-2
        # consumption rate = qty/days
        df['CR'] = (df['available_qty']/ df['DL_F_NP']) * 100.0

        # relation-3
        # production rate = next_produce_qty/DL_F_NP
        df['PR'] = (df['next_produce_qty']/ df['DL_F_NP']) * 100.0

        # relation-4
        # availability rate = next_produce_qty/DL_F_NP
        df['AR'] = ( (df['available_qty'] + df['next_produce_qty'] ) / df['DL_F_NP']) * 100.0

        #self.show_dataframe(df)

        #df = df[['available_qty', 'DL_F_NP', 'CR', 'PR', 'AR']]  # available_qty
        #df = df[['supply_for_days', 'available_qty', 'DL_F_NP', 'CR', 'PR', 'AR', 'runs_out_before_next_stock']] # supply_for_days
        df = df[['DL_F_NP', 'CR', 'PR', 'AR', forecast_col]] # supply_for_days

        # we cant use NaN data, filling then with some default value
        df.dropna(inplace=True)

        self.df = df

        #print(self.df)

    def create_classifier(self, forecast_col):
        #self._log("defining classifier and training it")

        self.forecast_col = forecast_col

        forecast_out = int( math.ceil( 0.5 * len(self.df) ) )

        self.df['label'] = self.df[self.forecast_col].shift(-forecast_out)

        # Return new object with labels in requested axis removed
        X = np.array(self.df.drop(['label'], 1)) # axis=1

        np.nan_to_num(1.0)

        X = preprocessing.scale(X)
        X = X[:-forecast_out]
        self.X_lately = X[-forecast_out:]

        self.df.dropna(inplace=True)

        y = np.array(self.df['label'])


        ##########################################################
        #                                                        #
        #  TRAIN CLASSIFIER UNDER THRESHOLD ACCURACY IS OBTAINED #
        #                                                        #
        ##########################################################
        accuracy = -1.0
        ACCURACY_THRESHOLD = .7
        MIN_THRESHOLD = .20
        attempt = 1
        while accuracy < ACCURACY_THRESHOLD:
            #print "\n-- TRAINING CLASSIFIER WITH THRESHOLD : %f \n" % ACCURACY_THRESHOLD
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.9)

            clf = LinearRegression()
            #clf = svm.SVR()
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)
            self.clf = clf

            attempt += 1
            if attempt % 10 == 0 and ACCURACY_THRESHOLD > MIN_THRESHOLD:
                ACCURACY_THRESHOLD -= .05

            if attempt > 100:
                break

        print "\n------------------------------------------"
        print "))---> Accuracy:", accuracy
        print "------------------------------------------\n"

        #self._log("classifier created and trained")

        #FIXME - not sure if need to serialize this classifier,
        #in order to save time of training the classifier for each prediction of this item

    def predict_data(self, output_file_suffix):
        forecast_set = self.clf.predict(self.X_lately)

        self.df['Forecast'] = np.nan

        last_unix = time.mktime(self.last_date.timetuple())
        one_day = 86400
        next_unix = last_unix + one_day

        # FIXME: ensure that output dir exists 
        # else create it

        out_file = open("output/%s-%s.csv" % (self.model_number, output_file_suffix), "w")
        out_file.write("Date,%s\n" % self.forecast_col)

        # Item, Current Stock, Days Supply, Next In Stock, Run out before next stock

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            out_file.write( "%s,%s\n" % (next_date.date(), math.floor(i) ))
            
            next_unix+= one_day
            #self.df.loc[next_date] = [np.nan for _ in range(len(self.df.columns)-1)] + [i]
            self.df.loc[next_date.date()] = i
        out_file.close()

        #self.df[self.forecast_col].plot()
        self.df['Forecast'].plot()
        if self.will_plot_data:
            plt.legend(loc=4)
            plt.xlabel('Date')
            plt.ylabel('Availability (%s)' % self.model_number)
            plt.show()

    def forecast(self):
        predict_items = {"available_qty": "aq", "supply_for_days": "sfd", "runs_out_before_next_stock": "ro"}

        for k,v in predict_items.iteritems():

            self._log("%s :: predicting '%s" % (self.model_number, k))

            try:

                # step-1 : read all record for this item from db
                self.populate_dataframe(k)
                assert len(self.df), "forecast cant be made without some data in dataframe"

                # step-2: define classifier, train it
                self.create_classifier(k)
                assert self.clf, "forecast of %s cant be made without a classifier" % k
        
                # step-3
                # predict the data for given time range, days/months etc
                #self._log("predicting '%s' for given time range, days/months etc" % k)
                self.predict_data(v)

            except Exception as exp:
                self._log("prediction of col '%s' failed with exception: \n%s" % (k, exp) )
                print "----------------------------------------------------------------------------"
                if self.show_traceback:
                    traceback.print_exc()
                print "----------------------------------------------------------------------------"

        self.merge_csv()


        
        # step-4
        # visualize the data
        #self._log("visualizing the data")

    def merge_csv(self):
        try:
            f2 = pd.read_csv('output/%s-sfd.csv' % self.model_number, usecols=['Date','supply_for_days'])
            f1 = pd.read_csv('output/%s-aq.csv' % self.model_number, usecols=['Date', 'available_qty'])
            f3 = pd.read_csv('output/%s-ro.csv' % self.model_number, usecols=['Date', 'runs_out_before_next_stock'])

            # merging f1 and f2 on basis of 'Date' column
            f4 = pd.merge(left=f1, right=f2, how='left', on='Date')

            # merging f4 and f3 on basis of 'Date' column
            f5 = pd.merge(left=f4, right=f3, how='left', on='Date')

            # converting col. type to init
            f5.supply_for_days = f5.supply_for_days.astype(int)
            f5.available_qty = f5.available_qty.astype(int)
            f5.runs_out_before_next_stock = f5.runs_out_before_next_stock.astype(int)
            f5['runs_out_before_next_stock'].replace(1, 'Y', inplace=True)
            f5['runs_out_before_next_stock'].replace(-1, 'N', inplace=True)
            f5['runs_out_before_next_stock'].replace(0, 'N', inplace=True)

            # writing final output csv
            file_name = "output/%s-forecast.csv" % self.model_number
            f5.to_csv(file_name)
        except Exception as exp:
                self._log("merge csv for item '%s' failed with exception: \n%s" % (self.model_number, exp) )
                print "----------------------------------------------------------------------------"
                if self.show_traceback:
                    traceback.print_exc()
                print "----------------------------------------------------------------------------"
        
        
def main():
    if len(sys.argv) !=2:
        print "\nError: model_number not specified\nUsage:-\n"
        print "%s <model-number>\n" % sys.argv[0]
        return

    model_number = sys.argv[1]
    pi = PredictItem(model_number, False)
    pi.forecast()
        
if __name__ == "__main__":
    main()
