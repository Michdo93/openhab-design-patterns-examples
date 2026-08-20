from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("TemperatureRooms")])
class WarningsAndAlertsForTemperature:
    def execute(self, module, input):
        hour = datetime.now().hour
        members = Registry.getItem("TemperatureRooms").getAllMembers()

        if 9 <= hour < 21:  # 9 bis 21 Uhr
            for r in members:
                state = str(r.getState())
                if state in ("NULL", "UNDEF"):
                    continue
                temp = float(state)
                if 25 <= temp < 30:
                    self.logger.info("Temp warn {}: {} Grad C".format(r.getName(), temp))
                    # Weitere Benachrichtigungen

        for r in members:
            state = str(r.getState())
            if state in ("NULL", "UNDEF"):
                continue
            temp = float(state)
            if temp >= 30:
                self.logger.info("Temp alert {}: {} Grad C".format(r.getName(), temp))
                # Weitere Benachrichtigungen
