from predict_item import PredictItem
from models import Hekman, get_session
import time

class PredictAll:

    def get_all_unique_model_numbers(self):
        session = get_session()
        query = session.query(Hekman.model_number.distinct().label("model_number"))
        self.model_numbers = [row.model_number for row in query.all()]
        return self.model_numbers

    def process_all(self):
        for model_number in self.model_numbers:
            print "======= Processing [ %s ] ============" % model_number
            pi = PredictItem(model_number, False)
            pi.forecast()
            print
            print


def main():
    pa = PredictAll()
    print len(pa.get_all_unique_model_numbers())
    pa.process_all()
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Total Time taken: %0.2f seconds ---" % (time.time() - start_time))
    
