from Inventory import (INVENTORY_DETAIL_STATUS_EXHAUST,
                       INVENTORY_DETAIL_STATUS_NORMAL)


def update_inventory_status(*args, **kwargs):
    inst = kwargs['instance']
    if (inst.count > 0 and inst.status == INVENTORY_DETAIL_STATUS_EXHAUST):
        inst.status = INVENTORY_DETAIL_STATUS_NORMAL
    elif (inst.count == 0 and inst.status == INVENTORY_DETAIL_STATUS_NORMAL):
        inst.status = INVENTORY_DETAIL_STATUS_EXHAUST
