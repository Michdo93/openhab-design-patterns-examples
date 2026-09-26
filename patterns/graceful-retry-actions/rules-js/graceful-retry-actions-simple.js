const MAX_RETRIES = 3;
const RETRY_INTERVAL = 10; // Sekunden

rules.JSRule({
  name: "Graceful Retry LightSwitch",
  triggers: [triggers.ItemStateChangeTrigger("SomeTrigger", undefined, "ON")],
  execute: (event) => {
    let retryCount = 0;
    let retryTimer = null;

    const attempt = () => {
      try {
        items.getItem("LightSwitch").sendCommand("ON");
        console.log("Command sent successfully!");
        if (retryTimer !== null) retryTimer.cancel();
      } catch (e) {
        retryCount++;
        console.warn("Error while sending, attempt #" + retryCount);
        if (retryCount < MAX_RETRIES) {
          retryTimer.reschedule(time.ZonedDateTime.now().plusSeconds(RETRY_INTERVAL));
        } else {
          console.error("Maximum number of attempts reached!");
          try {
            items.getItem("NotificationItem").postUpdate("LightSwitch could not be switched ON");
          } catch (notifyItemEx) {
            console.warn("Could not update NotificationItem: " + notifyItemEx.message);
          }
          try {
            if (actions.NotificationAction) {
              actions.NotificationAction.sendNotification("admin@example.com", "LightSwitch could not be switched ON");
            }
          } catch (notifyEx) {
            console.warn("Cloud notification not available: " + notifyEx.message);
          }
        }
      }
    };

    retryTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), attempt);
  }
});
