from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("TemperatureRooms")])
class WarningsAndAlertsForTemperature:
    def execute(self, module, input):
        hour = datetime.now().hour
        members = Registry.getItem("TemperatureRooms").members

        if 9 <= hour < 21:  # 9 bis 21 Uhr
            for r in members:
                temp = float(str(r.state))
                if 25 <= temp < 30:
                    self.logger.info("Temp warn {}: {} Grad C".format(r.name, temp))
                    # Weitere Benachrichtigungen

        for r in members:
            temp = float(str(r.state))
            if temp >= 30:
                self.logger.info("Temp alert {}: {} Grad C".format(r.name, temp))
                # Weitere Benachrichtigungen
