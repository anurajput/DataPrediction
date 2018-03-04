#
# script process all the output csv files
# and write them into db
#

import traceback
from models import PredictionResult, get_session
from os import listdir
from os.path import isfile, join
import pandas as pd

import logging
logger = logging.getLogger(__name__)

def set_logger():
    level = logging.INFO

    logger.setLevel(level)

    # log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # setup file handler
    file_handler = logging.FileHandler('write_results_to_db.log')
    file_handler.setLevel(level)

    # create a logging format
    file_handler.setFormatter(formatter)

    # setup stream/console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info('Hello baby')


def get_forecast_files():
    mypath = "./output/"
    return [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith("forecast.csv")]


def show_row(row):
    dt = row[1]
    aq = row[2]
    sfd = row[3]
    ro = row[4]

    logger.debug( "--- dt [%s]" % dt)
    logger.debug( "--- aq [%s]" % aq)
    logger.debug( "--- sdf [%s]" % sfd)
    logger.debug( "--- ro [%s]" % ro)

def dump_csv_to_db(f):
    session = get_session()
    try:
        path = "./output/%s" % f
        model_number = f.split("-")[0]
        logger.info("Processing item: %s" % model_number)
        df = pd.read_csv(path, header=None)
        for index, row in df.iterrows():
            if index == 0:
                continue
            show_row(row)
            runs_out = row[4]
            print "-----------> runs_out = [%s] " % runs_out
            if int(runs_out) < 0:
                runs_out = "N"
            pr = PredictionResult(row[1], model_number, int(row[2]), int(row[3]), row[4] )
            session.add(pr)
            session.commit()
            session.flush()
    except Exception as exp:
        logger.warn('dump_csv_to_db() :: got Exception: %s' % exp)
        logger.warn(traceback.format_exc())
    session.close()


def main():
    set_logger()

    # get all forecast csv files
    forecast_files = get_forecast_files()
    for f in forecast_files:
        dump_csv_to_db(f)


if __name__ == '__main__':
    main()
