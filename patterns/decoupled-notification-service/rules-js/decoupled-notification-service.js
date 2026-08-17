rules.JSRule({
  name: "Benachrichtigungsservice",
  triggers: [
    triggers.ItemStateChangeTrigger("VT_Notify_Info"),
    triggers.ItemStateChangeTrigger("VT_Notify_Warn"),
    triggers.ItemStateChangeTrigger("VT_Notify_Alert")
  ],
  execute: (event) => {
    const message = items.getItem(event.itemName).state;
    // Logik zum Versenden der Nachricht, z. B. per Mail oder Push-Notification
    console.log("[" + event.itemName + "] " + message);
  }
});
