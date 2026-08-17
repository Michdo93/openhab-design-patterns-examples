from openhab import rule
from openhab.triggers import ItemStateChangeTrigger

HAB_SETTINGS = {
    "RGBW": {
        "MaxDim": 90,
        "DimPeriod": 20,
        "DayColor": 205,
        "AfternoonColor": 58,
        "NightColor": 160,
    },
    "AC": {
        "DayTemp": 22,
        "NightTemp": 24,
    },
    "Light": {
        "EveningDim": 70,
        "NightDim": 20,
    },
}


@rule(triggers=[ItemStateChangeTrigger("SomeLight")])
class BeispielregelFuerRGBWLicht:
    def execute(self, module, input):
        max_dim = HAB_SETTINGS["RGBW"]["MaxDim"]
        dim_period = HAB_SETTINGS["RGBW"]["DimPeriod"]
        self.logger.info("MaxDim: {}%, DimPeriod: {}s".format(max_dim, dim_period))
        # Weitere Aktionen, z. B. Dimmen oder Farben einstellen
