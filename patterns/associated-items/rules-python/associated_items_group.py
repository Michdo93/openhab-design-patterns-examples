from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("gSensors")])
class ZugehoerigesItemUeberGruppenzugehoerigkeitFinden:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        sensors = Registry.getItem("gSensors").getAllMembers()

        # Ansatz: Item-Name
        status1 = next((i for i in sensors if i.getName() == item_name + "_Status"), None)

        # Ansatz: Item-Tag
        status2 = next((i for i in sensors if "Status" in i.getTags()), None)

        # Ansatz: Item-Tags
        status3 = next(
            (i for i in sensors if all(t in i.getTags() for t in ("Status", "Power"))),
            None,
        )

        # Ansatz: mehrere Kriterien
        status4 = next(
            (i for i in sensors
             if "Status" in i.getTags() and i.getName().endswith("_Status") and i.getType() == "Switch"),
            None,
        )

        self.logger.info(
            "status1={} status2={}".format(
                status1.getName() if status1 else None,
                status2.getName() if status2 else None,
            )
        )
