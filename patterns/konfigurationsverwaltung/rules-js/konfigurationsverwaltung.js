const HABSettings = {
  RGBW: {
    MaxDim: 90,
    DimPeriod: 20,
    DayColor: 205,
    AfternoonColor: 58,
    NightColor: 160
  },
  AC: {
    DayTemp: 22,
    NightTemp: 24
  },
  Light: {
    EveningDim: 70,
    NightDim: 20
  }
};

rules.JSRule({
  name: "Beispielregel fuer RGBW-Licht",
  triggers: [triggers.ItemStateChangeTrigger("SomeLight")],
  execute: (event) => {
    const maxDim = HABSettings.RGBW.MaxDim;
    const dimPeriod = HABSettings.RGBW.DimPeriod;
    console.log("MaxDim: " + maxDim + "%, DimPeriod: " + dimPeriod + "s");
    // Weitere Aktionen, z. B. Dimmen oder Farben einstellen
  }
});
