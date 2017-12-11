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


class Inventory(base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    item = Column(String(200))
    description = Column(String(200))
    status = Column(String(200))
    sty_avail = Column(String(200))
    qty = Column(String(200))
    available = Column(String(200))
    qty_ = Column(String(200))
    available_ = Column(String(200))
    retail = Column(String(200))
    pricing = Column(String(200))

    def __init__(self, id, item, description, status, sty_avail, qty,
                 available, qty_, available_, retail, pricing):
        self.id = id
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

def setup_db():
    try:
        Session = sessionmaker(db)
        session = Session()
        base.metadata.create_all(db)
        print("Database Create Successfull")
    except Exception as exp:
        print("Failed to create database, got exception: \n%s" % exp)

if __name__ == '__main__':
    setup_db()
