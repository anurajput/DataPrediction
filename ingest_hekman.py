import time
import threading
import traceback
from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil
from utils import smart_int
from models import Hekman, get_session
from config import HECKMAN_CSV_DIR, HECKMAN_PROCESSED_CSV_DIR, INGEST_SLEEP


class IngestHekman(threading.Thread):
    """
    Features of class:-
    * monitoring unprocessed csv files in CSV_DIR
    * process them, save their data in PostGRESql db
    * move the processed csv file to PROCESSED_CSV_DIR
    """

    def __init__(self):
        super(IngestHekman, self).__init__()
        self._log("initialised")

    def _log(self, msg):
        print "[IngestHekman] :: %s" % msg

    def process_csv_file(self, csv):
        try:
            # _log("Processing csv: %s" % csv)
            df = pd.read_csv(csv, header=None, skiprows=[0])
            # print df

            session = get_session()
            for index, row in df.iterrows():
                print index, row[0]

                hekman = Hekman(row[0], row[1], row[2], smart_int(row[3]),
                                smart_int(row[4]), row[5], smart_int(row[6]),
                                row[7], smart_int(row[8]), smart_int(row[9]))
                self._log(hekman)
                session.add(hekman)
                session.commit()
                session.flush()
            session.close()

            dest = HECKMAN_PROCESSED_CSV_DIR
            self._log("Moving %s -> %s" % (csv, HECKMAN_PROCESSED_CSV_DIR))
            shutil.move(csv, HECKMAN_PROCESSED_CSV_DIR)
        except Exception as exp:
            self._log('process_csv_file() :: Got Exception: %s' % exp)
            self._log(traceback.format_exc())

    def run(self):
        while True:

            try:
                time.sleep(INGEST_SLEEP)

                self._log("Watching CSV files to be processed")
                csv_files = ["%s/%s" % (HECKMAN_CSV_DIR, f)
                             for f in listdir(HECKMAN_CSV_DIR)
                             if isfile(join(HECKMAN_CSV_DIR, f))]
                self._log("CSV Found: %s" % csv_files)

                for csv in csv_files:
                    self.process_csv_file(csv)

            except Exception as exp:
                self._log('run() :: Got exception: %s' % exp)
                self._log(traceback.format_exc())


if __name__ == "__main__":
    ingest_hekman = IngestHekman()
    ingest_hekman.start()
