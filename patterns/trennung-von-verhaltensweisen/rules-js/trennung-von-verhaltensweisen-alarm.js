rules.JSRule({
  name: "Send message",
  triggers: [
    triggers.ItemCommandTrigger("Notification_Proxy_Info"),
    triggers.ItemCommandTrigger("Notification_Proxy_Alert")
  ],
  execute: (event) => {
    if (event.itemName === "Notification_Proxy_Info") {
      actions.NotificationAction.sendNotification("admin@example.com", String(event.receivedCommand));
    } else {
      actions.NotificationAction.sendBroadcastNotification(String(event.receivedCommand));
    }
  }
});
