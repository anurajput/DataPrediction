#
# Script for Parsing CSV files
#
import os
import traceback
from utils import sleep_timer, log
from prediction import InventoryPredictor

predictor = InventoryPredictor()


class Parser:

    tag = "Parser"

    def __init__(self):
        pass

    def csv_parser(self, file):
        method_name = 'csv_parser()'
        try:
            # count the no of lines
            with open(file) as f:
                for i, l in enumerate(f):
                        pass
            total_lines = i + 1
            log(self.tag, method_name, 'total lines in csv file: %s' %
                total_lines)

            # getting the data from the csv file
            csv_file = open(file, 'r')
            line = csv_file.readline()
            cnt = 1

            while cnt < total_lines:
                line = csv_file.readline()
                csv_data = line.split(',')

                log(self.tag, method_name, 'Item: %s' % csv_data[0])
                log(self.tag, method_name, 'Description: %s' % csv_data[1])
                log(self.tag, method_name, 'Status: %s' % csv_data[2])
                log(self.tag, method_name, 'Qty Avail: %s' % csv_data[3])
                log(self.tag, method_name, 'Qty: %s' % csv_data[4])
                log(self.tag, method_name, 'Available: %s' % csv_data[5])
                log(self.tag, method_name, 'Qty: %s' % csv_data[6])
                log(self.tag, method_name, 'Available: %s' % csv_data[7])
                log(self.tag, method_name, 'Retail: %s' % csv_data[8])
                log(self.tag, method_name, 'Pricing: %s' % csv_data[9])
                # predictor.make_predictions(self, csv_data[0], csv_data[1],
                #                            csv_data[2], csv_data[3],
                #                            csv_data[4], csv_data[5],
                #                            csv_data[6], csv_data[7],
                #                            csv_data[8], csv_data[9])
                cnt += 1

        except Exception as exp:
            log(self.tag, method_name, 'Got Exception: %s' % exp)
            log(self.tag, method_name, traceback.format_exc())


if __name__ == '__main__':
    parser = Parser()
    csv = os.listdir('./docs/csv_files')
    for file in csv:
        parser.csv_parser("./docs/csv_files/%s" % file)
        sleep_timer(file)
