#
# script for quick internal tests
#

from models import Inventory

def create_inventory():
    try:
        inv = Inventory(id, "item", "description", "status", "sty_avail", "qty", "available", "qty_", "available_", "retail", "pricing")
        inv.save()

    except Exception as exp:
        print("create_inventory() got exception: \n%s" % exp)

