import time
import threading
import traceback
from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil

from models import Inventory, get_session
from config import CSV_DIR, PROCESSED_CSV_DIR, INGEST_SLEEP


class Ingest(threading.Thread):
    """
    Features of class:-
    * monitoring unprocessed csv files in CSV_DIR
    * process them, save their data in PostGRESql db
    * move the processed csv file to PROCESSED_CSV_DIR
    """

    def __init__(self):
        super(Ingest, self).__init__()
        self._log("initialised")

    def _log(self, msg):
        print "[Ingest] :: %s" % msg

    def process_csv_file(self, csv):
        try:
            self._log("Processing csv: %s" % csv)
            df = pd.read_csv(csv, header=None) 
            #print df

            session = get_session()
            for index, row in df.iterrows():
                print index, row[0]

                inv = Inventory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                print "Inventory = %s" % inv
                session.add(inv)
                session.commit()
                session.flush()
            session.close()

            dest = PROCESSED_CSV_DIR
            print "Moving %s -> %s" % (csv, PROCESSED_CSV_DIR)
            shutil.move(csv, PROCESSED_CSV_DIR)
        except Exception as exp:
            print exp

    def run(self):
        while True:

            try:
                time.sleep(INGEST_SLEEP)

                self._log("Watching CSV files to be processed")
                csv_files = ["%s/%s" % (CSV_DIR, f) for f in listdir(CSV_DIR) if isfile(join(CSV_DIR, f))]
                self._log(csv_files)

                for csv in csv_files:
                    self.process_csv_file(csv)

            except Exception as exp:
                print exp


if __name__ == "__main__":
    ingest = Ingest()
    ingest.start()
