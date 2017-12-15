#
# script to predict when we will go out of stock on an item and for how long
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

style.use('ggplot')

def _log(msg):
    print "[PredictItem] :: %s" % msg


# item to be predicted
model_number = "29212"


# step - 1 
# read all record for this item from db
_log("reading all record for this item from db")



# step - 2
# create df/numpy array for historic dataset of this item
_log("creating df/numpy array for historic dataset of this item")


# step - 3
# define forecast column
_log("defining forecast column")

# step - 4
# define classifier, train it
_log("defining classifier, train it")


#FIXME - not sure if need to serialize this classifier,
#in order to save time of training the classifier for each prediction of this item


# step - 5
# predict the data for given time range, days/months etc
_log("predictingthe data for given time range, days/months etc")

# step - 6
# visualize the data
_log("visualizing the data")


