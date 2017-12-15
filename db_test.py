#
# script for quick internal tests
#

from models import Hekman, get_session
import traceback

model_number = '16102'


def _log(msg):
        print "[DB_Test] :: %s" % msg


def create_hekman():
    try:
        session = get_session()
        query = session.query(Hekman).filter(Hekman.model_number ==
                                             model_number).first()
        _log('model_number: %s' % query.model_number)
        _log('description: %s' % query.description)
        _log('supply_for_days: %s' % query.supply_for_days)
        _log('available_qty: %s' % query.available_qty)
        _log('next_produce_qty: %s' % query.next_produce_qty)
        _log('next_produce_date: %s' % query.next_produce_date)
        _log('next_schedule_produce_qty: %s' % query.next_schedule_produce_qty)
        _log('next_schedule_produce_date: %s' % query.next_schedule_produce_date)
        _log('retail: %s' % query.retail)
        _log('pricing: %s' % query.pricing)
    except Exception as exp:
        print("create_inventory() got exception: \n%s" % exp)
        print (traceback.format_exc())

create_hekman()

