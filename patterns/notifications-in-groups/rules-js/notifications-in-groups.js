rules.JSRule({
  name: "Warnings and alerts for temperature",
  triggers: [triggers.GroupStateChangeTrigger("TemperatureRooms")],
  execute: (event) => {
    const hour = time.ZonedDateTime.now().hour();
    const members = items.getItem("TemperatureRooms").members;

    if (hour >= 9 && hour < 21) { // 9 bis 21 Uhr
      members
        .filter((t) => parseFloat(t.state) >= 25 && parseFloat(t.state) < 30)
        .forEach((r) => {
          console.log("Temp warn " + r.name + ": " + r.state + " Grad C");
          // Weitere Benachrichtigungen
        });
    }

    members
      .filter((t) => parseFloat(t.state) >= 30)
      .forEach((r) => {
        console.log("Temp alert " + r.name + ": " + r.state + " Grad C");
        // Weitere Benachrichtigungen
      });
  }
});
