#
# script for quick internal tests
#

from models import Inventory, get_session

def create_inventory():
    try:
        inv = Inventory("item", "description", "status", "sty_avail", "qty", "available", "qty_", "available_", "retail", "pricing")
        session = get_session()
        print "Inventory = %s" % inv
        session.add(inv)
        session.commit()
        session.flush()
        session.close()

    except Exception as exp:
        print("create_inventory() got exception: \n%s" % exp)

create_inventory()
