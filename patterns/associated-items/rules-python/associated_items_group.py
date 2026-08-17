from openhab import Registry

sensors = Registry.getItem("gSensors").members

# Ansatz: Item-Name
status1 = next((i for i in sensors if i.name == item_name + "_Status"), None)

# Ansatz: Item-Tag
status2 = next((i for i in sensors if "Status" in i.tags), None)

# Ansatz: Item-Tags
status3 = next((i for i in sensors if all(t in i.tags for t in ("Status", "Power"))), None)

# Ansatz: mehrere Kriterien
status4 = next(
    (i for i in sensors if "Status" in i.tags and i.name.endswith("_Status") and i.type == "Switch"),
    None,
)
