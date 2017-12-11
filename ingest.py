import time
import threading
import traceback
from os import listdir
from os.path import isfile, join

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

    def process_csv_files(self, csv_files):
        try:
            for csv in csv_files:
                self._log("Processing csv: %s" % csv)

        except Exception as exp:
            print exp

    def run(self):
        while True:

            try:
                time.sleep(INGEST_SLEEP)

                self._log("Watching CSV files to be processed")
                csv_files = ["%s/%s" % (CSV_DIR, f) for f in listdir(CSV_DIR) if isfile(join(CSV_DIR, f))]
                self._log(csv_files)

            except Exception as exp:
                print exp


if __name__ == "__main__":
    ingest = Ingest()
    ingest.start()
