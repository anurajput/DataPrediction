#
# Script for Parsing CSV files
#
import os
import traceback
from utils import sleep_timer


class Parser:

    tag = "Parser"

    def __init__(self):
        pass

    def log(self, method_name, msg):
        print('[%s] :: %s :: %s' % (self.tag, method_name, msg))

    def csv_parser(self, file):
        method_name = 'csv_parser()'
        try:
            print('file: %s' % file)
            # count the no of lines
            with open(file) as f:
                for i, l in enumerate(f):
                        pass
            total_lines = i + 1
            self.log(method_name, 'total lines in csv file: %s' % total_lines)

            # getting the data from the csv file
            csv_file = open(file, 'r')
            line = csv_file.readline()
            cnt = 1

            while cnt < total_lines:
                line = csv_file.readline()
                csv_data = line.split(',')

                self.log(method_name, 'Item: %s' % csv_data[0])
                self.log(method_name, 'Description: %s' % csv_data[1])
                self.log(method_name, 'Status: %s' % csv_data[2])
                self.log(method_name, 'Qty Avail: %s' % csv_data[3])
                self.log(method_name, 'Qty: %s' % csv_data[4])
                self.log(method_name, 'Available: %s' % csv_data[5])
                self.log(method_name, 'Qty: %s' % csv_data[6])
                self.log(method_name, 'Available: %s' % csv_data[7])
                self.log(method_name, 'Retail: %s' % csv_data[8])
                self.log(method_name, 'Pricing: %s' % csv_data[9])
                cnt += 1

        except Exception as exp:
            self.log(method_name, 'Got Exception: %s' % exp)
            self.log(method_name, traceback.format_exc())


if __name__ == '__main__':
    parser = Parser()
    csv = os.listdir('./docs/csv_files')
    for file in csv:
        parser.csv_parser("./docs/csv_files/%s" % file)
        sleep_timer(file)
