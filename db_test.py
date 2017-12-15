#
# script for quick internal tests
#

from models import Hekman, get_session

model_number = '16102'


def create_hekman():
    try:
        session = get_session()
        query = session.query(Hekman).filter(Hekman.model_number ==
                                             model_number).first()
        print '==============', query.description
        print '++++++++++++++', query.next_produce_qty
    except Exception as exp:
        print("create_inventory() got exception: \n%s" % exp)

create_hekman()
