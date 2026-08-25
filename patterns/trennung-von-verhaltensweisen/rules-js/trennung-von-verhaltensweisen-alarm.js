rules.JSRule({
  name: "Send message",
  triggers: [
    triggers.ItemCommandTrigger("Notification_Proxy_Info"),
    triggers.ItemCommandTrigger("Notification_Proxy_Alert")
  ],
  execute: (event) => {
    const message = String(event.receivedCommand);
    try {
      if (event.itemName === "Notification_Proxy_Info") {
        actions.NotificationAction.sendNotification("admin@example.com", message);
      } else {
        actions.NotificationAction.sendBroadcastNotification(message);
      }
      console.log(event.itemName + " -> Cloud-Benachrichtigung gesendet: " + message);
    } catch (e) {
      console.warn("Cloud-Benachrichtigung nicht verfuegbar (" + event.itemName + "): " + e.message + " - Nachricht: " + message);
    }
  }
});
