const MAX_RETRIES_BACKOFF = 5;
const MAX_INTERVAL = 60;

rules.JSRule({
  name: "Graceful Retry LightSwitch with Backoff",
  triggers: [triggers.ItemStateChangeTrigger("SomeTrigger", undefined, "ON")],
  execute: (event) => {
    let retryCount = 0;
    let retryInterval = 5;
    let retryTimer = null;

    const attempt = () => {
      try {
        items.getItem("LightSwitch").sendCommand("ON");
        console.log("Command sent successfully!");
        if (retryTimer !== null) retryTimer.cancel();
      } catch (e) {
        retryCount++;
        console.warn("Failed attempt #" + retryCount);
        if (retryCount < MAX_RETRIES_BACKOFF) {
          retryInterval = Math.min(retryInterval * 2, MAX_INTERVAL);
          console.log("Next attempt in " + retryInterval + " seconds");
          retryTimer.reschedule(time.ZonedDateTime.now().plusSeconds(retryInterval));
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
