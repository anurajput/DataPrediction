import time
import threading
import traceback
from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil
from utils import smart_int
from models import HowardMiller, get_session
from config import HOWARD_MILLER_CSV_DIR, \
    HOWARD_MILLER_PROCESSED_CSV_DIR, INGEST_SLEEP


class IngestHowardMiller(threading.Thread):
    """
    Features of class:-
    * monitoring unprocessed csv files in CSV_DIR
    * process them, save their data in PostGRESql db
    * move the processed csv file to PROCESSED_CSV_DIR
    """

    def __init__(self):
        super(IngestHowardMiller, self).__init__()
        self._log("initialised")

    def _log(self, msg):
        print "[IngestHowardMiller] :: %s" % msg

    def process_csv_file(self, csv):
        try:
            # _log("Processing csv: %s" % csv)
            df = pd.read_csv(csv, header=None)
            # print df

            session = get_session()
            for index, row in df.iterrows():
                print index, row[0]

                howard_miller = HowardMiller(row[0], smart_int(row[1]), row[2],
                                            smart_int(row[3]), row[4],
                                            smart_int(row[5]))
                self._log(howard_miller)
                session.add(howard_miller)
                session.commit()
                session.flush()
            session.close()

            dest = HOWARD_MILLER_PROCESSED_CSV_DIR
            self._log("Moving %s -> %s" % (csv,
                                           HOWARD_MILLER_PROCESSED_CSV_DIR))
            shutil.move(csv, HOWARD_MILLER_PROCESSED_CSV_DIR)
        except Exception as exp:
            self._log('process_csv_file() :: Got Exception: %s' % exp)
            self._log(traceback.format_exc())

    def run(self):
        while True:

            try:
                time.sleep(INGEST_SLEEP)

                self._log("Watching CSV files to be processed")
                csv_files = ["%s/%s" % (HOWARD_MILLER_CSV_DIR, f)
                             for f in listdir(HOWARD_MILLER_CSV_DIR)
                             if isfile(join(HOWARD_MILLER_CSV_DIR, f))]
                self._log("CSV Found: %s" % csv_files)

                for csv in csv_files:
                    self.process_csv_file(csv)

            except Exception as exp:
                self._log('run() :: Got exception: %s' % exp)
                self._log(traceback.format_exc())


if __name__ == "__main__":
    ingest_howard_miller = IngestHowardMiller()
    ingest_howard_miller.start()
