#
# script for various ORM models for project
#

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
class Inventory(base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String(200))
    description = Column(String(200))
    status = Column(String(200))
    sty_avail = Column(Integer)
    qty = Column(Integer)
    available = Column(Integer)
    qty_ = Column(Integer)
    available_ = Column(Integer)
    retail = Column(Integer)
    pricing = Column(Integer)

    def __init__(self, item, description, status, sty_avail, qty,
                 available, qty_, available_, retail, pricing):
        self.item = item
        self.description = description
        self.status = status
        self.sty_avail = sty_avail
        self.qty = qty
        self.available = available
        self.qty_ = qty_
        self.available_ = available_
        self.retail = retail
        self.pricing = pricing

    def __repr__(self):
        return "<Inventory> item: %s" % self.item

    @property
    def serialize(self):

        """ Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'item': self.item,
            'description': self.description,
            'status': self.status,
            'sty_avail': self.sty_avail,
            'qty': self.qty,
            'available': self.available,
            'qty_': self.qty_,
            'available_': self.available_,
            'retail': self.retail,
            'pricing': self.pricing
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

if __name__ == '__main__':
    setup_db()
