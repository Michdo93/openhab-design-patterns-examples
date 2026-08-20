import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

retry_timers = {}
retry_counts = {}


def attempt(device, max_retries, initial_interval, max_interval, alt_action):
    try:
        state = Registry.getItem(device).getState()
        if str(state) != "NULL":
            Registry.getItem(device).sendCommand("ON")
            logger.info(device + " command sent successfully!")
            if device in retry_timers:
                retry_timers[device].cancel()
        else:
            raise Exception("Device " + device + " is offline")
    except Exception as ex:
        count = retry_counts.get(device, 0) + 1
        retry_counts[device] = count
        logger.warn("{} attempt #{} failed: {}".format(device, count, ex))

        if count < max_retries:
            next_interval = min(initial_interval * (2 ** count), max_interval)
            logger.info("Next attempt for {} in {} seconds".format(device, next_interval))
            t = threading.Timer(
                next_interval, attempt, args=(device, max_retries, initial_interval, max_interval, alt_action)
            )
            t.start()
            retry_timers[device] = t
        else:
            logger.error(device + " max retries reached!")
            message = (device + ": " + alt_action) if alt_action else (device + " could not be switched ON!")
            NotificationAction.sendNotification("admin@example.com", message)


@rule(triggers=[ItemStateChangeTrigger("RetryTrigger", state="ON")])
class ConfigurableMultiDeviceRetry:
    def execute(self, module, input):
        max_retries = int(str(Registry.getItem("RetryMaxAttempts").getState()))
        initial_interval = int(str(Registry.getItem("RetryInitialInterval").getState()))
        max_interval = int(str(Registry.getItem("RetryMaxInterval").getState()))
        alt_action = str(Registry.getItem("RetryAlternativeAction").getState())

        devices = [i.getName() for i in Registry.getItem("RetryDevices").getAllMembers()]

        for device in devices:
            retry_counts[device] = 0
            attempt(device, max_retries, initial_interval, max_interval, alt_action)
