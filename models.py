#
# script for various ORM models for project
#
import traceback
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "postgres://amz_inv:123@localhost/amz_inv_db"
db = create_engine(db_url)
base = declarative_base()

########################################################################################
#
#  HowardMiller
#  A - model_number
#  B - stock_qty
#  C - next_available_date
#  D - next_qty
#  E - prod_date
#  F - prod_quantity
#
#  Hekman
#  A - model_number
#  B - description
#  C - supply_for_days
#  D - available_qty
#  E - next_produce_qty
#  F - next_produce_date
#  G - next_schedule_produce_qty
#  H - next_schedule_produce_date
#  I - retail
#  J - pricing
# 
########################################################################################


class Hekman(base):

    __tablename__ = 'hekman'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(64))
    model_number = Column(String(64))
    description = Column(String(1024))
    supply_for_days = Column(String(64))
    available_qty = Column(Integer)
    next_produce_qty = Column(Integer)
    next_produce_date = Column(String(64))
    next_schedule_produce_qty = Column(Integer)
    next_schedule_produce_date = Column(String(64))
    retail = Column(Integer)
    pricing = Column(Integer)

    def __init__(self, date, model_number, description, supply_for_days,
                 available_qty, next_produce_qty, next_produce_date,
                 next_schedule_produce_qty, next_schedule_produce_date,
                 retail, pricing):
        self.date = date
        self.model_number = model_number
        self.description = description
        self.supply_for_days = supply_for_days
        self.available_qty = available_qty
        self.next_produce_qty = next_produce_qty
        self.next_produce_date = next_produce_date
        self.next_schedule_produce_qty = next_schedule_produce_qty
        self.next_schedule_produce_date = next_schedule_produce_date
        self.retail = retail
        self.pricing = pricing

    def __repr__(self):
        return "<Hekman> %s - %d" % (self.model_number, self.pricing)


class HowardMiller(base):

    __tablename__ = 'howardMiller'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(64))
    model_number = Column(String(1024))
    stock_qty = Column(Integer)
    next_available_date = Column(String(64))
    next_qty = Column(Integer)
    prod_date = Column(String(64))
    prod_quantity = Column(Integer)

    def __init__(self, date, model_number, stock_qty, next_available_date,
                 next_qty, prod_date, prod_quantity):
        self.date = date
        self.model_number = model_number
        self.stock_qty = stock_qty
        self.next_available_date = next_available_date
        self.next_qty = next_qty
        self.prod_date = prod_date
        self.prod_quantity = prod_quantity

    def __repr__(self):
        return "<HowardMiller> model_number: %s" % self.model_number

    @property
    def serialize(self):

        """ Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'model_number': self.model_number,
            'stock_qty': self.stock_qty,
            'next_available_date': self.next_available_date,
            'next_qty': self.next_qty,
            'prod_date': self.prod_date,
            'prod_quantity': self.prod_quantity
        }

class PredictionResult(base):

    __tablename__ = 'prediction_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(64))
    model_number = Column(String(64))
    available_qty = Column(Integer)
    supply_for_days = Column(Integer)
    runs_out_before_next_stock = Column(String(1))

    def __init__(self, date, model_number, available_qty, supply_for_days,
            runs_out_before_next_stock):
        self.date = date
        self.model_number = model_number
        self.available_qty = available_qty
        self.supply_for_days = supply_for_days
        self.runs_out_before_next_stock = runs_out_before_next_stock

    def __repr__(self):
        return "<Prediction> model_number: %s" % self.model_number

    @property
    def serialize(self):

        """ Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'model_number': self.model_number,
            'available_qty': self.available_qty,
            'supply_for_days': self.supply_for_days,
            'runs_out_before_next_stock': self.runs_out_before_next_stock
        }


def get_session():
    Session = sessionmaker(db)
    session = Session()
    return session


def setup_db():
    try:
        base.metadata.create_all(db)
        print("Database Created Successfully")
    except Exception as exp:
        print("Failed to create database, got exception: \n%s" % exp)
        print(traceback.format_exc())

if __name__ == '__main__':
    setup_db()
