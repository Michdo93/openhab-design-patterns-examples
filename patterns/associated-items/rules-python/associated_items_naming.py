from openhab import Registry

status_item = Registry.getItem(item_name + "_Status")
status_item.postUpdate("ON")
