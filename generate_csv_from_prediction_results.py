#
# script generate a csv file from PredictionResult table of db
#
import pandas as pd
import traceback
import time

from utils import query_to_dict
from models import PredictionResult, get_session


def main():
    try:
        session = get_session()

        print "reading table PredictionResult from db..."
        # query all records from PredictionResult table
        result_set = session.query(PredictionResult).all()

        print "creating pandas dataframe..."
        # note: dataframe will not well be ordered (e.g. 'id' is not the first)
        df = pd.DataFrame(query_to_dict(result_set))
        print (df.columns.tolist())
        df = df[['date', 'model_number', 'available_qty', 'supply_for_days', 'runs_out_before_next_stock']]

        # start the first value of index column with 1
        df.index = df.index + 1

        print "generating results.csv..."
        df.to_csv("results.csv", index_label="#", sep=',', encoding='utf-8')
        

    except Exception as exp:
        print('dump_csv_to_db() :: got Exception: %s' % exp)
        print(traceback.format_exc())


if __name__ == '__main__':
    start_time = time.time()
    main()
    print
    print "-------------------------------------------------------"
    print " Total Time taken: %0.2f secs" % (time.time() - start_time)
    print "-------------------------------------------------------"
