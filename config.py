import os

# export AMAZON_INVENTORY_DIR="/home/ted/work/DataPrediction/"

ROOT_DIR = os.environ['AMAZON_INVENTORY_DIR']

assert (ROOT_DIR, "AMAZON_INVENTORY_DIR is not defined")


HECKMAN_CSV_DIR = "%s/csv_files/heckman" % ROOT_DIR

HOWARD_MILLER_CSV_DIR = "%s/csv_files/howardmiller" % ROOT_DIR

HECKMAN_PROCESSED_CSV_DIR = "%s/processed_csv_files/heckman" % ROOT_DIR

HOWARD_MILLER_PROCESSED_CSV_DIR = "%s/processed_csv_files/howardmiller" % ROOT_DIR

INGEST_SLEEP = 20
