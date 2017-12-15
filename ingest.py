import threading
import traceback
from ingest_hekman import IngestHekman
from ingest_howard_miller import IngestHowardMiller


class Ingest(threading.Thread):
    """
    Features of class:-
    * process Hekman csv files
    * process HowardMiller csv files
    """

    def __init__(self):
        super(Ingest, self).__init__()
        self._log("initialised")
        self.ingest_hekman = IngestHekman()
        self.ingest_howard_miller = IngestHowardMiller()

    def _log(self, msg):
        print "[Ingest] :: %s" % msg

    def run(self):
        try:
            self.ingest_hekman.run()
            self.ingest_howard_miller.run()
        except Exception as exp:
            self._log("Got Exception: %s" % exp)
            self._log(traceback.format_exc())

if __name__ == "__main__":
    ingest = Ingest()
    ingest.start()
