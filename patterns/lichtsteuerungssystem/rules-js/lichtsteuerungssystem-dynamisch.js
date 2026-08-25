rules.JSRule({
  name: "Adjust light brightness based on time of day",
  triggers: [triggers.GenericCronTrigger("0 0 18 ? * * *")],
  execute: (event) => {
    const hour = time.ZonedDateTime.now().hour();
    if (hour >= 18 && hour < 22) {
      items.getItem("Light1_Dimmer").sendCommand(80); // Helligkeit auf 80%
      console.log("Stunde=" + hour + " -> Light1_Dimmer 80%");
    } else {
      items.getItem("Light1_Dimmer").sendCommand(20); // Helligkeit auf 20%
      console.log("Stunde=" + hour + " -> Light1_Dimmer 20%");
    }
  }
});
