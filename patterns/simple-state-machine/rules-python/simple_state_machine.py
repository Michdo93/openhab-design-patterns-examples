from openhab import rule, Registry
from openhab.actions import Ephemeris
from openhab.triggers import GenericCronTrigger


@rule(triggers=[GenericCronTrigger("0 0 6 * * ?")])
class TimeOfDayMorningNurWochentage:
    def execute(self, module, input):
        if Ephemeris.isWeekday():
            Registry.getItem("TimeOfDay").sendCommand("MORNING")
