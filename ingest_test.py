import time
import threading
import traceback
from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil
from utils import smart_int, smart_str
from models import Hekman, get_session
from config import CSV_DIR, PROCESSED_CSV_DIR, INGEST_SLEEP


def process_csv_file(csv):
    try:
        # _log("Processing csv: %s" % csv)
        df = pd.read_csv(csv, header=None)
        #print df

        session = get_session()
        for index, row in df.iterrows():
            print index, row[0]

            hekman = Hekman(row[0], row[1], row[2], smart_int(row[3]), smart_int(row[4]), row[5], smart_int(row[6]), row[7], smart_int(row[8]), smart_int(row[9]))
            print "Hekman = %s" % hekman
            session.add(hekman)
            session.commit()
            session.flush()
        session.close()

        dest = PROCESSED_CSV_DIR
        print "Moving %s -> %s" % (csv, PROCESSED_CSV_DIR)
        shutil.move(csv, PROCESSED_CSV_DIR)
    except Exception as exp:
        print 'Got Exception: %s' % exp
        print traceback.format_exc()


if __name__ == "__main__":
    process_csv_file('retailstockhekmanstock20170319.CSV')
